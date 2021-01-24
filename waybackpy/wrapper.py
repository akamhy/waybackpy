import re
from datetime import datetime, timedelta
from .exceptions import WaybackError
from .cdx import Cdx
from .utils import (
    _archive_url_parser,
    _wayback_timestamp,
    _get_response,
    default_user_agent,
    _url_check,
    _cleaned_url,
    _ts,
    _unix_ts_to_wayback_ts,
    _latest_version,
)


class Url:
    def __init__(self, url, user_agent=default_user_agent):
        self.url = url
        self.user_agent = str(user_agent)
        _url_check(self.url)
        self._archive_url = None
        self.timestamp = None
        self._JSON = None
        self.latest_version = None
        self.cached_save = False

    def __repr__(self):
        return "waybackpy.Url(url={url}, user_agent={user_agent})".format(
            url=self.url, user_agent=self.user_agent
        )

    def __str__(self):
        """
        Output when print() is used on <class 'waybackpy.wrapper.Url'>
        This should print an archive URL.

        We check if self._archive_url is not None.
        If not None, good. We return string of self._archive_url.

        If self._archive_url is None, it means we ain't used any method that
        sets self._archive_url, we now set self._archive_url to self.archive_url
        and return it.
        """

        if not self._archive_url:
            self._archive_url = self.archive_url
        return "{archive_url}".format(archive_url=self._archive_url)

    def __len__(self):
        """
        Why do we have len here?

        Applying len() on <class 'waybackpy.wrapper.Url'>
        will calculate the number of days between today and
        the archive timestamp.

        Can be applied on return values of near and its
        childs (e.g. oldest) and if applied on waybackpy.Url()
        whithout using any functions, it just grabs
        self._timestamp and def _timestamp gets it
        from def JSON.
        """
        td_max = timedelta(
            days=999999999, hours=23, minutes=59, seconds=59, microseconds=999999
        )

        if not self.timestamp:
            self.timestamp = self._timestamp

        if self.timestamp == datetime.max:
            return td_max.days

        return (datetime.utcnow() - self.timestamp).days

    @property
    def JSON(self):
        """
        If the end user has used near() or its childs like oldest, newest
        and archive_url then the JSON response of these are cached in self._JSON

        If we find that self._JSON is not None we return it.
        else we get the response of 'https://archive.org/wayback/available?url=YOUR-URL'
        and return it.
        """

        if self._JSON:
            return self._JSON

        endpoint = "https://archive.org/wayback/available"
        headers = {"User-Agent": self.user_agent}
        payload = {"url": "{url}".format(url=_cleaned_url(self.url))}
        response = _get_response(endpoint, params=payload, headers=headers)
        return response.json()

    @property
    def archive_url(self):
        """
        Returns any random archive for the instance.
        But if near, oldest, newest were used before
        then it returns the same archive again.

        We cache archive in self._archive_url
        """

        if self._archive_url:
            return self._archive_url

        data = self.JSON

        if not data["archived_snapshots"]:
            archive_url = None
        else:
            archive_url = data["archived_snapshots"]["closest"]["url"]
            archive_url = archive_url.replace(
                "http://web.archive.org/web/", "https://web.archive.org/web/", 1
            )
        self._archive_url = archive_url
        return archive_url

    @property
    def _timestamp(self):
        self.timestamp = _ts(self.timestamp, self.JSON)
        return self.timestamp

    def save(self):
        """
        To save a webpage on WayBack machine we
        need to send get request to https://web.archive.org/save/

        And to get the archive URL we are required to read the
        header of the API response.

        _get_response() takes care of the get requests.

        _archive_url_parser() parses the archive from the header.

        """
        request_url = "https://web.archive.org/save/" + _cleaned_url(self.url)
        headers = {"User-Agent": self.user_agent}

        response = _get_response(
            request_url,
            params=None,
            headers=headers,
            backoff_factor=2,
            no_raise_on_redirects=True,
        )

        if not self.latest_version:
            self.latest_version = _latest_version("waybackpy", headers=headers)
        if response:
            res_headers = response.headers
        else:
            res_headers = "save redirected"
        self._archive_url = "https://" + _archive_url_parser(
            res_headers,
            self.url,
            latest_version=self.latest_version,
            instance=self,
        )

        m = re.search(r"https?://web.archive.org/web/([0-9]{14})/http", self._archive_url)
        str_ts = m.group(1)
        ts = datetime.strptime(str_ts, "%Y%m%d%H%M%S")
        now = datetime.utcnow()
        total_seconds = int((now - ts).total_seconds())

        if total_seconds > 60 * 3:
            self.cached_save = True

        self.timestamp = ts

        return self

    def get(self, url="", user_agent="", encoding=""):
        """
        Return the source code of the last archived URL,
        if no URL is passed to this method.

        If encoding is not supplied, it is auto-detected
         from the response itself by requests package.
        """

        if not url and self._archive_url:
            url = self._archive_url

        elif not url and not self._archive_url:
            url = _cleaned_url(self.url)

        if not user_agent:
            user_agent = self.user_agent

        headers = {"User-Agent": str(user_agent)}
        response = _get_response(str(url), params=None, headers=headers)

        if not encoding:
            try:
                encoding = response.encoding
            except AttributeError:
                encoding = "UTF-8"

        return response.content.decode(encoding.replace("text/html", "UTF-8", 1))

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
        Wayback Machine can have many archives of a webpage,
        sometimes we want archive close to a specific time.

        This method takes year, month, day, hour and minute as input.
        The input type must be integer. Any non-supplied parameters
        default to the current time.

        We convert the input to a wayback machine timestamp using
        _wayback_timestamp(), it returns a string.

        We use the wayback machine's availability API
        (https://archive.org/wayback/available)
        to get the closest archive from the timestamp.

        We set self._archive_url to the archive found, if any.
        If archive found, we set self.timestamp to its timestamp.
        We self._JSON to the response of the availability API.

        And finally return self.
        """

        if unix_timestamp:
            timestamp = _unix_ts_to_wayback_ts(unix_timestamp)
        else:
            now = datetime.utcnow().timetuple()
            timestamp = _wayback_timestamp(
                year=year if year else now.tm_year,
                month=month if month else now.tm_mon,
                day=day if day else now.tm_mday,
                hour=hour if hour else now.tm_hour,
                minute=minute if minute else now.tm_min,
            )

        endpoint = "https://archive.org/wayback/available"
        headers = {"User-Agent": self.user_agent}
        payload = {
            "url": "{url}".format(url=_cleaned_url(self.url)),
            "timestamp": timestamp,
        }
        response = _get_response(endpoint, params=payload, headers=headers)
        data = response.json()

        if not data["archived_snapshots"]:
            raise WaybackError(
                "Can not find archive for '{url}' try later or use wayback.Url(url, user_agent).save() "
                "to create a new archive.\nAPI response:\n{text}".format(
                    url=_cleaned_url(self.url), text=response.text
                )
            )
        archive_url = data["archived_snapshots"]["closest"]["url"]
        archive_url = archive_url.replace(
            "http://web.archive.org/web/", "https://web.archive.org/web/", 1
        )

        self._archive_url = archive_url
        self.timestamp = datetime.strptime(
            data["archived_snapshots"]["closest"]["timestamp"], "%Y%m%d%H%M%S"
        )
        self._JSON = data

        return self

    def oldest(self, year=1994):
        """
        Returns the earliest/oldest Wayback Machine archive for the webpage.

        Wayback machine has started archiving the internet around 1997 and
        therefore we can't have any archive older than 1997, we use 1994 as the
        deafult year to look for the oldest archive.

        We simply pass the year in near() and return it.
        """
        return self.near(year=year)

    def newest(self):
        """
        Return the newest Wayback Machine archive available for this URL.

        We return the output of self.near() as it deafults to current utc time.

        Due to Wayback Machine database lag, this may not always be the
        most recent archive.
        """
        return self.near()

    def total_archives(self, start_timestamp=None, end_timestamp=None):
        """
        A webpage can have multiple archives on the wayback machine
        If someone wants to count the total number of archives of a
        webpage on wayback machine they can use this method.

        Returns the total number of Wayback Machine archives for the URL.

        Return type in integer.
        """

        cdx = Cdx(
            _cleaned_url(self.url),
            user_agent=self.user_agent,
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp,
        )
        i = 0
        for _ in cdx.snapshots():
            i = i + 1
        return i

    def known_urls(
        self,
        subdomain=False,
        host=False,
        start_timestamp=None,
        end_timestamp=None,
        match_type="prefix",
    ):
        """
        Yields list of URLs known to exist for given input.
        Defaults to input URL as prefix.

        This method is kept for compatibility, use the Cdx class instead.
        This method itself depends on Cdx.

         Idea by Mohammed Diaa (https://github.com/mhmdiaa) from:
         https://gist.github.com/mhmdiaa/adf6bff70142e5091792841d4b372050
        """

        if subdomain:
            match_type = "domain"
        if host:
            match_type = "host"

        cdx = Cdx(
            _cleaned_url(self.url),
            user_agent=self.user_agent,
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp,
            match_type=match_type,
            collapses=["urlkey"],
        )

        snapshots = cdx.snapshots()

        for snapshot in snapshots:
            yield (snapshot.original)
