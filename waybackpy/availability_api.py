import time
import json
import requests
from datetime import datetime
from .utils import DEFAULT_USER_AGENT
from .exceptions import (
    ArchiveNotInAvailabilityAPIResponse,
    InvalidJSONInAvailabilityAPIResponse,
)


class WaybackMachineAvailabilityAPI:
    """
    Class that interfaces the availability API of the Wayback Machine.
    """

    def __init__(self, url, user_agent=DEFAULT_USER_AGENT):
        self.url = str(url).strip().replace(" ", "%20")
        self.user_agent = user_agent
        self.headers = {"User-Agent": self.user_agent}
        self.payload = {"url": "{url}".format(url=self.url)}
        self.endpoint = "https://archive.org/wayback/available"
        self.JSON = None

    def unix_timestamp_to_wayback_timestamp(self, unix_timestamp):
        """
        Converts Unix time to wayback Machine timestamp.
        """
        return datetime.utcfromtimestamp(int(unix_timestamp)).strftime("%Y%m%d%H%M%S")

    def __repr__(self):
        """
        Same as string representation, just return the archive URL as a string.
        """
        return str(self)

    def __str__(self):
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

    def json(self):
        """
        Makes the API call to the availability API can set the JSON response
        to the JSON attribute of the instance and also returns the JSON attribute.
        """
        self.response = requests.get(
            self.endpoint, params=self.payload, headers=self.headers
        )
        try:
            self.JSON = self.response.json()
        except json.decoder.JSONDecodeError:
            raise InvalidJSONInAvailabilityAPIResponse(
                "Response data:\n{text}".format(text=self.response.text)
            )

        return self.JSON

    def timestamp(self):
        """
        Converts the timestamp form the JSON response to datetime object.
        If JSON attribute of the instance is None it implies that the either
        the the last API call failed or one was never made.

        If not JSON or if JSON but no timestamp in the JSON response then returns
        the maximum value for datetime object that is possible.

        If you get an URL as a response form the availability API it is guaranteed
        that you can get the datetime object from the timestamp.
        """
        if not self.JSON or not self.JSON["archived_snapshots"]:
            return datetime.max

        return datetime.strptime(
            self.JSON["archived_snapshots"]["closest"]["timestamp"], "%Y%m%d%H%M%S"
        )

    @property
    def archive_url(self):
        """
        Reads the the JSON response data and tries to get the timestamp and returns
        the timestamp if found else returns None.
        """
        data = self.JSON

        # If the user didn't used oldest, newest or near but tries to access the
        # archive_url attribute then, we assume they are fine with any archive
        # and invoke the oldest archive function.
        if not data:
            self.oldest()

        # If data is still not none then probably there are no
        # archive for the requested URL.
        if not data or not data["archived_snapshots"]:
            raise ArchiveNotInAvailabilityAPIResponse(
                "Archive not found in the availability "
                + "API response, maybe the URL you requested does not have any "
                + "archive yet. You may retry after some time or archive the webpage now."
                + "\nResponse data:\n{response}".format(response=self.response.text)
            )
        else:
            archive_url = data["archived_snapshots"]["closest"]["url"]
            archive_url = archive_url.replace(
                "http://web.archive.org/web/", "https://web.archive.org/web/", 1
            )
        return archive_url

    def wayback_timestamp(self, **kwargs):
        """
        Prepends zero before the year, month, day, hour and minute so that they
        are conformable with the YYYYMMDDhhmmss wayback machine timestamp format.
        """
        return "".join(
            str(kwargs[key]).zfill(2)
            for key in ["year", "month", "day", "hour", "minute"]
        )

    def oldest(self):
        """
        Passing the year 1994 should return the oldest archive because
        wayback machine was started in May, 1996 and there should be no archive
        before the year 1994.
        """
        return self.near(year=1994)

    def newest(self):
        """
        Passing the current UNIX time should be sufficient to get the newest
        archive considering the API request-response time delay and also the
        database lags on Wayback machine.
        """
        return self.near(unix_timestamp=int(time.time()))

    def near(
        self,
        year=None,
        month=None,
        day=None,
        hour=None,
        minute=None,
        unix_timestamp=None,
    ):
        """
        The main method for this Class, oldest and newest methods are dependent on this
        method.

        It generates the timestamp based on the input either by calling the
        unix_timestamp_to_wayback_timestamp or wayback_timestamp method with
        appropriate arguments for their respective parameters.
        Adds the timestamp to the payload dictionary.
        And finally invoking the json method to make the API call then returns the instance.
        """
        if unix_timestamp:
            timestamp = self.unix_timestamp_to_wayback_timestamp(unix_timestamp)
        else:
            now = datetime.utcnow().timetuple()
            timestamp = self.wayback_timestamp(
                year=year if year else now.tm_year,
                month=month if month else now.tm_mon,
                day=day if day else now.tm_mday,
                hour=hour if hour else now.tm_hour,
                minute=minute if minute else now.tm_min,
            )

        self.payload["timestamp"] = timestamp
        self.json()
        return self
