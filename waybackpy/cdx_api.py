from .exceptions import WaybackError
from .cdx_snapshot import CDXSnapshot
from .cdx_utils import (
    get_total_pages,
    get_response,
    check_filters,
    check_collapses,
    check_match_type,
)

from .utils import DEFAULT_USER_AGENT


class WaybackMachineCDXServerAPI:
    def __init__(
        self,
        url,
        user_agent=None,
        start_timestamp=None,
        end_timestamp=None,
        filters=[],
        match_type=None,
        gzip=None,
        collapses=[],
        limit=None,
    ):
        self.url = str(url).strip().replace(" ", "%20")
        self.user_agent = str(user_agent) if user_agent else DEFAULT_USER_AGENT
        self.start_timestamp = str(start_timestamp) if start_timestamp else None
        self.end_timestamp = str(end_timestamp) if end_timestamp else None
        self.filters = filters
        check_filters(self.filters)
        self.match_type = str(match_type).strip() if match_type else None
        check_match_type(self.match_type, self.url)
        self.gzip = gzip if gzip else True
        self.collapses = collapses
        check_collapses(self.collapses)
        self.limit = limit if limit else 5000
        self.last_api_request_url = None
        self.use_page = False
        self.endpoint = "https://web.archive.org/cdx/search/cdx"

    def cdx_api_manager(self, payload, headers, use_page=False):

        total_pages = get_total_pages(self.url, self.user_agent)
        # If we only have two or less pages of archives then we care for accuracy
        # pagination API can be lagged sometimes
        if use_page == True and total_pages >= 2:
            blank_pages = 0
            for i in range(total_pages):
                payload["page"] = str(i)

                url, res = get_response(
                    self.endpoint, params=payload, headers=headers, return_full_url=True
                )

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

                url, res = get_response(
                    self.endpoint, params=payload, headers=headers, return_full_url=True
                )

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

    def add_payload(self, payload):
        if self.start_timestamp:
            payload["from"] = self.start_timestamp

        if self.end_timestamp:
            payload["to"] = self.end_timestamp

        if self.gzip != True:
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

    def snapshots(self):
        payload = {}
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

                properties = {
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
                        "Snapshot returned by Cdx API has {prop_values_len} properties instead of expected {properties_len} properties.\nInvolved Snapshot : {snapshot}".format(
                            prop_values_len=prop_values_len,
                            properties_len=properties_len,
                            snapshot=snapshot,
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

                yield CDXSnapshot(properties)
