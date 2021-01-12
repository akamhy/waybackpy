from .snapshot import CdxSnapshot
from .exceptions import WaybackError
from .utils import (
    _get_total_pages,
    _get_response,
    default_user_agent,
    _check_filters,
    _check_collapses,
    _check_match_type,
    _add_payload,
)

# TODO : Threading support for pagination API. It's designed for Threading.


class Cdx:
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
        self.url = str(url).strip()
        self.user_agent = str(user_agent) if user_agent else default_user_agent
        self.start_timestamp = str(start_timestamp) if start_timestamp else None
        self.end_timestamp = str(end_timestamp) if end_timestamp else None
        self.filters = filters
        _check_filters(self.filters)
        self.match_type = str(match_type).strip() if match_type else None
        _check_match_type(self.match_type, self.url)
        self.gzip = gzip if gzip else True
        self.collapses = collapses
        _check_collapses(self.collapses)
        self.limit = limit if limit else 5000
        self.last_api_request_url = None
        self.use_page = False

    def cdx_api_manager(self, payload, headers, use_page=False):
        """
        We have two options to get the snapshots, we use this
        method to make a selection between pagination API and
        the normal one with Resumption Key, sequential querying
        of CDX data. For very large querying (for example domain query),
        it may be useful to perform queries in parallel and also estimate
        the total size of the query.

        read more about the pagination API at:
        https://web.archive.org/web/20201228063237/https://github.com/internetarchive/wayback/blob/master/wayback-cdx-server/README.md#pagination-api

        if use_page is false if will use the normal sequential query API,
        else use the pagination API.

        two mutually exclusive cases possible:

        1) pagination API is selected

            a) get the total number of pages to read, using _get_total_pages()

            b) then we use a for loop to get all the pages and yield the response text

        2) normal sequential query API is selected.

            a) get use showResumeKey=true to ask the API to add a query resumption key
               at the bottom of response

            b) check if the page has more than 3 lines, if not return the text

            c) if it has atleast three lines, we check the second last line for zero length.

            d) if the second last line has length zero than we assume that the last line contains
               the resumption key, we set the resumeKey and remove the resumeKey from text

            e) if the second line has non zero length we return the text as there will no resumption key

            f) if we find the resumption key we set the "more" variable status to True which is always set
               to False on each iteration. If more is not True the iteration stops and function returns.
        """

        endpoint = "https://web.archive.org/cdx/search/cdx"
        total_pages = _get_total_pages(self.url, self.user_agent)
        #If we only have two or less pages of archives then we care for accuracy
        # pagination API can be lagged sometimes
        if use_page == True and total_pages >= 2:
            blank_pages = 0
            for i in range(total_pages):
                payload["page"] = str(i)
                url, res = _get_response(
                    endpoint, params=payload, headers=headers, return_full_url=True
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

                url, res = _get_response(
                    endpoint, params=payload, headers=headers, return_full_url=True
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

    def snapshots(self):
        """
        This function yeilds snapshots encapsulated
        in CdxSnapshot for more usability.

        All the get request values are set if the conditions match

        And we use logic that if someone's only inputs don't have any
        of [start_timestamp, end_timestamp] and don't use any collapses
        then we use the pagination API as it returns archives starting
        from the first archive and the recent most archive will be on
        the last page.
        """
        payload = {}
        headers = {"User-Agent": self.user_agent}

        _add_payload(self, payload)

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

                # Making sure that we get the same number of
                # property values as the number of properties
                prop_values_len = len(prop_values)
                properties_len = len(properties)
                if prop_values_len != properties_len:
                    raise WaybackError(
                        "Snapshot returned by Cdx API has %s properties instead of expected %s properties.\nInvolved Snapshot : %s"
                        % (prop_values_len, properties_len, snapshot)
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

                yield CdxSnapshot(properties)
