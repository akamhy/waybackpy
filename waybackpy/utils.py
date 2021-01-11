import re
import requests
from .exceptions import WaybackError, URLError
from datetime import datetime

from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from .__version__ import __version__

quote = requests.utils.quote
default_user_agent = "waybackpy python package - https://github.com/akamhy/waybackpy"


def _unix_ts_to_wayback_ts(unix_ts):
    return datetime.utcfromtimestamp(int(unix_ts)).strftime("%Y%m%d%H%M%S")


def _add_payload(self, payload):
    if self.start_timestamp:
        payload["from"] = self.start_timestamp

    if self.end_timestamp:
        payload["to"] = self.end_timestamp

    if self.gzip != True:
        payload["gzip"] = "false"

    if self.match_type:
        payload["matchType"] = self.match_type

    if self.filters and len(self.filters) > 0:
        for i, f in enumerate(self.filters):
            payload["filter" + str(i)] = f

    if self.collapses and len(self.collapses) > 0:
        for i, f in enumerate(self.collapses):
            payload["collapse" + str(i)] = f

    payload["url"] = self.url


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
        raise WaybackError(
            "%s is not an allowed match type.\nUse one from 'exact', 'prefix', 'host' or 'domain'"
            % match_type
        )


def _check_collapses(collapses):

    if not isinstance(collapses, list):
        raise WaybackError("collapses must be a list.")

    if len(collapses) == 0:
        return

    for c in collapses:
        try:
            match = re.search(
                r"(urlkey|timestamp|original|mimetype|statuscode|digest|length)(:?[0-9]{1,99})?",
                c,
            )
            field = match.group(1)

            N = None
            if 2 == len(match.groups()):
                N = match.group(2)

            if N:
                if not (field + N == c):
                    raise Exception
            else:
                if not (field == c):
                    raise Exception

        except Exception:
            e = "collapse argument '%s' is not following the cdx collapse syntax." % c
            raise WaybackError(e)


def _check_filters(filters):
    if not isinstance(filters, list):
        raise WaybackError("filters must be a list.")

    # [!]field:regex
    for f in filters:
        try:
            match = re.search(
                r"(\!?(?:urlkey|timestamp|original|mimetype|statuscode|digest|length)):(.*)",
                f,
            )

            key = match.group(1)
            val = match.group(2)

        except Exception:
            e = "Filter '%s' not following the cdx filter syntax." % f
            raise WaybackError(e)


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
        raise URLError("'%s' is not a vaild URL." % url)


def _full_url(endpoint, params):
    full_url = endpoint
    if params:
        full_url = endpoint if endpoint.endswith("?") else (endpoint + "?")
        for key, val in params.items():
            key = "filter" if key.startswith("filter") else key
            key = "collapse" if key.startswith("collapse") else key
            amp = "" if full_url.endswith("?") else "&"
            full_url = full_url + amp + "%s=%s" % (key, quote(str(val)))
    return full_url


def _get_total_pages(url, user_agent):
    """
    If showNumPages is passed in cdx API, it returns
    'number of archive pages'and each page has many archives.

    This func returns number of pages of archives (type int).
    """
    total_pages_url = (
        "https://web.archive.org/cdx/search/cdx?url=%s&showNumPages=true" % url
    )
    headers = {"User-Agent": user_agent}
    return int((_get_response(total_pages_url, headers=headers).text).strip())


def _archive_url_parser(header, url):
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

    And if we couldn't find it, we raise
    WaybackError with an error message.
    """

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

    raise WaybackError(
        "No archive URL found in the API response. "
        "If '%s' can be accessed via your web browser then either "
        "this version of waybackpy (%s) is out of date or WayBack Machine is malfunctioning. Visit "
        "'https://github.com/akamhy/waybackpy' for the latest version "
        "of waybackpy.\nHeader:\n%s" % (url, __version__, str(header))
    )


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
    endpoint, params=None, headers=None, retries=5, return_full_url=False
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
        total=retries, backoff_factor=0.5, status_forcelist=[500, 502, 503, 504]
    )
    s.mount("https://", HTTPAdapter(max_retries=retries))
    url = _full_url(endpoint, params)
    try:
        if not return_full_url:
            return s.get(url, headers=headers)
        return (url, s.get(url, headers=headers))
    except Exception as e:
        exc = WaybackError("Error while retrieving %s" % url)
        exc.__cause__ = e
        raise exc
