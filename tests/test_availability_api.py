import pytest
import random
import string
from datetime import datetime, timedelta

from waybackpy.availability_api import WaybackMachineAvailabilityAPI
from waybackpy.exceptions import (
    InvalidJSONInAvailabilityAPIResponse,
    ArchiveNotInAvailabilityAPIResponse,
)

now = datetime.utcnow()
url = "https://google.com"
user_agent = "Mozilla/5.0 (Windows NT 5.1; rv:40.0) Gecko/20100101 Firefox/40.0"

rndstr = lambda n: "".join(
    random.choice(string.ascii_uppercase + string.digits) for _ in range(n)
)

availability_api = WaybackMachineAvailabilityAPI(url, user_agent)


def test_oldest():
    """
    Test the oldest archive of Google.com and also checks the attributes.
    """
    oldest = availability_api.oldest()
    oldest_archive_url = oldest.archive_url
    assert "1998" in oldest_archive_url
    oldest_timestamp = oldest.timestamp()
    assert abs(oldest_timestamp - now) > timedelta(days=8400)  # More than 20 years
    assert availability_api.JSON["archived_snapshots"]["closest"]["available"] is True
    assert "google.com" in repr(oldest)
    assert "1998" in str(oldest)


def test_newest():
    """
    Assuming that the recent most Google Archive was made no more earlier than
    last one day which is 86400 seconds.
    """
    newest = availability_api.newest()
    newest_timestamp = newest.timestamp()
    assert abs(newest_timestamp - now) < timedelta(seconds=86400)


def test_invalid_json():
    """
    When the API is malfunctioning or we don't pass a URL it may return invalid JSON data.
    """
    with pytest.raises(InvalidJSONInAvailabilityAPIResponse):
        availability_api = WaybackMachineAvailabilityAPI(url="", user_agent=user_agent)
        archive_url = availability_api.archive_url


def test_no_archive():
    """
    ArchiveNotInAvailabilityAPIResponse may be raised if Wayback Machine did not
    replied with the archive despite the fact that we know the site has million
    of archives. Don't know the reason for this wierd behavior.

    And also if really there are no archives for the passed URL this exception
    is raised.
    """
    with pytest.raises(ArchiveNotInAvailabilityAPIResponse):
        availability_api = WaybackMachineAvailabilityAPI(
            url="https://%s.com" % rndstr(30), user_agent=user_agent
        )
        archive_url = availability_api.archive_url


def test_no_api_call_str_repr():
    """
    Some entitled users maybe want to see what is the string representation
    if they don’t make any API requests.

    str() must not return None so we return ""
    """
    availability_api = WaybackMachineAvailabilityAPI(
        url="https://%s.com" % rndstr(30), user_agent=user_agent
    )
    assert "" == str(availability_api)


def test_no_call_timestamp():
    """
    If no API requests were made the bound timestamp() method returns
    the datetime.max as a default value.
    """
    availability_api = WaybackMachineAvailabilityAPI(
        url="https://%s.com" % rndstr(30), user_agent=user_agent
    )
    assert datetime.max == availability_api.timestamp()
