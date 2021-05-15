# request new capture if most recent capture is more than this many days old
MAX_CAPTURE_AGE = 30

# time in seconds to wait between requests
PERIOD = 600

# network timeout threshold in seconds
TIMEOUT = 60.0

DEFAULT_PARAMS = {
    # Capture a web page with errors (HTTP status=4xx or 5xx).
    # 'capture_all': 1,

    # Capture web page outlinks automatically.
    # 'capture_outlinks': 1,

    # Capture full page screenshot in PNG format.
    # 'capture_screenshot': 1,

    # Force the use of a simple HTTP GET request to capture the target URL.
    # 'force_get': 1,

    # Skip checking if a capture is a first.
    'skip_first_archive': 1,

    # Capture web page only if the latest existing capture at the
    # Archive is older than the <timedelta> limit. When using 2 comma
    # separated <timedelta> values, the first one applies to the main
    # capture and the second one applies to outlinks.
    # 'if_not_archived_within': '7d',

    # Return the timestamp of the last capture for all outlinks.
    # 'outlinks_availability': 1,

    # Send an email report of the captured URLs to the user’s email.
    # 'email_result': 1,

    # Run JS code for <N> seconds after page load.
    'js_behavior_timeout': 0,

    # Use extra HTTP Cookie value when capturing the target page.
    # 'capture_cookie': 'XXX',

    # Use your own username and password in the target page’s login forms.
    # 'target_username': 'XXX',
    # 'target_password': 'YYY',
}
