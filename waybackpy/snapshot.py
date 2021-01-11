from datetime import datetime


class CdxSnapshot:
    """
    This class helps to use the Cdx Snapshots easily.

    Raw Snapshot data looks like:
    org,archive)/ 20080126045828 http://github.com text/html 200 Q4YULN754FHV2U6Q5JUT6Q2P57WEWNNY 1415

    properties is a dict containg all of the 7 cdx snapshot properties.
    """

    def __init__(self, properties):
        self.urlkey = properties["urlkey"]
        self.timestamp = properties["timestamp"]
        self.datetime_timestamp = datetime.strptime(self.timestamp, "%Y%m%d%H%M%S")
        self.original = properties["original"]
        self.mimetype = properties["mimetype"]
        self.statuscode = properties["statuscode"]
        self.digest = properties["digest"]
        self.length = properties["length"]
        self.archive_url = (
            "https://web.archive.org/web/" + self.timestamp + "/" + self.original
        )

    def __str__(self):
        return ("%s %s %s %s %s %s %s") % (
            self.urlkey,
            self.timestamp,
            self.original,
            self.mimetype,
            self.statuscode,
            self.digest,
            self.length,
        )
