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


class WaybackMachineCDXServerAPI(object):
    """
    Class that interfaces the CDX server API of the Wayback Machine.
    """

    # start_timestamp: from, can not use from as it's a keyword
    # end_timestamp: to, not using to as can not use from
    def __init__(
        self,
        url: str,
        user_agent: str = DEFAULT_USER_AGENT,
        start_timestamp: Optional[str] = None,
        end_timestamp: Optional[str] = None,
        filters: List[str] = [],
        match_type: Optional[str] = None,
        gzip: Optional[str] = None,
        collapses: List[str] = [],
        limit: Optional[str] = None,
        max_tries: int = 3,
    ) -> None:
        self.url = str(url).strip().replace(" ", "%20")
        self.user_agent = user_agent
        self.start_timestamp = (
            str(start_timestamp) if start_timestamp is not None else None
        )
        self.end_timestamp = str(end_timestamp) if end_timestamp is not None else None
        self.filters = filters
        check_filters(self.filters)
        self.match_type = str(match_type).strip() if match_type is not None else None
        check_match_type(self.match_type, self.url)
        self.gzip = gzip
        self.collapses = collapses
        check_collapses(self.collapses)
        self.limit = limit if limit is not None else 5000
        self.max_tries = max_tries
        self.last_api_request_url: Optional[str] = None
        self.use_page = False
        self.endpoint = "https://web.archive.org/cdx/search/cdx"

    def cdx_api_manager(
        self, payload: Dict[str, str], headers: Dict[str, str], use_page: bool = False
    ) -> Generator[str, None, None]:
        total_pages = get_total_pages(self.url, self.user_agent)
        # If we only have two or less pages of archives then we care for more accuracy
        # pagination API is lagged sometimes
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
            resumeKey = None
            more = True
            while more:
                if resumeKey:
                    payload["resumeKey"] = resumeKey

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

                        resumeKey = lines[-1].strip()
                        text = text.replace(resumeKey, "", 1).strip()
                        more = True

                yield text

    def add_payload(self, payload: Dict[str, str]) -> None:
        if self.start_timestamp:
            payload["from"] = self.start_timestamp

        if self.end_timestamp:
            payload["to"] = self.end_timestamp

        if self.gzip is None:
            payload["gzip"] = "false"

        if self.match_type:
            payload["matchType"] = self.match_type

        if self.filters and len(self.filters) > 0:
            for i, f in enumerate(self.filters):
                payload["filter" + str(i)] = f

        if self.collapses and len(self.collapses) > 0:
            for i, f in enumerate(self.collapses):
                payload["collapse" + str(i)] = f

        # Don't need to return anything as it's dictionary.
        payload["url"] = self.url

    def snapshots(self) -> Generator[CDXSnapshot, None, None]:
        payload: Dict[str, str] = {}
        headers = {"User-Agent": self.user_agent}

        self.add_payload(payload)

        if not self.start_timestamp or self.end_timestamp:
            self.use_page = True

        if self.collapses != []:
            self.use_page = False

        texts = self.cdx_api_manager(payload, headers, use_page=self.use_page)

        for text in texts:

            if text.isspace() or len(text) <= 1 or not text:
                continue

            snapshot_list = text.split("\n")

            for snapshot in snapshot_list:

                if len(snapshot) < 46:  # 14 + 32 (timestamp+digest)
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

                prop_values = snapshot.split(" ")

                prop_values_len = len(prop_values)
                properties_len = len(properties)

                if prop_values_len != properties_len:
                    raise WaybackError(
                        "Snapshot returned by Cdx API has {prop_values_len} properties".format(
                            prop_values_len=prop_values_len
                        )
                        + " instead of expected {properties_len} ".format(
                            properties_len=properties_len
                        )
                        + "properties.\nProblematic Snapshot : {snapshot}".format(
                            snapshot=snapshot
                        )
                    )

                (
                    properties["urlkey"],
                    properties["timestamp"],
                    properties["original"],
                    properties["mimetype"],
                    properties["statuscode"],
                    properties["digest"],
                    properties["length"],
                ) = prop_values

                yield CDXSnapshot(cast(Dict[str, str], properties))
