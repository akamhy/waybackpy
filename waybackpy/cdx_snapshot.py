"""
Module that contains the CDXSnapshot class, CDX records/lines are casted
to CDXSnapshot objects for easier access.

The CDX index format is plain text data. Each line ('record') indicates a
crawled document. And these lines are casted to CDXSnapshot.
"""


from datetime import datetime
from typing import Dict


class CDXSnapshot:
    """
    Class for the CDX snapshot lines('record') returned by the CDX API,
    Each valid line of the CDX API is casted to an CDXSnapshot object
    by the CDX API interface, just use "." to access any attribute of the
    CDX server API snapshot.

    This provides the end-user the ease of using the data as attributes
    of the CDXSnapshot.

    The string representation of the class is identical to the line returned
    by the CDX server API.

    Besides all the attributes of the CDX server API this class also provides
    archive_url attribute, yes it is the archive url of the snapshot.

    Attributes of the this class and what they represents and are useful for:

    urlkey: The document captured, expressed as a SURT
            SURT stands for Sort-friendly URI Reordering Transform, and is a
            transformation applied to URIs which makes their left-to-right
            representation better match the natural hierarchy of domain names.
            A URI <scheme://domain.tld/path?query> has SURT
            form <scheme://(tld,domain,)/path?query>.

    timestamp: The timestamp of the archive, format is yyyyMMddhhmmss and type
               is string.

    datetime_timestamp: The timestamp as a datetime object.

    original: The original URL of the archive. If archive_url is
    https://web.archive.org/web/20220113130051/https://google.com then the
    original URL is https://google.com

    mimetype: The document’s file type. e.g. text/html

    statuscode: HTTP response code for the document at the time of its crawling

    digest: Base32-encoded SHA-1 checksum of the document for discriminating
            with others

    length: Document’s volume of bytes in the WARC file

    archive_url: The archive url of the snapshot, this is not returned by the
                 CDX server API but created by this class on init.
    """

    def __init__(self, properties: Dict[str, str]) -> None:
        self.urlkey: str = properties["urlkey"]
        self.timestamp: str = properties["timestamp"]
        self.datetime_timestamp: datetime = datetime.strptime(
            self.timestamp, "%Y%m%d%H%M%S"
        )
        self.original: str = properties["original"]
        self.mimetype: str = properties["mimetype"]
        self.statuscode: str = properties["statuscode"]
        self.digest: str = properties["digest"]
        self.length: str = properties["length"]
        self.archive_url: str = (
            f"https://web.archive.org/web/{self.timestamp}/{self.original}"
        )

    def __repr__(self) -> str:
        """
        Same as __str__()
        """
        return str(self)

    def __str__(self) -> str:
        """
        The string representation is same as the line returned by the
        CDX server API for the snapshot.
        """
        return (
            f"{self.urlkey} {self.timestamp} {self.original} "
            f"{self.mimetype} {self.statuscode} {self.digest} {self.length}"
        )
