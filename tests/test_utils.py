import pytest
import json

from waybackpy.utils import (
    _cleaned_url,
    _url_check,
    _full_url,
    URLError,
    WaybackError,
    _get_total_pages,
    _archive_url_parser,
    _wayback_timestamp,
    _get_response,
    _check_match_type,
    _check_collapses,
    _check_filters,
    _ts,
)


def test_ts():
    timestamp = True
    data = {}
    assert _ts(timestamp, data)

    data = """
    {"archived_snapshots": {"closest": {"timestamp": "20210109155628", "available": true, "status": "200", "url": "http://web.archive.org/web/20210109155628/https://www.google.com/"}}, "url": "https://www.google.com/"}
    """
    data = json.loads(data)
    assert data["archived_snapshots"]["closest"]["timestamp"] == "20210109155628"


def test_check_filters():
    filters = []
    _check_filters(filters)

    filters = ["statuscode:200", "timestamp:20215678901234", "original:https://url.com"]
    _check_filters(filters)

    with pytest.raises(WaybackError):
        _check_filters("not-list")


def test_check_collapses():
    collapses = []
    _check_collapses(collapses)

    collapses = ["timestamp:10"]
    _check_collapses(collapses)

    collapses = ["urlkey"]
    _check_collapses(collapses)

    collapses = "urlkey"  # NOT LIST
    with pytest.raises(WaybackError):
        _check_collapses(collapses)

    collapses = ["also illegal collapse"]
    with pytest.raises(WaybackError):
        _check_collapses(collapses)


def test_check_match_type():
    assert None == _check_match_type(None, "url")
    match_type = "exact"
    url = "test_url"
    assert None == _check_match_type(match_type, url)

    url = "has * in it"
    with pytest.raises(WaybackError):
        _check_match_type("domain", url)

    with pytest.raises(WaybackError):
        _check_match_type("not a valid type", "url")


def test_cleaned_url():
    test_url = " https://en.wikipedia.org/wiki/Network security "
    answer = "https://en.wikipedia.org/wiki/Network%20security"
    assert answer == _cleaned_url(test_url)


def test_url_check():
    good_url = "https://akamhy.github.io"
    assert None == _url_check(good_url)

    bad_url = "https://github-com"
    with pytest.raises(URLError):
        _url_check(bad_url)


def test_full_url():
    params = {}
    endpoint = "https://web.archive.org/cdx/search/cdx"
    assert endpoint == _full_url(endpoint, params)

    params = {"a": "1"}
    assert "https://web.archive.org/cdx/search/cdx?a=1" == _full_url(endpoint, params)
    assert "https://web.archive.org/cdx/search/cdx?a=1" == _full_url(
        endpoint + "?", params
    )

    params["b"] = 2
    assert "https://web.archive.org/cdx/search/cdx?a=1&b=2" == _full_url(
        endpoint + "?", params
    )

    params["c"] = "foo bar"
    assert "https://web.archive.org/cdx/search/cdx?a=1&b=2&c=foo%20bar" == _full_url(
        endpoint + "?", params
    )


def test_get_total_pages():
    user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko"
    url = "github.com*"
    assert 212890 <= _get_total_pages(url, user_agent)

    url = "https://zenodo.org/record/4416138"
    assert 2 >= _get_total_pages(url, user_agent)


def test_archive_url_parser():
    perfect_header = """
    {'Server': 'nginx/1.15.8', 'Date': 'Sat, 02 Jan 2021 09:40:25 GMT', 'Content-Type': 'text/html; charset=UTF-8', 'Transfer-Encoding': 'chunked', 'Connection': 'keep-alive', 'X-Archive-Orig-Server': 'nginx', 'X-Archive-Orig-Date': 'Sat, 02 Jan 2021 09:40:09 GMT', 'X-Archive-Orig-Transfer-Encoding': 'chunked', 'X-Archive-Orig-Connection': 'keep-alive', 'X-Archive-Orig-Vary': 'Accept-Encoding', 'X-Archive-Orig-Last-Modified': 'Fri, 01 Jan 2021 12:19:00 GMT', 'X-Archive-Orig-Strict-Transport-Security': 'max-age=31536000, max-age=0;', 'X-Archive-Guessed-Content-Type': 'text/html', 'X-Archive-Guessed-Charset': 'utf-8', 'Memento-Datetime': 'Sat, 02 Jan 2021 09:40:09 GMT', 'Link': '<https://www.scribbr.com/citing-sources/et-al/>; rel="original", <https://web.archive.org/web/timemap/link/https://www.scribbr.com/citing-sources/et-al/>; rel="timemap"; type="application/link-format", <https://web.archive.org/web/https://www.scribbr.com/citing-sources/et-al/>; rel="timegate", <https://web.archive.org/web/20200601082911/https://www.scribbr.com/citing-sources/et-al/>; rel="first memento"; datetime="Mon, 01 Jun 2020 08:29:11 GMT", <https://web.archive.org/web/20201126185327/https://www.scribbr.com/citing-sources/et-al/>; rel="prev memento"; datetime="Thu, 26 Nov 2020 18:53:27 GMT", <https://web.archive.org/web/20210102094009/https://www.scribbr.com/citing-sources/et-al/>; rel="memento"; datetime="Sat, 02 Jan 2021 09:40:09 GMT", <https://web.archive.org/web/20210102094009/https://www.scribbr.com/citing-sources/et-al/>; rel="last memento"; datetime="Sat, 02 Jan 2021 09:40:09 GMT"', 'Content-Security-Policy': "default-src 'self' 'unsafe-eval' 'unsafe-inline' data: blob: archive.org web.archive.org analytics.archive.org pragma.archivelab.org", 'X-Archive-Src': 'spn2-20210102092956-wwwb-spn20.us.archive.org-8001.warc.gz', 'Server-Timing': 'captures_list;dur=112.646325, exclusion.robots;dur=0.172010, exclusion.robots.policy;dur=0.158205, RedisCDXSource;dur=2.205932, esindex;dur=0.014647, LoadShardBlock;dur=82.205012, PetaboxLoader3.datanode;dur=70.750239, CDXLines.iter;dur=24.306278, load_resource;dur=26.520179', 'X-App-Server': 'wwwb-app200', 'X-ts': '200', 'X-location': 'All', 'X-Cache-Key': 'httpsweb.archive.org/web/20210102094009/https://www.scribbr.com/citing-sources/et-al/IN', 'X-RL': '0', 'X-Page-Cache': 'MISS', 'X-Archive-Screenname': '0', 'Content-Encoding': 'gzip'}
    """

    archive = _archive_url_parser(
        perfect_header, "https://www.scribbr.com/citing-sources/et-al/"
    )
    assert "web.archive.org/web/20210102094009" in archive

    header = """
    vhgvkjv
    Content-Location: /web/20201126185327/https://www.scribbr.com/citing-sources/et-al
    ghvjkbjmmcmhj
    """
    archive = _archive_url_parser(
        header, "https://www.scribbr.com/citing-sources/et-al/"
    )
    assert "20201126185327" in archive

    header = """
    hfjkfjfcjhmghmvjm
    X-Cache-Key: https://web.archive.org/web/20171128185327/https://www.scribbr.com/citing-sources/et-al/US
    yfu,u,gikgkikik
    """
    archive = _archive_url_parser(
        header, "https://www.scribbr.com/citing-sources/et-al/"
    )
    assert "20171128185327" in archive

    # The below header should result in Exception
    no_archive_header = """
    {'Server': 'nginx/1.15.8', 'Date': 'Sat, 02 Jan 2021 09:42:45 GMT', 'Content-Type': 'text/html; charset=utf-8', 'Transfer-Encoding': 'chunked', 'Connection': 'keep-alive', 'Cache-Control': 'no-cache', 'X-App-Server': 'wwwb-app52', 'X-ts': '523', 'X-RL': '0', 'X-Page-Cache': 'MISS', 'X-Archive-Screenname': '0'}
    """

    with pytest.raises(WaybackError):
        _archive_url_parser(
            no_archive_header, "https://www.scribbr.com/citing-sources/et-al/"
        )


def test_wayback_timestamp():
    ts = _wayback_timestamp(year=2020, month=1, day=2, hour=3, minute=4)
    assert "202001020304" in str(ts)


def test_get_response():
    endpoint = "https://www.google.com"
    user_agent = (
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0"
    )
    headers = {"User-Agent": "%s" % user_agent}
    response = _get_response(endpoint, params=None, headers=headers)
    assert response.status_code == 200

    endpoint = "http/wwhfhfvhvjhmom"
    with pytest.raises(WaybackError):
        _get_response(endpoint, params=None, headers=headers)

    endpoint = "https://akamhy.github.io"
    url, response = _get_response(
        endpoint, params=None, headers=headers, return_full_url=True
    )
    assert endpoint == url
