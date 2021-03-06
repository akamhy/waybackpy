from datetime import datetime


class CdxSnapshot:
    """
    This class encapsulates the snapshots for greater usability.

    Raw Snapshot data looks like:
    org,archive)/ 20080126045828 http://github.com text/html 200 Q4YULN754FHV2U6Q5JUT6Q2P57WEWNNY 1415

    """

    def __init__(self, properties):
        """
        Parameters
        ----------
        self : waybackpy.snapshot.CdxSnapshot
            The instance itself

        properties : dict
            Properties is a dict containg all of the 7 cdx snapshot properties.

        """
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
        """Returns the Cdx snapshot line.

        Output format:
        org,archive)/ 20080126045828 http://github.com text/html 200 Q4YULN754FHV2U6Q5JUT6Q2P57WEWNNY 1415

        """
        return "{urlkey} {timestamp} {original} {mimetype} {statuscode} {digest} {length}".format(
            urlkey=self.urlkey,
            timestamp=self.timestamp,
            original=self.original,
            mimetype=self.mimetype,
            statuscode=self.statuscode,
            digest=self.digest,
            length=self.length,
        )
