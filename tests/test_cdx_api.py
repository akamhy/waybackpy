import random
import string

import pytest

from waybackpy.cdx_api import WaybackMachineCDXServerAPI
from waybackpy.exceptions import NoCDXRecordFound


def rndstr(n: int) -> str:
    return "".join(
        random.choice(string.ascii_uppercase + string.digits) for _ in range(n)
    )


def test_a() -> None:
    user_agent = (
        "Mozilla/5.0 (MacBook Air; M1 Mac OS X 11_4) AppleWebKit/605.1.15 "
        "(KHTML, like Gecko) Version/14.1.1 Safari/604.1"
    )
    url = "https://twitter.com/jack"

    wayback = WaybackMachineCDXServerAPI(
        url=url,
        user_agent=user_agent,
        match_type="prefix",
        collapses=["urlkey"],
        start_timestamp="201001",
        end_timestamp="201002",
    )
    #  timeframe bound prefix matching enabled along with active urlkey based collapsing

    snapshots = wayback.snapshots()  # <class 'generator'>

    for snapshot in snapshots:
        assert snapshot.timestamp.startswith("2010")


def test_b() -> None:
    user_agent = (
        "Mozilla/5.0 (MacBook Air; M1 Mac OS X 11_4) "
        "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/604.1"
    )
    url = "https://www.google.com"

    wayback = WaybackMachineCDXServerAPI(
        url=url,
        user_agent=user_agent,
        start_timestamp="202101",
        end_timestamp="202112",
        collapses=["urlkey"],
    )
    #  timeframe bound prefix matching enabled along with active urlkey based collapsing

    snapshots = wayback.snapshots()  # <class 'generator'>

    for snapshot in snapshots:
        assert snapshot.timestamp.startswith("2021")


def test_c() -> None:
    user_agent = (
        "Mozilla/5.0 (MacBook Air; M1 Mac OS X 11_4) "
        "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/604.1"
    )
    url = "https://www.google.com"

    cdx = WaybackMachineCDXServerAPI(
        url=url,
        user_agent=user_agent,
        closest="201010101010",
        sort="closest",
        limit="1",
    )
    snapshots = cdx.snapshots()
    for snapshot in snapshots:
        archive_url = snapshot.archive_url
        timestamp = snapshot.timestamp
        break

    assert str(archive_url).find("google.com")
    assert "20101010" in timestamp


def test_d() -> None:
    user_agent = (
        "Mozilla/5.0 (MacBook Air; M1 Mac OS X 11_4) "
        "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/604.1"
    )

    cdx = WaybackMachineCDXServerAPI(
        url="akamhy.github.io",
        user_agent=user_agent,
        match_type="prefix",
        use_pagination=True,
        filters=["statuscode:200"],
    )
    snapshots = cdx.snapshots()

    count = 0
    for snapshot in snapshots:
        count += 1
        assert str(snapshot.archive_url).find("akamhy.github.io")
    assert count > 50


def test_oldest() -> None:
    user_agent = (
        "Mozilla/5.0 (MacBook Air; M1 Mac OS X 11_4) "
        "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/604.1"
    )

    cdx = WaybackMachineCDXServerAPI(
        url="google.com",
        user_agent=user_agent,
        filters=["statuscode:200"],
    )
    oldest = cdx.oldest()
    assert "1998" in oldest.timestamp
    assert "google" in oldest.urlkey
    assert oldest.original.find("google.com") != -1
    assert oldest.archive_url.find("google.com") != -1


def test_newest() -> None:
    user_agent = (
        "Mozilla/5.0 (MacBook Air; M1 Mac OS X 11_4) "
        "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/604.1"
    )

    cdx = WaybackMachineCDXServerAPI(
        url="google.com",
        user_agent=user_agent,
        filters=["statuscode:200"],
    )
    newest = cdx.newest()
    assert "google" in newest.urlkey
    assert newest.original.find("google.com") != -1
    assert newest.archive_url.find("google.com") != -1


def test_near() -> None:
    user_agent = (
        "Mozilla/5.0 (MacBook Air; M1 Mac OS X 11_4) "
        "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/604.1"
    )

    cdx = WaybackMachineCDXServerAPI(
        url="google.com",
        user_agent=user_agent,
        filters=["statuscode:200"],
    )
    near = cdx.near(year=2010, month=10, day=10, hour=10, minute=10)
    assert "2010101010" in near.timestamp
    assert "google" in near.urlkey
    assert near.original.find("google.com") != -1
    assert near.archive_url.find("google.com") != -1

    near = cdx.near(wayback_machine_timestamp="201010101010")
    assert "2010101010" in near.timestamp
    assert "google" in near.urlkey
    assert near.original.find("google.com") != -1
    assert near.archive_url.find("google.com") != -1

    near = cdx.near(unix_timestamp=1286705410)
    assert "2010101010" in near.timestamp
    assert "google" in near.urlkey
    assert near.original.find("google.com") != -1
    assert near.archive_url.find("google.com") != -1

    with pytest.raises(NoCDXRecordFound):
        dne_url = f"https://{rndstr(30)}.in"
        cdx = WaybackMachineCDXServerAPI(
            url=dne_url,
            user_agent=user_agent,
            filters=["statuscode:200"],
        )
        cdx.near(unix_timestamp=1286705410)
