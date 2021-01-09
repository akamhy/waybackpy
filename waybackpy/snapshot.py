from datetime import datetime


class CdxSnapshot:
    """
    This class helps to handle the Cdx Snapshots easily.

    What the raw data looks like:
    org,archive)/ 20080126045828 http://github.com text/html 200 Q4YULN754FHV2U6Q5JUT6Q2P57WEWNNY 1415
    """

    def __init__(
        self, urlkey, timestamp, original, mimetype, statuscode, digest, length
    ):
        self.urlkey = urlkey
        self.timestamp = timestamp
        self.datetime_timestamp = datetime.strptime(timestamp, "%Y%m%d%H%M%S")
        self.original = original
        self.mimetype = mimetype
        self.statuscode = statuscode
        self.digest = digest
        self.length = length
        self.archive_url = "https://web.archive.org/web/" + timestamp + "/" + original

    def __str__(self):
        return self.archive_url
