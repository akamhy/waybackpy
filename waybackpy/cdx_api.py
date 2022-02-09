"""
This module interfaces the Wayback Machine's CDX server API.

The module has WaybackMachineCDXServerAPI which should be used by the users of
this module to consume the CDX server API.

WaybackMachineCDXServerAPI has a snapshot method that yields the snapshots, and
the snapshots are yielded as instances of the CDXSnapshot class.
"""


from typing import Dict, Generator, List, Optional, cast

from .cdx_snapshot import CDXSnapshot
from .cdx_utils import (
    check_collapses,
    check_filters,
    check_match_type,
    full_url,
    get_response,
    get_total_pages,
)
from .exceptions import WaybackError
from .utils import DEFAULT_USER_AGENT


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
        gzip: Optional[str] = None,
        collapses: Optional[List[str]] = None,
        limit: Optional[str] = None,
        max_tries: int = 3,
    ) -> None:
        self.url = str(url).strip().replace(" ", "%20")
        self.user_agent = user_agent
        self.start_timestamp = None if start_timestamp is None else str(start_timestamp)
        self.end_timestamp = None if end_timestamp is None else str(end_timestamp)
        self.filters = [] if filters is None else filters
        check_filters(self.filters)
        self.match_type = None if match_type is None else str(match_type).strip()
        check_match_type(self.match_type, self.url)
        self.gzip = gzip
        self.collapses = [] if collapses is None else collapses
        check_collapses(self.collapses)
        self.limit = 25000 if limit is None else limit
        self.max_tries = max_tries
        self.last_api_request_url: Optional[str] = None
        self.use_page = False
        self.endpoint = "https://web.archive.org/cdx/search/cdx"

    def cdx_api_manager(
        self, payload: Dict[str, str], headers: Dict[str, str], use_page: bool = False
    ) -> Generator[str, None, None]:
        """
        Manages the API calls for the instance, it automatically selects the best
        parameters by looking as the query of the end-user. For bigger queries
        automatically use the CDX pagination API and for smaller queries use the
        normal API.

        CDX Server API is a complex API and to make it easy for the end user to
        consume it the CDX manager(this method) handles the selection of the
        API output, whether to use the pagination API or not.

        For doing large/bulk queries, the use of the Pagination API is
        recommended by the Wayback Machine authors. And it determines if the
        query would be large or not by using the showNumPages=true parameter,
        this tells the number of pages of CDX DATA that the pagination API
        will return.

        If the number of page is less than 2 we use the normal non-pagination
        API as the pagination API is known to lag and for big queries it should
        not matter but for queries where the number of pages are less this
        method chooses accuracy over the pagination API.
        """
        # number of pages that will returned by the pagination API.
        # get_total_pages adds the showNumPages=true param to pagination API
        # requests.
        # This is a special query that will return a single number indicating
        # the number of pages.
        total_pages = get_total_pages(self.url, self.user_agent)

        if use_page is True and total_pages >= 2:
            blank_pages = 0
            for i in range(total_pages):
                payload["page"] = str(i)

                url = full_url(self.endpoint, params=payload)
                res = get_response(url, headers=headers)
                if isinstance(res, Exception):
                    raise res

                self.last_api_request_url = url
                text = res.text
                if len(text) == 0:
                    blank_pages += 1

                if blank_pages >= 2:
                    break

                yield text
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

        if self.match_type:
            payload["matchType"] = self.match_type

        if self.filters and len(self.filters) > 0:
            for i, _filter in enumerate(self.filters):
                payload["filter" + str(i)] = _filter

        if self.collapses and len(self.collapses) > 0:
            for i, collapse in enumerate(self.collapses):
                payload["collapse" + str(i)] = collapse

        payload["url"] = self.url

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

        if not self.start_timestamp or self.end_timestamp:
            self.use_page = True

        if self.collapses != []:
            self.use_page = False

        entries = self.cdx_api_manager(payload, headers, use_page=self.use_page)

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
