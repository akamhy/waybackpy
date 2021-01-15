import sys
import pytest
import random
import requests
from datetime import datetime

from waybackpy.wrapper import Url, Cdx


user_agent = "Mozilla/5.0 (Windows NT 6.2; rv:20.0) Gecko/20121202 Firefox/20.0"


def test_url_check():
    """No API Use"""
    broken_url = "http://wwwgooglecom/"
    with pytest.raises(Exception):
        Url(broken_url, user_agent)


def test_save():
    # Test for urls that exist and can be archived.

    url_list = [
        "en.wikipedia.org",
        "akamhy.github.io",
        "www.wiktionary.org",
        "www.w3schools.com",
        "youtube.com",
    ]
    x = random.randint(0, len(url_list) - 1)
    url1 = url_list[x]
    target = Url(
        url1,
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/36.0.1944.0 Safari/537.36",
    )
    archived_url1 = str(target.save())
    assert url1 in archived_url1

    # Test for urls that are incorrect.
    with pytest.raises(Exception):
        url2 = "ha ha ha ha"
        Url(url2, user_agent)


def test_near():
    url = "google.com"
    target = Url(
        url,
        "Mozilla/5.0 (Windows; U; Windows NT 6.0; de-DE) AppleWebKit/533.20.25 "
        "(KHTML, like Gecko) Version/5.0.3 Safari/533.19.4",
    )
    archive_near_year = target.near(year=2010)
    assert "2010" in str(archive_near_year.timestamp)

    archive_near_month_year = str(target.near(year=2015, month=2).timestamp)
    assert (
        ("2015-02" in archive_near_month_year)
        or ("2015-01" in archive_near_month_year)
        or ("2015-03" in archive_near_month_year)
    )

    target = Url(
        "www.python.org",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246",
    )
    archive_near_hour_day_month_year = str(
        target.near(year=2008, month=5, day=9, hour=15)
    )
    assert (
        ("2008050915" in archive_near_hour_day_month_year)
        or ("2008050914" in archive_near_hour_day_month_year)
        or ("2008050913" in archive_near_hour_day_month_year)
    )

    with pytest.raises(Exception):
        NeverArchivedUrl = (
            "https://ee_3n.wrihkeipef4edia.org/rwti5r_ki/Nertr6w_rork_rse7c_urity"
        )
        target = Url(NeverArchivedUrl, user_agent)
        target.near(year=2010)


def test_oldest():
    url = "github.com/akamhy/waybackpy"
    target = Url(url, user_agent)
    o = target.oldest()
    assert "20200504141153" in str(o)
    assert "2020-05-04" in str(o._timestamp)


def test_json():
    url = "github.com/akamhy/waybackpy"
    target = Url(url, user_agent)
    assert "archived_snapshots" in str(target.JSON)


def test_archive_url():
    url = "github.com/akamhy/waybackpy"
    target = Url(url, user_agent)
    assert "github.com/akamhy" in str(target.archive_url)


def test_newest():
    url = "github.com/akamhy/waybackpy"
    target = Url(url, user_agent)
    assert url in str(target.newest())


def test_get():
    target = Url("google.com", user_agent)
    assert "Welcome to Google" in target.get(target.oldest())


def test_total_archives():
    user_agent = (
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0"
    )
    target = Url(" https://outlook.com ", user_agent)
    assert target.total_archives() > 80000

    target = Url(
        " https://gaha.e4i3n.m5iai3kip6ied.cima/gahh2718gs/ahkst63t7gad8 ", user_agent
    )
    assert target.total_archives() == 0


def test_known_urls():

    target = Url("akamhy.github.io", user_agent)
    assert len(target.known_urls()) > 3
