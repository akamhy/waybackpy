"""
This module interfaces the Wayback Machine's availability API.

The interface is useful for looking up archives and finding archives
that are close to a specific date and time.

It has a class WaybackMachineAvailabilityAPI, and the class has
methods like:

near() for retrieving archives close to a specific date and time.

oldest() for retrieving the first archive URL of the webpage.

newest() for retrieving the latest archive of the webpage.

The Wayback Machine Availability API response must be a valid JSON and
if it is not then an exception, InvalidJSONInAvailabilityAPIResponse is raised.

If the Availability API returned valid JSON but archive URL could not be found
it it then ArchiveNotInAvailabilityAPIResponse is raised.
"""

import json
import time
from datetime import datetime
from typing import Any, Dict, Optional

import requests
from requests.models import Response

from .exceptions import (
    ArchiveNotInAvailabilityAPIResponse,
    InvalidJSONInAvailabilityAPIResponse,
)
from .utils import (
    DEFAULT_USER_AGENT,
    unix_timestamp_to_wayback_timestamp,
    wayback_timestamp,
)

ResponseJSON = Dict[str, Any]


class WaybackMachineAvailabilityAPI:
    """
    Class that interfaces the Wayback Machine's availability API.
    """

    def __init__(
        self, url: str, user_agent: str = DEFAULT_USER_AGENT, max_tries: int = 3
    ) -> None:

        self.url = str(url).strip().replace(" ", "%20")
        self.user_agent = user_agent
        self.headers: Dict[str, str] = {"User-Agent": self.user_agent}
        self.payload: Dict[str, str] = {"url": self.url}
        self.endpoint: str = "https://archive.org/wayback/available"
        self.max_tries: int = max_tries
        self.tries: int = 0
        self.last_api_call_unix_time: int = int(time.time())
        self.api_call_time_gap: int = 5
        self.json: Optional[ResponseJSON] = None
        self.response: Optional[Response] = None

    def __repr__(self) -> str:
        """
        Same as string representation, just return the archive URL as a string.
        """
        return str(self)

    def __str__(self) -> str:
        """
        String representation of the class. If atleast one API
        call was successfully made then return the archive URL
        as a string. Else returns "" (empty string literal).
        """
        # __str__ can not return anything other than a string object
        # So, if a string repr is asked even before making a API request
        # just return ""
        if not self.json:
            return ""

        return self.archive_url

    def setup_json(self) -> Optional[ResponseJSON]:
        """
        Makes the API call to the availability API and set the JSON response
        to the JSON attribute of the instance and also returns the JSON
        attribute.

        time_diff and sleep_time makes sure that you are not making too many
        requests in a short interval of item, making too many requests is bad
        as Wayback Machine may reject them above a certain threshold.

        The end-user can change the api_call_time_gap attribute of the instance
        to increase or decrease the default time gap between two successive API
        calls, but it is not recommended to increase it.
        """
        time_diff = int(time.time()) - self.last_api_call_unix_time
        sleep_time = self.api_call_time_gap - time_diff

        if sleep_time > 0:
            time.sleep(sleep_time)

        self.response = requests.get(
            self.endpoint, params=self.payload, headers=self.headers
        )
        self.last_api_call_unix_time = int(time.time())
        self.tries += 1
        try:
            self.json = None if self.response is None else self.response.json()
        except json.decoder.JSONDecodeError as json_decode_error:
            raise InvalidJSONInAvailabilityAPIResponse(
                f"Response data:\n{self.response.text}"
            ) from json_decode_error

        return self.json

    def timestamp(self) -> datetime:
        """
        Converts the timestamp form the JSON response to datetime object.
        If JSON attribute of the instance is None it implies that the either
        the the last API call failed or one was never made.

        If not JSON or if JSON but no timestamp in the JSON response then
        returns the maximum value for datetime object that is possible.

        If you get an URL as a response form the availability API it is
        guaranteed that you can get the datetime object from the timestamp.
        """
        if self.json is None or "archived_snapshots" not in self.json:
            return datetime.max

        if (
            self.json is not None
            and "archived_snapshots" in self.json
            and self.json["archived_snapshots"] is not None
            and "closest" in self.json["archived_snapshots"]
            and self.json["archived_snapshots"]["closest"] is not None
            and "timestamp" in self.json["archived_snapshots"]["closest"]
        ):
            return datetime.strptime(
                self.json["archived_snapshots"]["closest"]["timestamp"], "%Y%m%d%H%M%S"
            )

        raise ValueError("Timestamp not found in the Availability API's JSON response.")

    @property
    def archive_url(self) -> str:
        """
        Reads the the JSON response data and returns
        the timestamp if found and if not found raises
        ArchiveNotInAvailabilityAPIResponse.
        """
        archive_url = ""
        data = self.json

        # If the user didn't invoke oldest, newest or near but tries to access
        # archive_url attribute then assume they that are fine with any archive
        # and invoke the oldest method.
        if not data:
            self.oldest()

        # If data is still not none then probably there are no
        # archive for the requested URL.
        if not data or not data["archived_snapshots"]:
            while (self.tries < self.max_tries) and (
                not data or not data["archived_snapshots"]
            ):
                self.setup_json()  # It makes a new API call
                data = self.json  # setup_json() updates value of json attribute

            # If exhausted max_tries, then give up and
            # raise ArchiveNotInAvailabilityAPIResponse.

            if not data or not data["archived_snapshots"]:
                raise ArchiveNotInAvailabilityAPIResponse(
                    "Archive not found in the availability "
                    "API response, the URL you requested may not have any archives "
                    "yet. You may retry after some time or archive the webpage now.\n"
                    "Response data:\n"
                    ""
                    if self.response is None
                    else self.response.text
                )
        else:
            archive_url = data["archived_snapshots"]["closest"]["url"]
            archive_url = archive_url.replace(
                "http://web.archive.org/web/", "https://web.archive.org/web/", 1
            )
        return archive_url

    def oldest(self) -> "WaybackMachineAvailabilityAPI":
        """
        Passes the date 1994-01-01 to near which should return the oldest archive
        because Wayback Machine was started in May, 1996 and it is assumed that
        there would be no archive older than January 1, 1994.
        """
        return self.near(year=1994, month=1, day=1)

    def newest(self) -> "WaybackMachineAvailabilityAPI":
        """
        Passes the current UNIX time to near() for retrieving the newest archive
        from the availability API.

        Remember UNIX time is UTC and Wayback Machine is also UTC based.
        """
        return self.near(unix_timestamp=int(time.time()))

    def near(
        self,
        year: Optional[int] = None,
        month: Optional[int] = None,
        day: Optional[int] = None,
        hour: Optional[int] = None,
        minute: Optional[int] = None,
        unix_timestamp: Optional[int] = None,
    ) -> "WaybackMachineAvailabilityAPI":
        """
        The most important method of this Class, oldest() and newest() are
        dependent on it.

        It generates the timestamp based on the input either by calling the
        unix_timestamp_to_wayback_timestamp or wayback_timestamp method with
        appropriate arguments for their respective parameters.

        Adds the timestamp to the payload dictionary.

        And finally invokes the setup_json method to make the API call then
        finally returns the instance.
        """
        if unix_timestamp:
            timestamp = unix_timestamp_to_wayback_timestamp(unix_timestamp)
        else:
            now = datetime.utcnow().timetuple()
            timestamp = wayback_timestamp(
                year=now.tm_year if year is None else year,
                month=now.tm_mon if month is None else month,
                day=now.tm_mday if day is None else day,
                hour=now.tm_hour if hour is None else hour,
                minute=now.tm_min if minute is None else minute,
            )

        self.payload["timestamp"] = timestamp
        self.setup_json()
        return self
