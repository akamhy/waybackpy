from typing import Any, Dict, List

import pytest

from waybackpy.cdx_utils import (
    check_collapses,
    check_filters,
    check_match_type,
    check_sort,
    full_url,
    get_response,
    get_total_pages,
)
from waybackpy.exceptions import WaybackError


def test_get_total_pages() -> None:
    url = "twitter.com"
    user_agent = (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 "
        "(KHTML, like Gecko) Version/14.0.2 Safari/605.1.15"
    )
    assert get_total_pages(url=url, user_agent=user_agent) >= 56


def test_full_url() -> None:
    endpoint = "https://web.archive.org/cdx/search/cdx"
    params: Dict[str, Any] = {}
    assert endpoint == full_url(endpoint, params)

    params = {"a": "1"}
    assert full_url(endpoint, params) == "https://web.archive.org/cdx/search/cdx?a=1"
    assert (
        full_url(endpoint + "?", params) == "https://web.archive.org/cdx/search/cdx?a=1"
    )

    params["b"] = 2
    assert (
        full_url(endpoint + "?", params)
        == "https://web.archive.org/cdx/search/cdx?a=1&b=2"
    )

    params["c"] = "foo bar"
    assert (
        full_url(endpoint + "?", params)
        == "https://web.archive.org/cdx/search/cdx?a=1&b=2&c=foo%20bar"
    )


def test_get_response() -> None:
    url = "https://github.com"
    user_agent = (
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0"
    )
    headers = {"User-Agent": str(user_agent)}
    response = get_response(url, headers=headers)
    assert not isinstance(response, Exception) and response.status_code == 200


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


def test_check_sort() -> None:
    assert check_sort("default")
    assert check_sort("closest")
    assert check_sort("reverse")

    with pytest.raises(WaybackError):
        assert check_sort("random crap")
