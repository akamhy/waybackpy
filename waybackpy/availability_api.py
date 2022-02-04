import json
import time
from datetime import datetime
from typing import Any, Dict, Optional

import requests

from .exceptions import (
    ArchiveNotInAvailabilityAPIResponse,
    InvalidJSONInAvailabilityAPIResponse,
)
from .utils import DEFAULT_USER_AGENT

ResponseJSON = Dict[str, Any]


class WaybackMachineAvailabilityAPI(object):
    """
    Class that interfaces the availability API of the Wayback Machine.
    """

    def __init__(
        self, url: str, user_agent: str = DEFAULT_USER_AGENT, max_tries: int = 3
    ) -> None:
        self.url = str(url).strip().replace(" ", "%20")
        self.user_agent = user_agent
        self.headers: Dict[str, str] = {"User-Agent": self.user_agent}
        self.payload = {"url": self.url}
        self.endpoint = "https://archive.org/wayback/available"
        self.max_tries = max_tries
        self.tries = 0
        self.last_api_call_unix_time = int(time.time())
        self.api_call_time_gap = 5
        self.JSON: Optional[ResponseJSON] = None

    @staticmethod
    def unix_timestamp_to_wayback_timestamp(unix_timestamp: int) -> str:
        """
        Converts Unix time to wayback Machine timestamp.
        """
        return datetime.utcfromtimestamp(int(unix_timestamp)).strftime("%Y%m%d%H%M%S")

    def __repr__(self) -> str:
        """
        Same as string representation, just return the archive URL as a string.
        """
        return str(self)

    def __str__(self) -> str:
        """
        String representation of the class. If atleast one API call was successfully
        made then return the archive URL as a string. Else returns None.
        """

        # String must not return anything other than a string object
        # So, if some asks for string repr before making the API requests
        # just return ""
        if not self.JSON:
            return ""

        return self.archive_url

    def json(self) -> Optional[ResponseJSON]:
        """
        Makes the API call to the availability API can set the JSON response
        to the JSON attribute of the instance and also returns the JSON attribute.
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
            self.JSON = self.response.json()
        except json.decoder.JSONDecodeError:
            raise InvalidJSONInAvailabilityAPIResponse(
                f"Response data:\n{self.response.text}"
            )

        return self.JSON

    def timestamp(self) -> datetime:
        """
        Converts the timestamp form the JSON response to datetime object.
        If JSON attribute of the instance is None it implies that the either
        the the last API call failed or one was never made.

        If not JSON or if JSON but no timestamp in the JSON response then returns
        the maximum value for datetime object that is possible.

        If you get an URL as a response form the availability API it is guaranteed
        that you can get the datetime object from the timestamp.
        """
        if self.JSON is None or "archived_snapshots" not in self.JSON:
            return datetime.max
        elif (
            self.JSON is not None
            and "archived_snapshots" in self.JSON
            and self.JSON["archived_snapshots"] is not None
            and "closest" in self.JSON["archived_snapshots"]
            and self.JSON["archived_snapshots"]["closest"] is not None
            and "timestamp" in self.JSON["archived_snapshots"]["closest"]
        ):
            return datetime.strptime(
                self.JSON["archived_snapshots"]["closest"]["timestamp"], "%Y%m%d%H%M%S"
            )
        else:
            raise ValueError("Could not get timestamp from result")

    @property
    def archive_url(self) -> str:
        """
        Reads the the JSON response data and tries to get the timestamp and returns
        the timestamp if found else returns None.
        """
        archive_url = ""
        data = self.JSON

        # If the user didn't used oldest, newest or near but tries to access the
        # archive_url attribute then, we assume they are fine with any archive
        # and invoke the oldest archive function.
        if not data:
            self.oldest()

        # If data is still not none then probably there are no
        # archive for the requested URL.
        if not data or not data["archived_snapshots"]:
            while (self.tries < self.max_tries) and (
                not data or not data["archived_snapshots"]
            ):
                self.json()  # It makes a new API call
                data = self.JSON  # json() updated the value of JSON attribute

            # Even if after we exhausted teh max_tries, then we give up and
            # raise exception.

            if not data or not data["archived_snapshots"]:
                raise ArchiveNotInAvailabilityAPIResponse(
                    "Archive not found in the availability "
                    "API response, the URL you requested may not have any archives "
                    "yet. You may retry after some time or archive the webpage now.\n"
                    f"Response data:\n{self.response.text}"
                )
        else:
            archive_url = data["archived_snapshots"]["closest"]["url"]
            archive_url = archive_url.replace(
                "http://web.archive.org/web/", "https://web.archive.org/web/", 1
            )
        return archive_url

    @staticmethod
    def wayback_timestamp(**kwargs: int) -> str:
        """
        Prepends zero before the year, month, day, hour and minute so that they
        are conformable with the YYYYMMDDhhmmss wayback machine timestamp format.
        """
        return "".join(
            str(kwargs[key]).zfill(2)
            for key in ["year", "month", "day", "hour", "minute"]
        )

    def oldest(self) -> "WaybackMachineAvailabilityAPI":
        """
        Passing the year 1994 should return the oldest archive because
        wayback machine was started in May, 1996 and there should be no archive
        before the year 1994.
        """
        return self.near(year=1994)

    def newest(self) -> "WaybackMachineAvailabilityAPI":
        """
        Passing the current UNIX time should be sufficient to get the newest
        archive considering the API request-response time delay and also the
        database lags on Wayback machine.
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
        The main method for this Class, oldest and newest methods are dependent on this
        method.

        It generates the timestamp based on the input either by calling the
        unix_timestamp_to_wayback_timestamp or wayback_timestamp method with
        appropriate arguments for their respective parameters.
        Adds the timestamp to the payload dictionary.
        And finally invoking the json method to make the API call then returns
        the instance.
        """
        if unix_timestamp:
            timestamp = self.unix_timestamp_to_wayback_timestamp(unix_timestamp)
        else:
            now = datetime.utcnow().timetuple()
            timestamp = self.wayback_timestamp(
                year=now.tm_year if year is None else year,
                month=now.tm_mon if month is None else month,
                day=now.tm_mday if day is None else day,
                hour=now.tm_hour if hour is None else hour,
                minute=now.tm_min if minute is None else minute,
            )

        self.payload["timestamp"] = timestamp
        self.json()
        return self
