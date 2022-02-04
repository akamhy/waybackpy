from datetime import datetime
from typing import Dict


class CDXSnapshot(object):
    """
    Class for the CDX snapshot lines returned by the CDX API,
    Each valid line of the CDX API is casted to an CDXSnapshot object
    by the CDX API interface.
    This provides the end-user the ease of using the data as attributes
    of the CDXSnapshot.
    """

    def __init__(self, properties: Dict[str, str]) -> None:
        self.urlkey = properties["urlkey"]
        self.timestamp = properties["timestamp"]
        self.datetime_timestamp = datetime.strptime(self.timestamp, "%Y%m%d%H%M%S")
        self.original = properties["original"]
        self.mimetype = properties["mimetype"]
        self.statuscode = properties["statuscode"]
        self.digest = properties["digest"]
        self.length = properties["length"]
        self.archive_url = (
            f"https://web.archive.org/web/{self.timestamp}/{self.original}"
        )

    def __str__(self) -> str:
        return (
            f"{self.urlkey} {self.timestamp} {self.original} "
            f"{self.mimetype} {self.statuscode} {self.digest} {self.length}"
        )
