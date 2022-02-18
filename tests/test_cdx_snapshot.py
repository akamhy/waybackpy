from datetime import datetime

from waybackpy.cdx_snapshot import CDXSnapshot


def test_CDXSnapshot() -> None:
    sample_input = (
        "org,archive)/ 20080126045828 http://github.com "
        "text/html 200 Q4YULN754FHV2U6Q5JUT6Q2P57WEWNNY 1415"
    )
    prop_values = sample_input.split(" ")
    properties = {}
    (
        properties["urlkey"],
        properties["timestamp"],
        properties["original"],
        properties["mimetype"],
        properties["statuscode"],
        properties["digest"],
        properties["length"],
    ) = prop_values

    snapshot = CDXSnapshot(properties)

    assert properties["urlkey"] == snapshot.urlkey
    assert properties["timestamp"] == snapshot.timestamp
    assert properties["original"] == snapshot.original
    assert properties["mimetype"] == snapshot.mimetype
    assert properties["statuscode"] == snapshot.statuscode
    assert properties["digest"] == snapshot.digest
    assert properties["length"] == snapshot.length
    assert (
        datetime.strptime(properties["timestamp"], "%Y%m%d%H%M%S")
        == snapshot.datetime_timestamp
    )
    archive_url = (
        "https://web.archive.org/web/"
        + properties["timestamp"]
        + "/"
        + properties["original"]
    )
    assert archive_url == snapshot.archive_url
    assert sample_input == str(snapshot)
    assert sample_input == repr(snapshot)
