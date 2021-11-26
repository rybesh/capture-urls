#! ./venv/bin/python3.10

import sys

if sys.version_info.major < 3 or sys.version_info.minor < 10:
    sys.exit("You need Python 3.10 or later to run this script.")


import httpx
import json
import os
import re
from datetime import datetime
from enum import Enum
from ratelimit import limits, sleep_and_retry
from typing import Union, NamedTuple


from secret import ACCESS_KEY, SECRET_KEY
from config import MAX_CAPTURE_AGE, PERIOD, TIMEOUT, DEFAULT_PARAMS, USER_AGENT
from errors import ERROR_MESSAGES


class Progress(NamedTuple):
    capture_requests: dict[str, dict[str, str]]
    pending_urls: dict[str, str]
    captured_urls: dict[str, str]
    failed_urls: set[str]


class Status(Enum):
    pending = "pending"
    error = "error"
    success = "success"


def log(x):
    print(x, file=sys.stderr)


def log_error(result: dict):
    if "status_ext" in result:
        message = ERROR_MESSAGES.get(
            result["status_ext"], ERROR_MESSAGES["error:unknown"]
        )
        log(" - " + message)
    if "message" in result:
        log(" - " + result["message"])


def log_progress(progress: Progress):
    log(
        f"{len(progress.captured_urls)} captured"
        + f", {len(progress.failed_urls)} failed"
        + f", {len(progress.pending_urls)} pending"
    )


@sleep_and_retry
@limits(calls=1, period=PERIOD)
def post_request(client, url, data: dict) -> Union[dict, list, None]:
    try:
        r = client.post(
            url,
            headers={
                "Accept": "application/json",
                "Authorization": f"LOW {ACCESS_KEY}:{SECRET_KEY}",
            },
            data=data,
        )
        if r.status_code == 200:
            return r.json()
        else:
            log(f"POST to {url} returned {r.status_code}")
    except httpx.RequestError as e:
        log(f"POST to {url} failed:")
        log(e)

    return None


def capture(client, url) -> Union[dict, None]:
    result = post_request(
        client, "https://web.archive.org/save", data={**DEFAULT_PARAMS, **{"url": url}}
    )
    if (
        result is not None
        and type(result) is dict
        and "job_id" in result
        and "url" in result
    ):
        return result
    else:
        return None


def check_status(client, job_ids: list) -> list:
    all_results = []
    for batch in (job_ids[i : i + 5] for i in range(0, len(job_ids), 5)):
        log("checking capture request status for jobs:")
        for job_id in batch:
            log(f"  {job_id}")
        results = post_request(
            client,
            "https://web.archive.org/save/status",
            data={"job_ids": ",".join(job_ids)},
        )
        if results is not None and type(results) is list:
            all_results += results
        else:
            log("status check failed")
    return all_results


def get_last_capture_url(client, url) -> Union[str, None]:
    redirect_url = f"https://web.archive.org/web/2/{url}"
    try:
        r = client.get(redirect_url)
        if r.status_code == 302:
            return r.headers.get("location", "")
        else:
            log(f"GET to {redirect_url} returned {r.status_code}")
    except httpx.RequestError as e:
        log(f"GET to {redirect_url} failed:")
        log(e)

    return None


def get_capture_timestamp(capture_url) -> Union[str, None]:
    m = re.match(r"^https://web.archive.org/web/(\d+)/http.*$", capture_url)
    if m is None:
        return None
    else:
        return m.group(1)


def get_timestamp_age(timestamp) -> Union[int, None]:
    try:
        return (datetime.utcnow() - datetime.strptime(timestamp, "%Y%m%d%H%M%S")).days
    except ValueError:
        return None


def process_input_url(client, url, progress: Progress):
    if (
        url in progress.pending_urls
        or url in progress.failed_urls
        or url in progress.captured_urls
    ):
        return

    log(url)
    last_capture_url = get_last_capture_url(client, url)
    if last_capture_url is None:
        log(" - has not been captured")
        return

    last_capture_timestamp = get_capture_timestamp(last_capture_url)
    if last_capture_timestamp is None:
        log(" - has not been captured")
        return

    last_capture_age = get_timestamp_age(last_capture_timestamp)
    if last_capture_age is None:
        log(" - has not been captured")
        return

    log(
        f" - was last captured {last_capture_age} "
        + f'day{"" if last_capture_age == 1 else "s"} ago'
    )

    if last_capture_age <= MAX_CAPTURE_AGE:
        progress.captured_urls[url] = last_capture_timestamp
    else:
        log(" - submitting capture request")
        capture_request = capture(client, url)
        if capture_request is None:
            progress.failed_urls.add(url)
        else:
            job_id = capture_request["job_id"]
            log(f" - job id: {job_id}")
            progress.capture_requests[job_id] = capture_request
            progress.pending_urls[url] = job_id


def process_result(result: dict, progress: Progress):
    job_id = result.get("job_id")
    if job_id is None:
        log("missing job ID in results; ignoring")
        return

    url = progress.capture_requests[job_id]["url"]
    if url not in progress.pending_urls:
        log("already-processed job ID in results; ignoring")
        return

    log(url)
    log(f" - job id: {job_id}")

    try:
        status = Status(result.get("status", "error"))
    except ValueError:
        status = Status.error

    if status is not Status.pending:
        del progress.pending_urls[url]
    else:
        log(" - capture still pending")

    if status is Status.error:
        log(" - capture failed")
        progress.failed_urls.add(url)
        log_error(result)

    elif status is Status.success:
        log(" - capture succeeded")
        timestamp = result.get("timestamp", "2")
        progress.captured_urls[url] = timestamp


def capture_urls(progress: Progress):
    with httpx.Client(headers={"user-agent": USER_AGENT}, timeout=TIMEOUT) as client:
        for url in map(str.rstrip, sys.stdin):
            process_input_url(client, url, progress)

        while len(progress.pending_urls) > 0:
            for result in check_status(client, list(progress.pending_urls.values())):
                process_result(result, progress)
            log_progress(progress)


def load_progress():
    if os.path.isfile(PROGRESS_FILENAME):
        progress = None
        with open(PROGRESS_FILENAME) as f:
            o = json.load(f)
            progress = Progress(
                capture_requests=o["capture_requests"],
                pending_urls=o["pending_job_ids"],
                captured_urls=o["captured_urls"],
                failed_urls=set(o["failed_urls"]),
            )
        os.remove(PROGRESS_FILENAME)
        return progress
    else:
        return Progress(
            capture_requests={},
            pending_urls={},
            captured_urls={},
            failed_urls=set(),
        )


def save_progress(progress: Progress):
    with open(PROGRESS_FILENAME, mode="w") as f:
        json.dump(
            {
                "capture_requests": progress.capture_requests,
                "pending_job_ids": progress.pending_urls,
                "captured_urls": progress.captured_urls,
                "failed_urls": list(progress.failed_urls),
            },
            f,
        )


def main():
    progress = load_progress()
    try:
        capture_urls(progress)

        if len(progress.failed_urls) > 0:
            log("\ncapturing the following URLs failed:")
            for url in sorted(progress.failed_urls):
                log(url)

        for url in sorted(progress.captured_urls):
            timestamp = progress.captured_urls[url]
            print(f"https://web.archive.org/web/{timestamp}/{url}")

    except KeyboardInterrupt:
        save_progress(progress)
        sys.exit()


PROGRESS_FILENAME = "progress.json"

if __name__ == "__main__":
    main()
