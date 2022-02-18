"""
This module interfaces the Wayback Machine's CDX server API.

The module has WaybackMachineCDXServerAPI which should be used by the users of
this module to consume the CDX server API.

WaybackMachineCDXServerAPI has a snapshot method that yields the snapshots, and
the snapshots are yielded as instances of the CDXSnapshot class.
"""


import time
from datetime import datetime
from typing import Dict, Generator, List, Optional, Union, cast

from .cdx_snapshot import CDXSnapshot
from .cdx_utils import (
    check_collapses,
    check_filters,
    check_match_type,
    check_sort,
    full_url,
    get_response,
    get_total_pages,
)
from .exceptions import NoCDXRecordFound, WaybackError
from .utils import (
    DEFAULT_USER_AGENT,
    unix_timestamp_to_wayback_timestamp,
    wayback_timestamp,
)


class WaybackMachineCDXServerAPI:
    """
    Class that interfaces the CDX server API of the Wayback Machine.

    snapshot() returns a generator that can be iterated upon by the end-user,
    the generator returns the snapshots/entries as instance of CDXSnapshot to
    make the usage easy, just use '.' to get any attribute as the attributes are
    accessible via a dot ".".
    """

    # start_timestamp: from, can not use from as it's a keyword
    # end_timestamp: to, not using to as can not use from
    def __init__(
        self,
        url: str,
        user_agent: str = DEFAULT_USER_AGENT,
        start_timestamp: Optional[str] = None,
        end_timestamp: Optional[str] = None,
        filters: Optional[List[str]] = None,
        match_type: Optional[str] = None,
        sort: Optional[str] = None,
        gzip: Optional[str] = None,
        collapses: Optional[List[str]] = None,
        limit: Optional[str] = None,
        max_tries: int = 3,
        use_pagination: bool = False,
        closest: Optional[str] = None,
    ) -> None:
        self.url = str(url).strip().replace(" ", "%20")
        self.user_agent = user_agent
        self.start_timestamp = None if start_timestamp is None else str(start_timestamp)
        self.end_timestamp = None if end_timestamp is None else str(end_timestamp)
        self.filters = [] if filters is None else filters
        check_filters(self.filters)
        self.match_type = None if match_type is None else str(match_type).strip()
        check_match_type(self.match_type, self.url)
        self.sort = None if sort is None else str(sort).strip()
        check_sort(self.sort)
        self.gzip = gzip
        self.collapses = [] if collapses is None else collapses
        check_collapses(self.collapses)
        self.limit = 25000 if limit is None else limit
        self.max_tries = max_tries
        self.use_pagination = use_pagination
        self.closest = None if closest is None else str(closest)
        self.last_api_request_url: Optional[str] = None
        self.endpoint = "https://web.archive.org/cdx/search/cdx"

    def cdx_api_manager(
        self, payload: Dict[str, str], headers: Dict[str, str]
    ) -> Generator[str, None, None]:
        """
        This method uses the pagination API of the CDX server if
        use_pagination attribute is True else uses the standard
        CDX server response data.
        """

        # When using the pagination API of the CDX server.
        if self.use_pagination is True:

            total_pages = get_total_pages(self.url, self.user_agent)
            successive_blank_pages = 0

            for i in range(total_pages):
                payload["page"] = str(i)

                url = full_url(self.endpoint, params=payload)
                res = get_response(url, headers=headers)

                if isinstance(res, Exception):
                    raise res

                self.last_api_request_url = url
                text = res.text

                # Reset the counter if the last page was blank
                # but the current page is not.
                if successive_blank_pages == 1:
                    if len(text) != 0:
                        successive_blank_pages = 0

                # Increase the succesive page counter on encountering
                # blank page.
                if len(text) == 0:
                    successive_blank_pages += 1

                # If two succesive pages are blank
                # then we don't have any more pages left to
                # iterate.
                if successive_blank_pages >= 2:
                    break

                yield text

        # When not using the pagination API of the CDX server
        else:
            payload["showResumeKey"] = "true"
            payload["limit"] = str(self.limit)
            resume_key = None
            more = True
            while more:
                if resume_key:
                    payload["resumeKey"] = resume_key

                url = full_url(self.endpoint, params=payload)
                res = get_response(url, headers=headers)
                if isinstance(res, Exception):
                    raise res

                self.last_api_request_url = url

                text = res.text.strip()
                lines = text.splitlines()

                more = False

                if len(lines) >= 3:

                    second_last_line = lines[-2]

                    if len(second_last_line) == 0:

                        resume_key = lines[-1].strip()
                        text = text.replace(resume_key, "", 1).strip()
                        more = True

                yield text

    def add_payload(self, payload: Dict[str, str]) -> None:
        """
        Adds the payload to the payload dictionary.
        """
        if self.start_timestamp:
            payload["from"] = self.start_timestamp

        if self.end_timestamp:
            payload["to"] = self.end_timestamp

        if self.gzip is None:
            payload["gzip"] = "false"

        if self.closest:
            payload["closest"] = self.closest

        if self.match_type:
            payload["matchType"] = self.match_type

        if self.sort:
            payload["sort"] = self.sort

        if self.filters and len(self.filters) > 0:
            for i, _filter in enumerate(self.filters):
                payload["filter" + str(i)] = _filter

        if self.collapses and len(self.collapses) > 0:
            for i, collapse in enumerate(self.collapses):
                payload["collapse" + str(i)] = collapse

        payload["url"] = self.url

    def near(
        self,
        year: Optional[int] = None,
        month: Optional[int] = None,
        day: Optional[int] = None,
        hour: Optional[int] = None,
        minute: Optional[int] = None,
        unix_timestamp: Optional[int] = None,
        wayback_machine_timestamp: Optional[Union[int, str]] = None,
    ) -> CDXSnapshot:
        """
        Fetch archive close to a datetime, it can only return
        a single URL. If you want more do not use this method
        instead use the class.
        """
        if unix_timestamp:
            timestamp = unix_timestamp_to_wayback_timestamp(unix_timestamp)
        elif wayback_machine_timestamp:
            timestamp = str(wayback_machine_timestamp)
        else:
            now = datetime.utcnow().timetuple()
            timestamp = wayback_timestamp(
                year=now.tm_year if year is None else year,
                month=now.tm_mon if month is None else month,
                day=now.tm_mday if day is None else day,
                hour=now.tm_hour if hour is None else hour,
                minute=now.tm_min if minute is None else minute,
            )
        self.closest = timestamp
        self.sort = "closest"
        self.limit = 1
        first_snapshot = None
        for snapshot in self.snapshots():
            first_snapshot = snapshot
            break

        if not first_snapshot:
            raise NoCDXRecordFound(
                "Wayback Machine's CDX server did not return any records "
                + "for the query. The URL may not have any archives "
                + " on the Wayback Machine or the URL may have been recently "
                + "archived and is still not available on the CDX server."
            )

        return first_snapshot

    def newest(self) -> CDXSnapshot:
        """
        Passes the current UNIX time to near() for retrieving the newest archive
        from the availability API.

        Remember UNIX time is UTC and Wayback Machine is also UTC based.
        """
        return self.near(unix_timestamp=int(time.time()))

    def oldest(self) -> CDXSnapshot:
        """
        Passes the date 1994-01-01 to near which should return the oldest archive
        because Wayback Machine was started in May, 1996 and it is assumed that
        there would be no archive older than January 1, 1994.
        """
        return self.near(year=1994, month=1, day=1)

    def snapshots(self) -> Generator[CDXSnapshot, None, None]:
        """
        This function yields the CDX data lines as snapshots.

        As it is a generator it exhaustible, the reason that this is
        a generator and not a list are:

        a) CDX server API can return millions of entries for a query and list
        is not suitable for such cases.

        b) Preventing memory usage issues, as told before this method may yield
        millions of records for some queries and your system may not have enough
        memory for such a big list. Also Remember this if outputing to Jupyter
        Notebooks.

        The objects yielded by this method are instance of CDXSnapshot class,
        you can access the attributes of the entries as the attribute of the instance
        itself.
        """
        payload: Dict[str, str] = {}
        headers = {"User-Agent": self.user_agent}

        self.add_payload(payload)

        entries = self.cdx_api_manager(payload, headers)

        for entry in entries:

            if entry.isspace() or len(entry) <= 1 or not entry:
                continue

            # each line is a snapshot aka entry of the CDX server API.
            # We are able to split the page by lines because it only
            # splits the lines on a sinlge page and not all the entries
            # at once, thus there should be no issues of too much memory usage.
            snapshot_list = entry.split("\n")

            for snapshot in snapshot_list:

                # 14 + 32 == 46 ( timestamp + digest ), ignore the invalid entries.
                # they are invalid if their length is smaller than sum of length
                # of a standard wayback_timestamp and standard digest of an entry.
                if len(snapshot) < 46:
                    continue

                properties: Dict[str, Optional[str]] = {
                    "urlkey": None,
                    "timestamp": None,
                    "original": None,
                    "mimetype": None,
                    "statuscode": None,
                    "digest": None,
                    "length": None,
                }

                property_value = snapshot.split(" ")

                total_property_values = len(property_value)
                warranted_total_property_values = len(properties)

                if total_property_values != warranted_total_property_values:
                    raise WaybackError(
                        f"Snapshot returned by CDX API has {total_property_values} prop"
                        f"erties instead of expected {warranted_total_property_values} "
                        f"properties.\nProblematic Snapshot: {snapshot}"
                    )

                (
                    properties["urlkey"],
                    properties["timestamp"],
                    properties["original"],
                    properties["mimetype"],
                    properties["statuscode"],
                    properties["digest"],
                    properties["length"],
                ) = property_value

                yield CDXSnapshot(cast(Dict[str, str], properties))
