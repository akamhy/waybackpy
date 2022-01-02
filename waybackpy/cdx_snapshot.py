from datetime import datetime


class CDXSnapshot:
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
        return "{urlkey} {timestamp} {original} {mimetype} {statuscode} {digest} {length}".format(
            urlkey=self.urlkey,
            timestamp=self.timestamp,
            original=self.original,
            mimetype=self.mimetype,
            statuscode=self.statuscode,
            digest=self.digest,
            length=self.length,
        )
