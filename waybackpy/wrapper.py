"""
This module exists because backwards compatibility matters.
Don't touch this or add any new functionality here and don't use
the Url class.
"""

from datetime import datetime, timedelta
from typing import Generator, Optional

from requests.structures import CaseInsensitiveDict

from .availability_api import ResponseJSON, WaybackMachineAvailabilityAPI
from .cdx_api import WaybackMachineCDXServerAPI
from .save_api import WaybackMachineSaveAPI
from .utils import DEFAULT_USER_AGENT


class Url:
    """
    The Url class is not recommended to be used anymore, instead use:

    - WaybackMachineSaveAPI
    - WaybackMachineAvailabilityAPI
    - WaybackMachineCDXServerAPI

    The reason it is still in the code is backwards compatibility with 2.x.x
    versions.

    If were are using the Url before the update to version 3.x.x, your code should
    still be working fine and there is no hurry to update the interface but is
    recommended that you do not use the Url class for new code as it would be
    removed after 2025 also the first 3.x.x versions was released in January 2022
    and three years are more than enough to update the older interface code.
    """

    def __init__(self, url: str, user_agent: str = DEFAULT_USER_AGENT) -> None:
        self.url = url
        self.user_agent = str(user_agent)
        self.archive_url: Optional[str] = None
        self.timestamp: Optional[datetime] = None
        self.wayback_machine_availability_api = WaybackMachineAvailabilityAPI(
            self.url, user_agent=self.user_agent
        )
        self.wayback_machine_save_api: Optional[WaybackMachineSaveAPI] = None
        self.headers: Optional[CaseInsensitiveDict[str]] = None
        self.json: Optional[ResponseJSON] = None

    def __str__(self) -> str:
        if not self.archive_url:
            self.newest()
        return str(self.archive_url)

    def __len__(self) -> int:
        td_max = timedelta(
            days=999999999, hours=23, minutes=59, seconds=59, microseconds=999999
        )

        if not isinstance(self.timestamp, datetime):
            self.oldest()

        if not isinstance(self.timestamp, datetime):
            raise TypeError("timestamp must be a datetime")

        if self.timestamp == datetime.max:
            return td_max.days

        return (datetime.utcnow() - self.timestamp).days

    def save(self) -> "Url":
        """Save the URL on wayback machine."""
        self.wayback_machine_save_api = WaybackMachineSaveAPI(
            self.url, user_agent=self.user_agent
        )
        self.archive_url = self.wayback_machine_save_api.archive_url
        self.timestamp = self.wayback_machine_save_api.timestamp()
        self.headers = self.wayback_machine_save_api.headers
        return self

    def near(
        self,
        year: Optional[int] = None,
        month: Optional[int] = None,
        day: Optional[int] = None,
        hour: Optional[int] = None,
        minute: Optional[int] = None,
        unix_timestamp: Optional[int] = None,
    ) -> "Url":
        """Returns the archive of the URL close to a date and time."""
        self.wayback_machine_availability_api.near(
            year=year,
            month=month,
            day=day,
            hour=hour,
            minute=minute,
            unix_timestamp=unix_timestamp,
        )
        self.set_availability_api_attrs()
        return self

    def oldest(self) -> "Url":
        """Returns the oldest archive of the URL."""
        self.wayback_machine_availability_api.oldest()
        self.set_availability_api_attrs()
        return self

    def newest(self) -> "Url":
        """Returns the newest archive of the URL."""
        self.wayback_machine_availability_api.newest()
        self.set_availability_api_attrs()
        return self

    def set_availability_api_attrs(self) -> None:
        """Set the attributes for total backwards compatibility."""
        self.archive_url = self.wayback_machine_availability_api.archive_url
        self.json = self.wayback_machine_availability_api.json
        self.JSON = self.json  # for backwards compatibility, do not remove it.
        self.timestamp = self.wayback_machine_availability_api.timestamp()

    def total_archives(
        self, start_timestamp: Optional[str] = None, end_timestamp: Optional[str] = None
    ) -> int:
        """
        Returns an integer which indicates total number of archives for an URL.
        Useless in my opinion, only here because of backwards compatibility.
        """
        cdx = WaybackMachineCDXServerAPI(
            self.url,
            user_agent=self.user_agent,
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp,
        )

        count = 0
        for _ in cdx.snapshots():
            count = count + 1
        return count

    def known_urls(
        self,
        subdomain: bool = False,
        host: bool = False,
        start_timestamp: Optional[str] = None,
        end_timestamp: Optional[str] = None,
        match_type: str = "prefix",
    ) -> Generator[str, None, None]:
        """Yields known URLs for any URL."""
        if subdomain:
            match_type = "domain"
        if host:
            match_type = "host"

        cdx = WaybackMachineCDXServerAPI(
            self.url,
            user_agent=self.user_agent,
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp,
            match_type=match_type,
            collapses=["urlkey"],
        )

        for snapshot in cdx.snapshots():
            yield snapshot.original
