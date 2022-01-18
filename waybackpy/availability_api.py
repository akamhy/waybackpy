import re
import time
import requests
from datetime import datetime
from .__version__ import __version__
from .utils import DEFAULT_USER_AGENT


def full_url(endpoint, params):
    if not params:
        return endpoint.strip()

    full_url = endpoint if endpoint.endswith("?") else (endpoint + "?")

    for key, val in params.items():
        key = "filter" if key.startswith("filter") else key
        key = "collapse" if key.startswith("collapse") else key
        amp = "" if full_url.endswith("?") else "&"
        full_url = (
            full_url
            + amp
            + "{key}={val}".format(key=key, val=requests.utils.quote(str(val)))
        )
    return full_url


class WaybackMachineAvailabilityAPI:
    def __init__(self, url, user_agent=DEFAULT_USER_AGENT):
        self.url = str(url).strip().replace(" ", "%20")
        self.user_agent = user_agent
        self.headers = {"User-Agent": self.user_agent}
        self.payload = {"url": "{url}".format(url=self.url)}
        self.endpoint = "https://archive.org/wayback/available"
        self.JSON = None

    def unix_timestamp_to_wayback_timestamp(self, unix_timestamp):
        return datetime.utcfromtimestamp(int(unix_timestamp)).strftime("%Y%m%d%H%M%S")

    def __repr__(self):
        return str(self)  # self.__str__()

    def __str__(self):
        if not self.JSON:
            return None
        return self.archive_url

    def json(self):
        self.request_url = full_url(self.endpoint, self.payload)
        self.response = requests.get(self.request_url, self.headers)
        self.JSON = self.response.json()
        return self.JSON

    def timestamp(self):
        if not self.JSON["archived_snapshots"] or not self.JSON:
            return datetime.max

        return datetime.strptime(
            self.JSON["archived_snapshots"]["closest"]["timestamp"], "%Y%m%d%H%M%S"
        )

    @property
    def archive_url(self):
        data = self.JSON

        if not data["archived_snapshots"]:
            archive_url = None
        else:
            archive_url = data["archived_snapshots"]["closest"]["url"]
            archive_url = archive_url.replace(
                "http://web.archive.org/web/", "https://web.archive.org/web/", 1
            )
        return archive_url

    def wayback_timestamp(self, **kwargs):
        return "".join(
            str(kwargs[key]).zfill(2)
            for key in ["year", "month", "day", "hour", "minute"]
        )

    def oldest(self):
        return self.near(year=1994)

    def newest(self):
        return self.near(unix_timestamp=int(time.time()))

    def near(
        self,
        year=None,
        month=None,
        day=None,
        hour=None,
        minute=None,
        unix_timestamp=None,
    ):
        if unix_timestamp:
            timestamp = self.unix_timestamp_to_wayback_timestamp(unix_timestamp)
        else:
            now = datetime.utcnow().timetuple()
            timestamp = self.wayback_timestamp(
                year=year if year else now.tm_year,
                month=month if month else now.tm_mon,
                day=day if day else now.tm_mday,
                hour=hour if hour else now.tm_hour,
                minute=minute if minute else now.tm_min,
            )

        self.payload["timestamp"] = timestamp
        self.json()
        return self
