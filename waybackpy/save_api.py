import re
import time
import requests

from datetime import datetime
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

from .utils import DEFAULT_USER_AGENT
from .exceptions import MaximumSaveRetriesExceeded


class WaybackMachineSaveAPI:

    """
    WaybackMachineSaveAPI class provides an interface for saving URLs on the
    Wayback Machine.
    """

    def __init__(self, url, user_agent=DEFAULT_USER_AGENT, max_tries=8):
        self.url = str(url).strip().replace(" ", "%20")
        self.request_url = "https://web.archive.org/save/" + self.url
        self.user_agent = user_agent
        self.request_headers = {"User-Agent": self.user_agent}
        self.max_tries = max_tries
        self.total_save_retries = 5
        self.backoff_factor = 0.5
        self.status_forcelist = [500, 502, 503, 504]
        self._archive_url = None
        self.instance_birth_time = datetime.utcnow()

    @property
    def archive_url(self):

        if self._archive_url:
            return self._archive_url
        else:
            return self.save()

    def get_save_request_headers(self):

        session = requests.Session()
        retries = Retry(
            total=self.total_save_retries,
            backoff_factor=self.backoff_factor,
            status_forcelist=self.status_forcelist,
        )
        session.mount("https://", HTTPAdapter(max_retries=retries))
        self.response = session.get(self.request_url, headers=self.request_headers)
        self.headers = self.response.headers
        self.status_code = self.response.status_code
        self.response_url = self.response.url

    def archive_url_parser(self):

        regex1 = r"Content-Location: (/web/[0-9]{14}/.*)"
        match = re.search(regex1, str(self.headers))
        if match:
            return "https://web.archive.org" + match.group(1)

        regex2 = r"rel=\"memento.*?(web\.archive\.org/web/[0-9]{14}/.*?)>"
        match = re.search(regex2, str(self.headers))
        if match:
            return "https://" + match.group(1)

        regex3 = r"X-Cache-Key:\shttps(.*)[A-Z]{2}"
        match = re.search(regex3, str(self.headers))
        if match:
            return "https://" + match.group(1)

        if self.response_url:
            self.response_url = self.response_url.strip()
            if "web.archive.org/web" in self.response_url:
                regex = r"web\.archive\.org/web/(?:[0-9]*?)/(?:.*)$"
                match = re.search(regex, self.response_url)
                if match:
                    return "https://" + match.group(0)

    def sleep(self, tries):

        sleep_seconds = 5
        if tries % 3 == 0:
            sleep_seconds = 10
        time.sleep(sleep_seconds)

    def timestamp(self):
        m = re.search(
            r"https?://web.archive.org/web/([0-9]{14})/http", self._archive_url
        )
        string_timestamp = m.group(1)
        timestamp = datetime.strptime(string_timestamp, "%Y%m%d%H%M%S")

        timestamp_unixtime = time.mktime(timestamp.timetuple())
        instance_birth_time_unixtime = time.mktime(self.instance_birth_time.timetuple())

        if timestamp_unixtime < instance_birth_time_unixtime:
            self.cached_save = True
        else:
            self.cached_save = False

        return timestamp

    def save(self):

        saved_archive = None
        tries = 0

        while True:

            tries += 1

            if tries >= self.max_tries:
                raise MaximumSaveRetriesExceeded(
                    "Tried %s times but failed to save and return the archive for %s.\nResponse URL:\n%s \nResponse Header:\n%s\n"
                    % (str(tries), self.url, self.response_url, str(self.headers)),
                )

            if not saved_archive:

                if tries > 1:
                    self.sleep(tries)

                self.get_save_request_headers()
                saved_archive = self.archive_url_parser()

                if not saved_archive:
                    continue
                else:
                    self._archive_url = saved_archive
                    self.timestamp()
                    return saved_archive
