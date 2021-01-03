import re
import requests
import concurrent.futures
from datetime import datetime, timedelta
from waybackpy.__version__ import __version__
from waybackpy.exceptions import WaybackError, URLError


default_user_agent = "waybackpy python package - https://github.com/akamhy/waybackpy"


def _archive_url_parser(header, url):
    """
    The wayback machine's save API doesn't
    return JSON response, we are required
    to read the header of the API response
    and look for the archive URL.

    This method has some regexen (or regexes)
    that search for archive url in header.

    This method is used when you try to
    save a webpage on wayback machine.

    Two cases are possible:
    1) Either we find the archive url in
       the header.

    2) Or we didn't find the archive url in
       API header.

    If we found the archive URL we return it.

    And if we couldn't find it, we raise
    WaybackError with an error message.
    """

    # Regex1
    m = re.search(r"Content-Location: (/web/[0-9]{14}/.*)", str(header))
    if m:
        return "web.archive.org" + m.group(1)

    # Regex2
    m = re.search(
        r"rel=\"memento.*?(web\.archive\.org/web/[0-9]{14}/.*?)>", str(header)
    )
    if m:
        return m.group(1)

    # Regex3
    m = re.search(r"X-Cache-Key:\shttps(.*)[A-Z]{2}", str(header))
    if m:
        return m.group(1)

    raise WaybackError(
        "No archive URL found in the API response. "
        "If '%s' can be accessed via your web browser then either "
        "this version of waybackpy (%s) is out of date or WayBack Machine is malfunctioning. Visit "
        "'https://github.com/akamhy/waybackpy' for the latest version "
        "of waybackpy.\nHeader:\n%s" % (url, __version__, str(header))
    )


def _wayback_timestamp(**kwargs):
    """
    Wayback Machine archive URLs
    have a timestamp in them.

    The standard archive URL format is
    https://web.archive.org/web/20191214041711/https://www.youtube.com

    If we break it down in three parts:
    1 ) The start (https://web.archive.org/web/)
    2 ) timestamp (20191214041711)
    3 ) https://www.youtube.com, the original URL

    The near method takes year, month, day, hour and minute
    as Arguments, their type is int.

    This method takes those integers and converts it to
    wayback machine timestamp and returns it.

    Return format is string.
    """

    return "".join(
        str(kwargs[key]).zfill(2) for key in ["year", "month", "day", "hour", "minute"]
    )


def _get_response(endpoint, params=None, headers=None):
    """
    This function is used make get request.
    We use the requests package to make the
    requests.


    We try twice and if both the times is fails And
    raises exceptions we give-up and raise WaybackError.

    You can handles WaybackError by importing:
    from waybackpy.exceptions import WaybackError

    try:
        ...
    except WaybackError as e:
        # handle it
    """

    try:
        return requests.get(endpoint, params=params, headers=headers)
    except Exception:
        try:
            return requests.get(endpoint, params=params, headers=headers)
        except Exception as e:
            exc = WaybackError("Error while retrieving %s" % endpoint)
            exc.__cause__ = e
            raise exc


class Url:
    """
    waybackpy Url object, Type : <class 'waybackpy.wrapper.Url'>
    """

    def __init__(self, url, user_agent=default_user_agent):
        self.url = url
        self.user_agent = user_agent
        self._url_check()
        self._archive_url = None
        self.timestamp = None
        self._JSON = None
        self._alive_url_list = []

    def __repr__(self):
        return "waybackpy.Url(url=%s, user_agent=%s)" % (self.url, self.user_agent)

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
        return "%s" % self._archive_url

    def __len__(self):
        td_max = timedelta(
            days=999999999, hours=23, minutes=59, seconds=59, microseconds=999999
        )

        if not self.timestamp:
            self.timestamp = self._timestamp

        if self.timestamp == datetime.max:
            return td_max.days

        return (datetime.utcnow() - self.timestamp).days

    def _url_check(self):
        """
        Check for common URL problems.
        What we are checking:
        1) '.' in self.url, no url that ain't '.' in it.

        If you known any others, please create a PR on the github repo.
        """

        if "." not in self.url:
            raise URLError("'%s' is not a vaild URL." % self.url)

    @property
    def JSON(self):
        """
        Returns JSON data from 'https://archive.org/wayback/available?url=YOUR-URL'.
        """

        if self._JSON:
            return self._JSON

        endpoint = "https://archive.org/wayback/available"
        headers = {"User-Agent": "%s" % self.user_agent}
        payload = {"url": "%s" % self._cleaned_url()}
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
        """
        Get timestamp of last fetched archive.
        If used before fetching any archive, This
        randomly picks archive.
        """

        if self.timestamp:
            return self.timestamp

        data = self.JSON

        if not data["archived_snapshots"]:
            ts = datetime.max

        else:
            ts = datetime.strptime(
                data["archived_snapshots"]["closest"]["timestamp"], "%Y%m%d%H%M%S"
            )
        self.timestamp = ts
        return ts

    def _cleaned_url(self):
        """
        Remove newlines
        replace " " with "_"
        """
        return str(self.url).strip().replace(" ", "_")

    def save(self):
        """Create a new Wayback Machine archive for this URL."""
        request_url = "https://web.archive.org/save/" + self._cleaned_url()
        headers = {"User-Agent": "%s" % self.user_agent}
        response = _get_response(request_url, params=None, headers=headers)
        self._archive_url = "https://" + _archive_url_parser(response.headers, self.url)
        self.timestamp = datetime.utcnow()
        return self

    def get(self, url="", user_agent="", encoding=""):
        """Return the source code of the supplied URL.
        If encoding is not supplied, it is auto-detected from the response.
        """

        if not url:
            url = self._cleaned_url()

        if not user_agent:
            user_agent = self.user_agent

        headers = {"User-Agent": "%s" % self.user_agent}
        response = _get_response(url, params=None, headers=headers)

        if not encoding:
            try:
                encoding = response.encoding
            except AttributeError:
                encoding = "UTF-8"

        return response.content.decode(encoding.replace("text/html", "UTF-8", 1))

    def near(self, year=None, month=None, day=None, hour=None, minute=None):
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
        now = datetime.utcnow().timetuple()
        timestamp = _wayback_timestamp(
            year=year if year else now.tm_year,
            month=month if month else now.tm_mon,
            day=day if day else now.tm_mday,
            hour=hour if hour else now.tm_hour,
            minute=minute if minute else now.tm_min,
        )

        endpoint = "https://archive.org/wayback/available"
        headers = {"User-Agent": "%s" % self.user_agent}
        payload = {"url": "%s" % self._cleaned_url(), "timestamp": timestamp}
        response = _get_response(endpoint, params=payload, headers=headers)
        data = response.json()

        if not data["archived_snapshots"]:
            raise WaybackError(
                "Can not find archive for '%s' try later or use wayback.Url(url, user_agent).save() "
                "to create a new archive." % self._cleaned_url()
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

    def total_archives(self):
        """
        A webpage can have multiple archives on the wayback machine
        If someone wants to count the total number of archives of a
        webpage on wayback machine they can use this method.

        Returns the total number of Wayback Machine archives for the URL.

        Return type in integer.
        """
        total_pages_url = (
            "https://web.archive.org/cdx/search/cdx?url=%s&showNumPages=true"
            % self._cleaned_url()
        )
        headers = {"User-Agent": "%s" % self.user_agent}
        total_pages = int(
            (_get_response(total_pages_url, headers=headers).text).strip()
        )

        archive_count = 0
        for i in range(total_pages):
            page_url = "https://web.archive.org/cdx/search/cdx?url=%s&page=%s" % (
                self._cleaned_url(),
                str(i),
            )
            count = str(_get_response(page_url, headers=headers).text).count("\n")
            archive_count = archive_count + count
        return archive_count

    def live_urls_picker(self, url):
        """
        This method is used to check if supplied url
        is >= 400.
        """

        try:
            response_code = requests.get(url).status_code
        except Exception:
            return  # we don't care if Exception

        # 200s are OK and 300s are usually redirects, if you don't want redirects replace 400 with 300
        if response_code >= 400:
            return

        self._alive_url_list.append(url)

    def known_urls(self, alive=False, subdomain=False):
        """
        Returns list of URLs known to exist for given domain name
        because these URLs were crawled by WayBack Machine bots.
        Useful for pen-testers and others.
        Idea by Mohammed Diaa (https://github.com/mhmdiaa) from:
        https://gist.github.com/mhmdiaa/adf6bff70142e5091792841d4b372050
        """

        url_list = []

        if subdomain:
            request_url = (
                "https://web.archive.org/cdx/search/cdx?url=*.%s/*&output=json&fl=original&collapse=urlkey"
                % self._cleaned_url()
            )
        else:
            request_url = (
                "http://web.archive.org/cdx/search/cdx?url=%s/*&output=json&fl=original&collapse=urlkey"
                % self._cleaned_url()
            )

        headers = {"User-Agent": "%s" % self.user_agent}
        response = _get_response(request_url, params=None, headers=headers)
        data = response.json()
        url_list = [y[0] for y in data if y[0] != "original"]

        # Remove all deadURLs from url_list if alive=True
        if alive:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                executor.map(self.live_urls_picker, url_list)
            url_list = self._alive_url_list

        return url_list
