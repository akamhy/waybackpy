from typing import Any, Dict, List

import pytest

from waybackpy.cdx_utils import (
    check_collapses,
    check_filters,
    check_match_type,
    full_url,
    get_response,
    get_total_pages,
)
from waybackpy.exceptions import WaybackError


def test_get_total_pages() -> None:
    url = "twitter.com"
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 Safari/605.1.15"
    assert get_total_pages(url=url, user_agent=user_agent) >= 56


def test_full_url() -> None:
    endpoint = "https://web.archive.org/cdx/search/cdx"
    params: Dict[str, Any] = {}
    assert endpoint == full_url(endpoint, params)

    params = {"a": "1"}
    assert "https://web.archive.org/cdx/search/cdx?a=1" == full_url(endpoint, params)
    assert "https://web.archive.org/cdx/search/cdx?a=1" == full_url(
        endpoint + "?", params
    )

    params["b"] = 2
    assert "https://web.archive.org/cdx/search/cdx?a=1&b=2" == full_url(
        endpoint + "?", params
    )

    params["c"] = "foo bar"
    assert "https://web.archive.org/cdx/search/cdx?a=1&b=2&c=foo%20bar" == full_url(
        endpoint + "?", params
    )


def test_get_response() -> None:
    url = "https://github.com"
    user_agent = (
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0"
    )
    headers = {"User-Agent": "%s" % user_agent}
    response = get_response(url, headers=headers)
    assert not isinstance(response, Exception) and response.status_code == 200

    url = "http/wwhfhfvhvjhmom"
    with pytest.raises(WaybackError):
        get_response(url, headers=headers)


def test_check_filters() -> None:
    filters: List[str] = []
    check_filters(filters)

    filters = ["statuscode:200", "timestamp:20215678901234", "original:https://url.com"]
    check_filters(filters)

    with pytest.raises(WaybackError):
        check_filters("not-list")  # type: ignore[arg-type]

    with pytest.raises(WaybackError):
        check_filters(["invalid"])


def test_check_collapses() -> None:
    collapses: List[str] = []
    check_collapses(collapses)

    collapses = ["timestamp:10"]
    check_collapses(collapses)

    collapses = ["urlkey"]
    check_collapses(collapses)

    collapses = "urlkey"  # type: ignore[assignment]
    with pytest.raises(WaybackError):
        check_collapses(collapses)

    collapses = ["also illegal collapse"]
    with pytest.raises(WaybackError):
        check_collapses(collapses)


def test_check_match_type() -> None:
    assert check_match_type(None, "url")
    match_type = "exact"
    url = "test_url"
    assert check_match_type(match_type, url)

    url = "has * in it"
    with pytest.raises(WaybackError):
        check_match_type("domain", url)

    with pytest.raises(WaybackError):
        check_match_type("not a valid type", "url")
