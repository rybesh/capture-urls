ERROR_MESSAGES = {
    'error:invalid-url-syntax':
    'Target URL syntax is not valid.',

    'error:invalid-url':
    'Target URL is not available.',

    'error:invalid-server-response':
    'The target server response was invalid.',

    'error:invalid-host-resolution':
    'Couldn’t resolve the target host.',

    'error:user-session-limit':
    'User has reached the limit of 10 concurrent active capture sessions.',

    'error:soft-time-limit-exceeded':
    'Capture duration exceeded 40s time limit and was terminated.',

    'error:proxy-error':
    'SPN2 back-end proxy error.',

    'error:browsing-timeout':
    'SPN2 back-end headless browser timeout.',

    'error:no-browsers-available':
    'SPN2 back-end headless browser cannot run.',

    'error:redis-error':
    'SPN2 back-end Redis error.',

    'error:capture-location-error':
    'SPN2 back-end cannot find the created capture location.',

    'error:gateway-timeout':
    'The target server did not respond in time.',

    'error:no-access':
    'Target URL could not be accessed.',

    'error:not-found':
    'Target URL not found.',

    'error:celery':
    'Cannot start capture task.',

    'error:filesize-limit':
    'Cannot capture web resources over 2GB.',

    'error:blocked-url':
    'Attempted to capture a blocked URL.',

    'error:too-many-daily-captures':
    'URL has been captured 10 times today, cannot make any more captures.',

    'error:ftp-access-denied':
    'Tried to capture an FTP resource but access was denied.',

    'error:read-timeout':
    'HTTP connection read timeout.',

    'error:protocol-error':
    'HTTP connection broken.',

    'error:too-many-redirects':
    'Too many redirects.',

    'error:too-many-requests':
    'The target host has received too many requests from Save Page Now.',

    'error:not-implemented':
    'The request method is not supported by the server.',

    'error:bad-gateway':
    'Bad Gateway for URL.',

    'error:service-unavailable':
    'Service unavailable for URL.',

    'error:http-version-not-supported':
    'The server does not support the HTTP protocol version used.',

    'error:network-authentication-required':
    'The client needs to authenticate to gain network access to URL.',
}
