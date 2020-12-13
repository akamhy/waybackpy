# -*- coding: utf-8 -*-
import sys
import pytest
import random
import requests
sys.path.append("..")

import waybackpy.wrapper as waybackpy  # noqa: E402
from urllib.request import Request



user_agent = "Mozilla/5.0 (Windows NT 6.2; rv:20.0) Gecko/20121202 Firefox/20.0"


def test_clean_url():
    test_url = " https://en.wikipedia.org/wiki/Network security "
    answer = "https://en.wikipedia.org/wiki/Network_security"
    target = waybackpy.Url(test_url, user_agent)
    test_result = target._clean_url()
    assert answer == test_result

def test_dunders():
    url = "https://en.wikipedia.org/wiki/Network_security"
    user_agent = "UA"
    target = waybackpy.Url(url, user_agent)
    assert "waybackpy.Url(url=%s, user_agent=%s)" % (url, user_agent) == repr(target)
    assert "en.wikipedia.org" in str(target)

def test_archive_url_parser():
    endpoint = "https://amazon.com"
    user_agent = "Mozilla/5.0 (Windows NT 6.2; rv:20.0) Gecko/20121202 Firefox/20.0"
    headers = {"User-Agent": "%s" % user_agent}
    response = waybackpy._get_response(endpoint, params=None, headers=headers)
    header = response.headers
    with pytest.raises(Exception):
        waybackpy._archive_url_parser(header)

def test_url_check():
    broken_url = "http://wwwgooglecom/"
    with pytest.raises(Exception):
        waybackpy.Url(broken_url, user_agent)


def test_save():
    # Test for urls that exist and can be archived.

    url_list = [
        "en.wikipedia.org",
        "www.wikidata.org",
        "commons.wikimedia.org",
        "www.wiktionary.org",
        "www.w3schools.com",
        "www.ibm.com",
    ]
    x = random.randint(0, len(url_list) - 1)
    url1 = url_list[x]
    target = waybackpy.Url(
        url1,
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/36.0.1944.0 Safari/537.36",
    )
    archived_url1 = str(target.save())
    assert url1 in archived_url1



    # Test for urls that are incorrect.
    with pytest.raises(Exception):
        url2 = "ha ha ha ha"
        waybackpy.Url(url2, user_agent)
    url3 = "http://www.archive.is/faq.html"

    with pytest.raises(Exception):
        target = waybackpy.Url(
            url3,
            "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) "
            "AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 "
            "Safari/533.20.27",
        )
        target.save()


def test_near():
    url = "google.com"
    target = waybackpy.Url(
        url,
        "Mozilla/5.0 (Windows; U; Windows NT 6.0; de-DE) AppleWebKit/533.20.25 "
        "(KHTML, like Gecko) Version/5.0.3 Safari/533.19.4",
    )
    archive_near_year = target.near(year=2010)
    assert "2010" in str(archive_near_year)


    archive_near_month_year = str(target.near(year=2015, month=2))
    assert (
        ("201502" in archive_near_month_year)
        or ("201501" in archive_near_month_year)
        or ("201503" in archive_near_month_year)
    )

    target = waybackpy.Url(
        "www.python.org",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246",
    )
    archive_near_hour_day_month_year = str(target.near(
        year=2008, month=5, day=9, hour=15
    ))
    assert (
        ("2008050915" in archive_near_hour_day_month_year)
        or ("2008050914" in archive_near_hour_day_month_year)
        or ("2008050913" in archive_near_hour_day_month_year)
    )

    with pytest.raises(Exception):
        NeverArchivedUrl = (
            "https://ee_3n.wrihkeipef4edia.org/rwti5r_ki/Nertr6w_rork_rse7c_urity"
        )
        target = waybackpy.Url(NeverArchivedUrl, user_agent)
        target.near(year=2010)



def test_oldest():
    url = "github.com/akamhy/waybackpy"
    target = waybackpy.Url(url, user_agent)
    assert "20200504141153" in str(target.oldest())

def test_json():
    url = "github.com/akamhy/waybackpy"
    target = waybackpy.Url(url, user_agent)
    assert "archived_snapshots" in str(target.JSON)

def test_archive_url():
    url = "github.com/akamhy/waybackpy"
    target = waybackpy.Url(url, user_agent)
    assert "github.com/akamhy" in str(target.archive_url)

def test_newest():
    url = "github.com/akamhy/waybackpy"
    target = waybackpy.Url(url, user_agent)
    assert url in str(target.newest())


def test_get():
    target = waybackpy.Url("google.com", user_agent)
    assert "Welcome to Google" in target.get(target.oldest())



def test_wayback_timestamp():
    ts = waybackpy._wayback_timestamp(
        year=2020, month=1, day=2, hour=3, minute=4
    )
    assert "202001020304" in str(ts)


def test_get_response():
    endpoint = "https://www.google.com"
    user_agent = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0"
    headers = {"User-Agent": "%s" % user_agent}
    response = waybackpy._get_response(endpoint, params=None, headers=headers)
    assert response.status_code == 200


def test_total_archives():

    target = waybackpy.Url(" https://google.com ", user_agent)
    assert target.total_archives() > 500000

    target = waybackpy.Url(
        " https://gaha.e4i3n.m5iai3kip6ied.cima/gahh2718gs/ahkst63t7gad8 ", user_agent
    )
    assert target.total_archives() == 0

def test_known_urls():

    target = waybackpy.Url("akamhy.github.io", user_agent)
    assert len(target.known_urls(alive=True, subdomain=True)) > 2

    target = waybackpy.Url("akamhy.github.io", user_agent)
    assert len(target.known_urls()) > 3
