# -*- coding: utf-8 -*-

import re
from datetime import datetime, timedelta
from waybackpy.exceptions import WaybackError, URLError
from waybackpy.__version__ import __version__
import requests
import concurrent.futures


default_UA = "waybackpy python package - https://github.com/akamhy/waybackpy"


def _archive_url_parser(header):
    """Parse out the archive from header."""
    # Regex1
    arch = re.search(
        r"Content-Location: (/web/[0-9]{14}/.*)", str(header)
    )
    if arch:
        return "web.archive.org" + arch.group(1)
    # Regex2
    arch = re.search(
        r"rel=\"memento.*?(web\.archive\.org/web/[0-9]{14}/.*?)>", str(header)
    )
    if arch:
        return arch.group(1)
    # Regex3
    arch = re.search(r"X-Cache-Key:\shttps(.*)[A-Z]{2}", str(header))
    if arch:
        return arch.group(1)
    raise WaybackError(
        "No archive URL found in the API response. "
        "This version of waybackpy (%s) is likely out of date. Visit "
        "https://github.com/akamhy/waybackpy for the latest version "
        "of waybackpy.\nHeader:\n%s" % (__version__, str(header))
    )


def _wayback_timestamp(**kwargs):
    """Return a formatted timestamp."""
    return "".join(
        str(kwargs[key]).zfill(2) for key in ["year", "month", "day", "hour", "minute"]
    )


def _get_response(endpoint, params=None, headers=None):
    """Get response for the supplied request."""

    try:
        response = requests.get(endpoint, params=params, headers=headers)
    except Exception:
        try:
            response = requests.get(endpoint, params=params, headers=headers)  # nosec
        except Exception as e:
            exc = WaybackError("Error while retrieving %s" % req.full_url)
            exc.__cause__ = e
            raise exc
    return response


class Url:
    """waybackpy Url object"""

    def __init__(self, url, user_agent=default_UA):
        self.url = url
        self.user_agent = user_agent
        self._url_check()  # checks url validity on init.
        self.JSON = self._JSON()  # JSON of most recent archive
        self.archive_url = self._archive_url()  # URL of archive
        self.timestamp = self._archive_timestamp()  # timestamp for last archive
        self._alive_url_list = []

    def __repr__(self):
        return "waybackpy.Url(url=%s, user_agent=%s)" % (self.url, self.user_agent)

    def __str__(self):
        return "%s" % self.archive_url

    def __len__(self):
        td_max = timedelta(
            days=999999999,
            hours=23,
            minutes=59,
            seconds=59,
            microseconds=999999
        )
        if self.timestamp == datetime.max:
            return td_max.days
        else:
            diff = datetime.utcnow() - self.timestamp
            return diff.days

    def _url_check(self):
        """Check for common URL problems."""
        if "." not in self.url:
            raise URLError("'%s' is not a vaild URL." % self.url)

    def _JSON(self):
        endpoint = "https://archive.org/wayback/available"
        headers = {"User-Agent": "%s" % self.user_agent}
        payload = {"url": "%s" % self._clean_url()}
        response = _get_response(endpoint, params=payload, headers=headers)
        return response.json()

    def _archive_url(self):
        """Get URL of archive."""
        data = self.JSON

        if not data["archived_snapshots"]:
            archive_url = None
        else:
            archive_url = data["archived_snapshots"]["closest"]["url"]
            archive_url = archive_url.replace(
                "http://web.archive.org/web/",
                "https://web.archive.org/web/",
                1
            )

        return archive_url

    def _archive_timestamp(self):
        """Get timestamp of last archive."""
        data = self.JSON

        if not data["archived_snapshots"]:
            time = datetime.max

        else:
            time = datetime.strptime(data["archived_snapshots"]
                                     ["closest"]
                                     ["timestamp"],
                                     '%Y%m%d%H%M%S')

        return time

    def _clean_url(self):
        """Fix the URL, if possible."""
        return str(self.url).strip().replace(" ", "_")

    def save(self):
        """Create a new Wayback Machine archive for this URL."""
        request_url = "https://web.archive.org/save/" + self._clean_url()
        headers = {"User-Agent": "%s" % self.user_agent}
        response = _get_response(request_url, params=None, headers=headers)
        self.archive_url = "https://" + _archive_url_parser(response.headers)
        self.timestamp = datetime.utcnow()
        return self

    def get(self, url="", user_agent="", encoding=""):
        """Return the source code of the supplied URL.
        If encoding is not supplied, it is auto-detected from the response.
        """

        if not url:
            url = self._clean_url()

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
        """ Return the closest Wayback Machine archive to the time supplied.
            Supported params are year, month, day, hour and minute.
            Any non-supplied parameters default to the current time.

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
        payload = {"url": "%s" % self._clean_url(), "timestamp" : timestamp}
        response = _get_response(endpoint, params=payload, headers=headers)
        print(response.text)
        data = response.json()
        if not data["archived_snapshots"]:
            raise WaybackError(
                "Can not find archive for '%s' try later or use wayback.Url(url, user_agent).save() "
                "to create a new archive." % self._clean_url()
            )
        archive_url = data["archived_snapshots"]["closest"]["url"]
        archive_url = archive_url.replace(
            "http://web.archive.org/web/", "https://web.archive.org/web/", 1
        )

        self.archive_url = archive_url
        self.timestamp = datetime.strptime(data["archived_snapshots"]["closest"]["timestamp"], '%Y%m%d%H%M%S')

        return self

    def oldest(self, year=1994):
        """Return the oldest Wayback Machine archive for this URL."""
        return self.near(year=year)

    def newest(self):
        """Return the newest Wayback Machine archive available for this URL.

        Due to Wayback Machine database lag, this may not always be the
        most recent archive.
        """
        return self.near()

    def total_archives(self):
        """Returns the total number of Wayback Machine archives for this URL."""

        endpoint = "https://web.archive.org/cdx/search/cdx"
        headers = {"User-Agent": "%s" % self.user_agent, "output" : "json", "fl" : "statuscode"}
        payload = {"url": "%s" % self._clean_url()}
        response = _get_response(endpoint, params=payload, headers=headers)

        # Most efficient method to count number of archives (yet)
        return response.text.count(",")

    def pick_live_urls(self, url):

        try:
            response_code = requests.get(url).status_code
        except Exception:
            return  # we don't care if urls are not opening

        # 200s are OK and 300s are usually redirects, if you don't want redirects replace 400 with 300
        if response_code >= 400:
            return

        self._alive_url_list.append(url)

    def known_urls(self, alive=False, subdomain=False):
        """Returns list of URLs known to exist for given domain name
        because these URLs were crawled by WayBack Machine bots.
        Useful for pen-testers and others.
        Idea by Mohammed Diaa (https://github.com/mhmdiaa) from:
        https://gist.github.com/mhmdiaa/adf6bff70142e5091792841d4b372050
        """

        url_list = []

        if subdomain:
            request_url = (
                "https://web.archive.org/cdx/search/cdx?url=*.%s/*&output=json&fl=original&collapse=urlkey" % self._clean_url()
            )
        else:
            request_url = (
                "http://web.archive.org/cdx/search/cdx?url=%s/*&output=json&fl=original&collapse=urlkey" % self._clean_url()
            )

        headers = {"User-Agent": "%s" % self.user_agent}
        response = _get_response(request_url, params=None, headers=headers)
        data = response.json()
        url_list = [y[0] for y in data if y[0] != "original"]

        # Remove all deadURLs from url_list if alive=True
        if alive:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                executor.map(self.pick_live_urls, url_list)
            url_list = self._alive_url_list

        return url_list
