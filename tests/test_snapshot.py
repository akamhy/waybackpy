import pytest

from waybackpy.snapshot import CdxSnapshot, datetime


def test_CdxSnapshot():
    sample_input = "org,archive)/ 20080126045828 http://github.com text/html 200 Q4YULN754FHV2U6Q5JUT6Q2P57WEWNNY 1415"
    (
        urlkey,
        timestamp,
        original,
        mimetype,
        statuscode,
        digest,
        length,
    ) = sample_input.split(" ")

    snapshot = CdxSnapshot(
        urlkey, timestamp, original, mimetype, statuscode, digest, length
    )

    assert urlkey == snapshot.urlkey
    assert timestamp == snapshot.timestamp
    assert original == snapshot.original
    assert mimetype == snapshot.mimetype
    assert statuscode == snapshot.statuscode
    assert digest == snapshot.digest
    assert length == snapshot.length
    assert datetime.strptime(timestamp, "%Y%m%d%H%M%S") == snapshot.datetime_timestamp
    archive_url = "https://web.archive.org/web/" + timestamp + "/" + original
    assert archive_url == snapshot.archive_url
    assert archive_url == str(snapshot)
