# Archive a list of URLs using the Wayback Machine

This script uses the [Save Page Now 2 Public API](https://docs.google.com/document/d/1Nsv52MvSjbLb2PCpHlat0gkzw0EvtSgpKHu4mk0MnrA/edit).

To use it:

1. Clone or [download](https://github.com/rybesh/capture-urls/archive/refs/heads/main.zip "download repository as a zip file") and unzip this repository.

1. Install the required Python libraries. Assuming you cloned or
   unzipped this repository to the directory `path/to/capture-urls/`:

   ```
   cd path/to/capture-urls/
   make
   ```

1. Go to https://archive.org/account/s3.php and get your S3-like API keys.

1. In `path/to/capture-urls/`, create a file called `secret.py` with
   the following contents:

   ```python
   ACCESS_KEY = 'your access key'
   SECRET_KEY = 'your secret key'
   ```
   
   (Use the actual values of your access key and secret key, not `your
   access key` and `your secret key`.)
   
1. *Optionally* edit `config.py` to your liking.

1. Archive your URLs:
   ```
   cat urls.txt | ./capture-urls.py > archived-urls.txt
   ```
   `urls.txt` should contain a list of URLs to be archived, one on each line.

1. Archiving URLs can take a long time. You can interrupt the process
   with `Ctrl-C`. This will create a file called `progress.json` with
   the state of the archiving process so far. If you start the process
   again, it will pick up where it left off. You can add new URLs to
   `urls.txt` before you restart the process.

1. When it finishes running you should have a list of the archived
   URLs in `archived-urls.txt`.
