import re
import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from .exceptions import WaybackError


def get_total_pages(url, user_agent):
    request_url = (
        "https://web.archive.org/cdx/search/cdx?url={url}&showNumPages=true".format(
            url=url
        )
    )
    headers = {"User-Agent": user_agent}
    return int((requests.get(request_url, headers=headers).text).strip())


def full_url(endpoint, params):
    if not params:
        return endpoint
    full_url = endpoint if endpoint.endswith("?") else (endpoint + "?")
    for key, val in params.items():
        key = "filter" if key.startswith("filter") else key
        key = "collapse" if key.startswith("collapse") else key
        amp = "" if full_url.endswith("?") else "&"
        full_url = (
            full_url
            + amp
            + "{key}={val}".format(key=key, val=requests.utils.quote(str(val)))
        )
    return full_url


def get_response(
    endpoint,
    params=None,
    headers=None,
    return_full_url=False,
    retries=5,
    backoff_factor=0.5,
    no_raise_on_redirects=False,
):

    s = requests.Session()

    retries = Retry(
        total=retries,
        backoff_factor=backoff_factor,
        status_forcelist=[500, 502, 503, 504],
    )

    s.mount("https://", HTTPAdapter(max_retries=retries))

    # The URL with parameters required for the get request
    url = full_url(endpoint, params)

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


def check_filters(filters):
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
                "Filter '{_filter}' is not following the cdx filter syntax.".format(
                    _filter=_filter
                )
            )
            raise WaybackError(exc_message)


def check_collapses(collapses):

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


def check_match_type(match_type, url):
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
