import re
from typing import Any, Dict, List, Optional, Union
from urllib.parse import quote

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .exceptions import WaybackError
from .utils import DEFAULT_USER_AGENT


def get_total_pages(url: str, user_agent: str = DEFAULT_USER_AGENT) -> int:
    endpoint = "https://web.archive.org/cdx/search/cdx?"
    payload = {"showNumPages": "true", "url": str(url)}
    headers = {"User-Agent": user_agent}
    request_url = full_url(endpoint, params=payload)
    response = get_response(request_url, headers=headers)
    if isinstance(response, requests.Response):
        return int(response.text.strip())
    else:
        raise response


def full_url(endpoint: str, params: Dict[str, Any]) -> str:
    if not params:
        return endpoint
    full_url = endpoint if endpoint.endswith("?") else (endpoint + "?")
    for key, val in params.items():
        key = "filter" if key.startswith("filter") else key
        key = "collapse" if key.startswith("collapse") else key
        amp = "" if full_url.endswith("?") else "&"
        full_url = (
            full_url + amp + "{key}={val}".format(key=key, val=quote(str(val), safe=""))
        )
    return full_url


def get_response(
    url: str,
    headers: Optional[Dict[str, str]] = None,
    retries: int = 5,
    backoff_factor: float = 0.5,
    # no_raise_on_redirects=False,
) -> Union[requests.Response, Exception]:
    session = requests.Session()
    retries_ = Retry(
        total=retries,
        backoff_factor=backoff_factor,
        status_forcelist=[500, 502, 503, 504],
    )
    session.mount("https://", HTTPAdapter(max_retries=retries_))

    try:
        response = session.get(url, headers=headers)
        session.close()
        return response
    except Exception as e:
        reason = str(e)
        exc_message = "Error while retrieving {url}.\n{reason}".format(
            url=url, reason=reason
        )
        exc = WaybackError(exc_message)
        exc.__cause__ = e
        raise exc


def check_filters(filters: List[str]) -> None:
    if not isinstance(filters, list):
        raise WaybackError("filters must be a list.")

    # [!]field:regex
    for _filter in filters:
        match = re.search(
            r"(\!?(?:urlkey|timestamp|original|mimetype|statuscode|digest|length)):(.*)",
            _filter,
        )

        if match is None or len(match.groups()) != 2:

            exc_message = (
                "Filter '{_filter}' is not following the cdx filter syntax.".format(
                    _filter=_filter
                )
            )
            raise WaybackError(exc_message)


def check_collapses(collapses: List[str]) -> bool:
    if not isinstance(collapses, list):
        raise WaybackError("collapses must be a list.")
    elif len(collapses) == 0:
        return True

    for collapse in collapses:
        match = re.search(
            r"(urlkey|timestamp|original|mimetype|statuscode|digest|length)(:?[0-9]{1,99})?",
            collapse,
        )
        if match is None or len(match.groups()) != 2:
            exc_message = "collapse argument '{collapse}' is not following the cdx collapse syntax.".format(
                collapse=collapse
            )
            raise WaybackError(exc_message)
    else:
        return True


def check_match_type(match_type: Optional[str], url: str) -> bool:
    legal_match_type = ["exact", "prefix", "host", "domain"]
    if not match_type:
        return True
    elif "*" in url:
        raise WaybackError(
            "Can not use wildcard in the URL along with the match_type arguments."
        )
    elif match_type not in legal_match_type:
        exc_message = "{match_type} is not an allowed match type.\nUse one from 'exact', 'prefix', 'host' or 'domain'".format(
            match_type=match_type
        )
        raise WaybackError(exc_message)
    else:
        return True
