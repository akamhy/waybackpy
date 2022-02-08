"""
This module interfaces the Wayback Machine's SavePageNow (SPN) API.

The module has WaybackMachineSaveAPI class which should be used by the users of
this module to use the SavePageNow API.
"""

import re
import time
from datetime import datetime
from typing import Dict, Optional

import requests
from requests.adapters import HTTPAdapter
from requests.models import Response
from requests.structures import CaseInsensitiveDict
from urllib3.util.retry import Retry

from .exceptions import MaximumSaveRetriesExceeded, TooManyRequestsError, WaybackError
from .utils import DEFAULT_USER_AGENT


class WaybackMachineSaveAPI:
    """
    WaybackMachineSaveAPI class provides an interface for saving URLs on the
    Wayback Machine.
    """

    def __init__(
        self,
        url: str,
        user_agent: str = DEFAULT_USER_AGENT,
        max_tries: int = 8,
    ) -> None:
        self.url = str(url).strip().replace(" ", "%20")
        self.request_url = "https://web.archive.org/save/" + self.url
        self.user_agent = user_agent
        self.request_headers: Dict[str, str] = {"User-Agent": self.user_agent}
        if max_tries < 1:
            raise ValueError("max_tries should be positive")
        self.max_tries = max_tries
        self.total_save_retries = 5
        self.backoff_factor = 0.5
        self.status_forcelist = [500, 502, 503, 504]
        self._archive_url: Optional[str] = None
        self.instance_birth_time = datetime.utcnow()
        self.response: Optional[Response] = None
        self.headers: Optional[CaseInsensitiveDict[str]] = None
        self.status_code: Optional[int] = None
        self.response_url: Optional[str] = None
        self.cached_save: Optional[bool] = None
        self.saved_archive: Optional[str] = None

    @property
    def archive_url(self) -> str:
        """
        Returns the archive URL is already cached by _archive_url
        else invoke the save method to save the archive which returns the
        archive thus we return the methods return value.
        """
        if self._archive_url:
            return self._archive_url

        return self.save()

    def get_save_request_headers(self) -> None:
        """
        Creates a session and tries 'retries' number of times to
        retrieve the archive.

        If successful in getting the response, sets the headers, status_code
        and response_url attributes.

        The archive is usually in the headers but it can also be the response URL
        as the Wayback Machine redirects to the archive after a successful capture
        of the webpage.

        Wayback Machine's save API is known
        to be very unreliable thus if it fails first check opening
        the response URL yourself in the browser.
        """
        session = requests.Session()
        retries = Retry(
            total=self.total_save_retries,
            backoff_factor=self.backoff_factor,
            status_forcelist=self.status_forcelist,
        )
        session.mount("https://", HTTPAdapter(max_retries=retries))
        self.response = session.get(self.request_url, headers=self.request_headers)
        # requests.response.headers is requests.structures.CaseInsensitiveDict
        self.headers = self.response.headers
        self.status_code = self.response.status_code
        self.response_url = self.response.url
        session.close()

        if self.status_code == 429:
            # why wait 5 minutes and 429?
            # see https://github.com/akamhy/waybackpy/issues/97
            raise TooManyRequestsError(
                f"Can not save '{self.url}'. "
                f"Save request refused by the server. "
                f"Save Page Now limits saving 15 URLs per minutes. "
                f"Try waiting for 5 minutes and then try again."
            )

        # why 509?
        # see https://github.com/akamhy/waybackpy/pull/99
        # also https://t.co/xww4YJ0Iwc
        if self.status_code == 509:
            raise WaybackError(
                f"Can not save '{self.url}'. You have probably reached the "
                f"limit of active sessions."
            )

    def archive_url_parser(self) -> Optional[str]:
        """
        Three regexen (like oxen?) are used to search for the
        archive URL in the headers and finally look in the response URL
        for the archive URL.
        """
        regex1 = r"Content-Location: (/web/[0-9]{14}/.*)"
        match = re.search(regex1, str(self.headers))
        if match:
            return "https://web.archive.org" + match.group(1)

        regex2 = r"rel=\"memento.*?(web\.archive\.org/web/[0-9]{14}/.*?)>"
        match = re.search(regex2, str(self.headers))
        if match is not None and len(match.groups()) == 1:
            return "https://" + match.group(1)

        regex3 = r"X-Cache-Key:\shttps(.*)[A-Z]{2}"
        match = re.search(regex3, str(self.headers))
        if match is not None and len(match.groups()) == 1:
            return "https" + match.group(1)

        self.response_url = (
            "" if self.response_url is None else self.response_url.strip()
        )
        regex4 = r"web\.archive\.org/web/(?:[0-9]*?)/(?:.*)$"
        match = re.search(regex4, self.response_url)
        if match is not None:
            return "https://" + match.group(0)

        return None

    @staticmethod
    def sleep(tries: int) -> None:
        """
        Ensure that the we wait some time before succesive retries so that we
        don't waste the retries before the page is even captured by the Wayback
        Machine crawlers also ensures that we are not putting too much load on
        the Wayback Machine's save API.

        If tries are multiple of 3 sleep 10 seconds else sleep 5 seconds.
        """
        sleep_seconds = 5
        if tries % 3 == 0:
            sleep_seconds = 10
        time.sleep(sleep_seconds)

    def timestamp(self) -> datetime:
        """
        Read the timestamp off the archive URL and convert the Wayback Machine
        timestamp to datetime object.

        Also check if the time on archive is URL and compare it to instance birth
        time.

        If time on the archive is older than the instance creation time set the
        cached_save to True else set it to False. The flag can be used to check
        if the Wayback Machine didn't serve a Cached URL. It is quite common for
        the Wayback Machine to serve cached archive if last archive was captured
        before last 45 minutes.
        """
        regex = r"https?://web\.archive.org/web/([0-9]{14})/http"
        match = re.search(regex, str(self._archive_url))

        if match is None or len(match.groups()) != 1:
            raise ValueError(
                f"Can not parse timestamp from archive URL, '{self._archive_url}'."
            )

        string_timestamp = match.group(1)
        timestamp = datetime.strptime(string_timestamp, "%Y%m%d%H%M%S")
        timestamp_unixtime = time.mktime(timestamp.timetuple())
        instance_birth_time_unixtime = time.mktime(self.instance_birth_time.timetuple())

        if timestamp_unixtime < instance_birth_time_unixtime:
            self.cached_save = True
        else:
            self.cached_save = False

        return timestamp

    def save(self) -> str:
        """
        Calls the SavePageNow API of the Wayback Machine with required parameters
        and headers to save the URL.

        Raises MaximumSaveRetriesExceeded is maximum retries are exhausted but still
        we were unable to retrieve the archive from the Wayback Machine.
        """
        self.saved_archive = None
        tries = 0

        while True:
            if tries >= 1:
                self.sleep(tries)

            self.get_save_request_headers()
            self.saved_archive = self.archive_url_parser()

            if isinstance(self.saved_archive, str):
                self._archive_url = self.saved_archive
                self.timestamp()
                return self.saved_archive

            tries += 1
            if tries >= self.max_tries:
                raise MaximumSaveRetriesExceeded(
                    f"Tried {tries} times but failed to save "
                    f"and retrieve the archive for {self.url}.\n"
                    f"Response URL:\n{self.response_url}\n"
                    f"Response Header:\n{self.headers}"
                )
