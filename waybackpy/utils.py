import re
import time
import requests
from .exceptions import WaybackError, URLError
from datetime import datetime

from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from .__version__ import __version__

quote = requests.utils.quote
default_user_agent = "waybackpy python package - https://github.com/akamhy/waybackpy"


def _latest_version(package_name, headers):
    endpoint = "https://pypi.org/pypi/" + package_name + "/json"
    json = _get_response(endpoint, headers=headers).json()
    return json["info"]["version"]


def _unix_ts_to_wayback_ts(unix_ts):
    return datetime.utcfromtimestamp(int(unix_ts)).strftime("%Y%m%d%H%M%S")


def _add_payload(instance, payload):
    if instance.start_timestamp:
        payload["from"] = instance.start_timestamp

    if instance.end_timestamp:
        payload["to"] = instance.end_timestamp

    if instance.gzip != True:
        payload["gzip"] = "false"

    if instance.match_type:
        payload["matchType"] = instance.match_type

    if instance.filters and len(instance.filters) > 0:
        for i, f in enumerate(instance.filters):
            payload["filter" + str(i)] = f

    if instance.collapses and len(instance.collapses) > 0:
        for i, f in enumerate(instance.collapses):
            payload["collapse" + str(i)] = f

    payload["url"] = instance.url


def _ts(timestamp, data):
    """
    Get timestamp of last fetched archive.
    If used before fetching any archive, will
    use whatever self.JSON returns.

    self.timestamp is None implies that
    self.JSON will return any archive's JSON
    that wayback machine provides it.
    """

    if timestamp:
        return timestamp

    if not data["archived_snapshots"]:
        return datetime.max

    return datetime.strptime(
        data["archived_snapshots"]["closest"]["timestamp"], "%Y%m%d%H%M%S"
    )


def _check_match_type(match_type, url):
    if not match_type:
        return

    if "*" in url:
        raise WaybackError("Can not use wildcard with match_type argument")

    legal_match_type = ["exact", "prefix", "host", "domain"]

    if match_type not in legal_match_type:
        exc_message = "{match_type} is not an allowed match type.\nUse one from 'exact', 'prefix', 'host' or 'domain'".format(
            match_type=match_type
        )
        raise WaybackError(exc_message)


def _check_collapses(collapses):

    if not isinstance(collapses, list):
        raise WaybackError("collapses must be a list.")

    if len(collapses) == 0:
        return

    for collapse in collapses:
        try:
            match = re.search(
                r"(urlkey|timestamp|original|mimetype|statuscode|digest|length)(:?[0-9]{1,99})?",
                collapse,
            )
            field = match.group(1)

            N = None
            if 2 == len(match.groups()):
                N = match.group(2)

            if N:
                if not (field + N == collapse):
                    raise Exception
            else:
                if not (field == collapse):
                    raise Exception

        except Exception:
            exc_message = "collapse argument '{collapse}' is not following the cdx collapse syntax.".format(
                collapse=collapse
            )
            raise WaybackError(exc_message)


def _check_filters(filters):
    if not isinstance(filters, list):
        raise WaybackError("filters must be a list.")

    # [!]field:regex
    for _filter in filters:
        try:
            match = re.search(
                r"(\!?(?:urlkey|timestamp|original|mimetype|statuscode|digest|length)):(.*)",
                _filter,
            )

            key = match.group(1)
            val = match.group(2)

        except Exception:
            exc_message = (
                "Filter '{_filter}' not following the cdx filter syntax.".format(
                    _filter=_filter
                )
            )
            raise WaybackError(exc_message)


def _cleaned_url(url):
    return str(url).strip().replace(" ", "%20")


def _url_check(url):
    """
    Check for common URL problems.
    What we are checking:
    1) '.' in self.url, no url that ain't '.' in it.

    If you known any others, please create a PR on the github repo.
    """

    if "." not in url:
        exc_message = "'{url}' is not a vaild URL.".format(url=url)
        raise URLError(exc_message)


def _full_url(endpoint, params):
    full_url = endpoint
    if params:
        full_url = endpoint if endpoint.endswith("?") else (endpoint + "?")
        for key, val in params.items():
            key = "filter" if key.startswith("filter") else key
            key = "collapse" if key.startswith("collapse") else key
            amp = "" if full_url.endswith("?") else "&"
            full_url = (
                full_url + amp + "{key}={val}".format(key=key, val=quote(str(val)))
            )
    return full_url


def _get_total_pages(url, user_agent):
    """
    If showNumPages is passed in cdx API, it returns
    'number of archive pages'and each page has many archives.

    This func returns number of pages of archives (type int).
    """
    total_pages_url = (
        "https://web.archive.org/cdx/search/cdx?url={url}&showNumPages=true".format(
            url=url
        )
    )
    headers = {"User-Agent": user_agent}
    return int((_get_response(total_pages_url, headers=headers).text).strip())


def _archive_url_parser(header, url, latest_version=__version__, instance=None):
    """
    The wayback machine's save API doesn't
    return JSON response, we are required
    to read the header of the API response
    and look for the archive URL.

    This method has some regexen (or regexes)
    that search for archive url in header.

    This method is used when you try to
    save a webpage on wayback machine.

    Two cases are possible:
    1) Either we find the archive url in
       the header.

    2) Or we didn't find the archive url in
       API header.

    If we found the archive URL we return it.

    Return format:

    web.archive.org/web/<TIMESTAMP>/<URL>

    And if we couldn't find it, we raise
    WaybackError with an error message.
    """

    if "save redirected" in header and instance:
        time.sleep(60)  # makeup for archive time

        now = datetime.utcnow().timetuple()
        timestamp = _wayback_timestamp(
            year=now.tm_year,
            month=now.tm_mon,
            day=now.tm_mday,
            hour=now.tm_hour,
            minute=now.tm_min,
        )

        return_str = "web.archive.org/web/{timestamp}/{url}".format(
            timestamp=timestamp, url=url
        )
        url = "https://" + return_str

        headers = {"User-Agent": instance.user_agent}

        res = _get_response(url, headers=headers)

        if res.status_code < 400:
            return "web.archive.org/web/{timestamp}/{url}".format(
                timestamp=timestamp, url=url
            )

    # Regex1
    m = re.search(r"Content-Location: (/web/[0-9]{14}/.*)", str(header))
    if m:
        return "web.archive.org" + m.group(1)

    # Regex2
    m = re.search(
        r"rel=\"memento.*?(web\.archive\.org/web/[0-9]{14}/.*?)>", str(header)
    )
    if m:
        return m.group(1)

    # Regex3
    m = re.search(r"X-Cache-Key:\shttps(.*)[A-Z]{2}", str(header))
    if m:
        return m.group(1)

    if instance:
        newest_archive = None
        try:
            newest_archive = instance.newest()
        except WaybackError:
            pass  # We don't care as this is a save request

        if newest_archive:
            minutes_old = (
                datetime.utcnow() - newest_archive.timestamp
            ).total_seconds() / 60.0

            if minutes_old <= 30:
                archive_url = newest_archive.archive_url
                m = re.search(r"web\.archive\.org/web/[0-9]{14}/.*", archive_url)
                if m:
                    instance.cached_save = True
                    return m.group(0)

    if __version__ == latest_version:
        exc_message = (
            "No archive URL found in the API response. "
            "If '{url}' can be accessed via your web browser then either "
            "Wayback Machine is malfunctioning or it refused to archive your URL."
            "\nHeader:\n{header}".format(url=url, header=header)
        )
    else:
        exc_message = (
            "No archive URL found in the API response. "
            "If '{url}' can be accessed via your web browser then either "
            "this version of waybackpy ({version}) is out of date or WayBack "
            "Machine is malfunctioning. Visit 'https://github.com/akamhy/waybackpy' "
            "for the latest version of waybackpy.\nHeader:\n{header}".format(
                url=url, version=__version__, header=header
            )
        )

    raise WaybackError(exc_message)


def _wayback_timestamp(**kwargs):
    """
    Wayback Machine archive URLs
    have a timestamp in them.

    The standard archive URL format is
    https://web.archive.org/web/20191214041711/https://www.youtube.com

    If we break it down in three parts:
    1 ) The start (https://web.archive.org/web/)
    2 ) timestamp (20191214041711)
    3 ) https://www.youtube.com, the original URL

    The near method takes year, month, day, hour and minute
    as Arguments, their type is int.

    This method takes those integers and converts it to
    wayback machine timestamp and returns it.

    Return format is string.
    """

    return "".join(
        str(kwargs[key]).zfill(2) for key in ["year", "month", "day", "hour", "minute"]
    )


def _get_response(
    endpoint,
    params=None,
    headers=None,
    return_full_url=False,
    retries=5,
    backoff_factor=0.5,
    no_raise_on_redirects=False,
):
    """
    This function is used make get request.
    We use the requests package to make the
    requests.


    We try five times and if it fails it raises
    WaybackError exception.

    You can handles WaybackError by importing:
    from waybackpy.exceptions import WaybackError

    try:
        ...
    except WaybackError as e:
        # handle it
    """

    # From https://stackoverflow.com/a/35504626
    # By https://stackoverflow.com/users/401467/datashaman

    s = requests.Session()

    retries = Retry(
        total=retries,
        backoff_factor=backoff_factor,
        status_forcelist=[500, 502, 503, 504],
    )

    s.mount("https://", HTTPAdapter(max_retries=retries))

    url = _full_url(endpoint, params)

    try:
        if not return_full_url:
            return s.get(url, headers=headers)
        return (url, s.get(url, headers=headers))
    except Exception as e:
        reason = str(e)
        if no_raise_on_redirects:
            if "Exceeded 30 redirects" in reason:
                return
        exc_message = "Error while retrieving {url}.\n{reason}".format(
            url=url, reason=reason
        )
        exc = WaybackError(exc_message)
        exc.__cause__ = e
        raise exc
