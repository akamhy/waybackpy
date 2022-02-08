import random
import string
from datetime import datetime, timedelta

import pytest

from waybackpy.availability_api import WaybackMachineAvailabilityAPI
from waybackpy.exceptions import (
    ArchiveNotInAvailabilityAPIResponse,
    InvalidJSONInAvailabilityAPIResponse,
)

now = datetime.utcnow()
url = "https://example.com/"
user_agent = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
)


def rndstr(n: int) -> str:
    return "".join(
        random.choice(string.ascii_uppercase + string.digits) for _ in range(n)
    )


def test_oldest() -> None:
    """
    Test the oldest archive of Google.com and also checks the attributes.
    """
    url = "https://example.com/"
    user_agent = (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
    )
    availability_api = WaybackMachineAvailabilityAPI(url, user_agent)
    oldest = availability_api.oldest()
    oldest_archive_url = oldest.archive_url
    assert "2002" in oldest_archive_url
    oldest_timestamp = oldest.timestamp()
    assert abs(oldest_timestamp - now) > timedelta(days=7000)  # More than 19 years
    assert (
        availability_api.json is not None
        and availability_api.json["archived_snapshots"]["closest"]["available"] is True
    )
    assert repr(oldest).find("example.com") != -1
    assert "2002" in str(oldest)


def test_newest() -> None:
    """
    Assuming that the recent most Google Archive was made no more earlier than
    last one day which is 86400 seconds.
    """
    url = "https://www.youtube.com/"
    user_agent = "Mozilla/5.0 (X11; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0"
    availability_api = WaybackMachineAvailabilityAPI(url, user_agent)
    newest = availability_api.newest()
    newest_timestamp = newest.timestamp()
    # betting in favor that latest youtube archive was not before the last 3 days
    # high tarffic sites like youtube are archived mnay times a day, so seems
    # very reasonable to me.
    assert abs(newest_timestamp - now) < timedelta(seconds=86400 * 3)


def test_invalid_json() -> None:
    """
    When the API is malfunctioning or we don't pass a URL,
    it may return invalid JSON data.
    """
    with pytest.raises(InvalidJSONInAvailabilityAPIResponse):
        availability_api = WaybackMachineAvailabilityAPI(url="", user_agent=user_agent)
        _ = availability_api.archive_url


def test_no_archive() -> None:
    """
    ArchiveNotInAvailabilityAPIResponse may be raised if Wayback Machine did not
    replied with the archive despite the fact that we know the site has million
    of archives. Don't know the reason for this wierd behavior.

    And also if really there are no archives for the passed URL this exception
    is raised.
    """
    with pytest.raises(ArchiveNotInAvailabilityAPIResponse):
        availability_api = WaybackMachineAvailabilityAPI(
            url=f"https://{rndstr(30)}.cn", user_agent=user_agent
        )
        _ = availability_api.archive_url


def test_no_api_call_str_repr() -> None:
    """
    Some entitled users maybe want to see what is the string representation
    if they don’t make any API requests.

    str() must not return None so we return ""
    """
    availability_api = WaybackMachineAvailabilityAPI(
        url=f"https://{rndstr(30)}.gov", user_agent=user_agent
    )
    assert str(availability_api) == ""


def test_no_call_timestamp() -> None:
    """
    If no API requests were made the bound timestamp() method returns
    the datetime.max as a default value.
    """
    availability_api = WaybackMachineAvailabilityAPI(
        url=f"https://{rndstr(30)}.in", user_agent=user_agent
    )
    assert datetime.max == availability_api.timestamp()
