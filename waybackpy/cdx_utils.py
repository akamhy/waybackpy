"""
Utility functions required for accessing the CDX server API.

These are here in this module so that we don’t make any module too
long.
"""

import re
from typing import Any, Dict, List, Optional, Union
from urllib.parse import quote

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .exceptions import BlockedSiteError, WaybackError
from .utils import DEFAULT_USER_AGENT


def get_total_pages(url: str, user_agent: str = DEFAULT_USER_AGENT) -> int:
    """
    When using the pagination use adding showNumPages=true to the request
    URL makes the CDX server return an integer which is the number of pages
    of CDX pages available for us to query using the pagination API.
    """
    endpoint = "https://web.archive.org/cdx/search/cdx?"
    payload = {"showNumPages": "true", "url": str(url)}
    headers = {"User-Agent": user_agent}
    request_url = full_url(endpoint, params=payload)
    response = get_response(request_url, headers=headers)
    check_for_blocked_site(response, url)
    if isinstance(response, requests.Response):
        return int(response.text.strip())
    raise response


def check_for_blocked_site(
    response: Union[requests.Response, Exception], url: Optional[str] = None
) -> None:
    """
    Checks that the URL can be archived by wayback machine or not.
    robots.txt policy of the site may prevent the wayback machine.
    """
    # see https://github.com/akamhy/waybackpy/issues/157

    # the following if block is to make mypy happy.
    if isinstance(response, Exception):
        raise response

    if not url:
        url = "The requested content"
    if (
        "org.archive.util.io.RuntimeIOException: "
        + "org.archive.wayback.exception.AdministrativeAccessControlException: "
        + "Blocked Site Error"
        in response.text.strip()
    ):
        raise BlockedSiteError(
            f"{url} is excluded from Wayback Machine by the site's robots.txt policy."
        )


def full_url(endpoint: str, params: Dict[str, Any]) -> str:
    """
    As the function's name already implies that it returns
    full URL, but why we need a function for generating full URL?
    The CDX server can support multiple arguments for parameters
    such as filter and collapse and this function adds them without
    overwriting earlier added arguments.
    """
    if not params:
        return endpoint
    _full_url = endpoint if endpoint.endswith("?") else (endpoint + "?")

    for key, val in params.items():
        key = "filter" if key.startswith("filter") else key
        key = "collapse" if key.startswith("collapse") else key
        amp = "" if _full_url.endswith("?") else "&"
        val = quote(str(val), safe="")
        _full_url += f"{amp}{key}={val}"

    return _full_url


def get_response(
    url: str,
    headers: Optional[Dict[str, str]] = None,
    retries: int = 5,
    backoff_factor: float = 0.5,
) -> Union[requests.Response, Exception]:
    """
    Makes get request to the CDX server and returns the response.
    """
    session = requests.Session()

    retries_ = Retry(
        total=retries,
        backoff_factor=backoff_factor,
        status_forcelist=[500, 502, 503, 504],
    )

    session.mount("https://", HTTPAdapter(max_retries=retries_))
    response = session.get(url, headers=headers)
    session.close()
    check_for_blocked_site(response)
    return response


def check_filters(filters: List[str]) -> None:
    """
    Check that the filter arguments passed by the end-user are valid.
    If not valid then raise WaybackError.
    """
    if not isinstance(filters, list):
        raise WaybackError("filters must be a list.")

    # [!]field:regex
    for _filter in filters:
        match = re.search(
            r"(\!?(?:urlkey|timestamp|original|mimetype|statuscode|digest|length)):"
            r"(.*)",
            _filter,
        )

        if match is None or len(match.groups()) != 2:

            exc_message = f"Filter '{_filter}' is not following the cdx filter syntax."
            raise WaybackError(exc_message)


def check_collapses(collapses: List[str]) -> bool:
    """
    Check that the collapse arguments passed by the end-user are valid.
    If not valid then raise WaybackError.
    """
    if not isinstance(collapses, list):
        raise WaybackError("collapses must be a list.")

    if len(collapses) == 0:
        return True

    for collapse in collapses:
        match = re.search(
            r"(urlkey|timestamp|original|mimetype|statuscode|digest|length)"
            r"(:?[0-9]{1,99})?",
            collapse,
        )
        if match is None or len(match.groups()) != 2:
            exc_message = (
                f"collapse argument '{collapse}' "
                "is not following the cdx collapse syntax."
            )
            raise WaybackError(exc_message)

    return True


def check_match_type(match_type: Optional[str], url: str) -> bool:
    """
    Check that the match_type argument passed by the end-user is valid.
    If not valid then raise WaybackError.
    """
    legal_match_type = ["exact", "prefix", "host", "domain"]

    if not match_type:
        return True

    if "*" in url:
        raise WaybackError(
            "Can not use wildcard in the URL along with the match_type arguments."
        )

    if match_type not in legal_match_type:
        exc_message = (
            f"{match_type} is not an allowed match type.\n"
            "Use one from 'exact', 'prefix', 'host' or 'domain'"
        )
        raise WaybackError(exc_message)

    return True


def check_sort(sort: Optional[str]) -> bool:
    """
    Check that the sort argument passed by the end-user is valid.
    If not valid then raise WaybackError.
    """

    legal_sort = ["default", "closest", "reverse"]

    if not sort:
        return True

    if sort not in legal_sort:
        exc_message = (
            f"{sort} is not an allowed argument for sort.\n"
            "Use one from 'default', 'closest' or 'reverse'"
        )
        raise WaybackError(exc_message)

    return True
