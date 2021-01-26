import pytest
from waybackpy.cdx import Cdx
from waybackpy.exceptions import WaybackError


def test_all_cdx():
    url = "akamhy.github.io"
    user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, \
    like Gecko) Chrome/45.0.2454.85 Safari/537.36"
    cdx = Cdx(
        url=url,
        user_agent=user_agent,
        start_timestamp=2017,
        end_timestamp=2020,
        filters=[
            "statuscode:200",
            "mimetype:text/html",
            "timestamp:20201002182319",
            "original:https://akamhy.github.io/",
        ],
        gzip=False,
        collapses=["timestamp:10", "digest"],
        limit=50,
        match_type="prefix",
    )
    snapshots = cdx.snapshots()
    for snapshot in snapshots:
        ans = snapshot.archive_url
    assert "https://web.archive.org/web/20201002182319/https://akamhy.github.io/" == ans

    url = "akahfjgjkmhy.gihthub.ip"
    cdx = Cdx(
        url=url,
        user_agent=user_agent,
        start_timestamp=None,
        end_timestamp=None,
        filters=[],
        match_type=None,
        gzip=True,
        collapses=[],
        limit=10,
    )

    snapshots = cdx.snapshots()
    print(snapshots)
    i = 0
    for _ in snapshots:
        i += 1
    assert i == 0

    url = "https://github.com/akamhy/waybackpy/*"
    cdx = Cdx(url=url, user_agent=user_agent, limit=50)
    snapshots = cdx.snapshots()

    for snapshot in snapshots:
        print(snapshot.archive_url)

    url = "https://github.com/akamhy/waybackpy"
    with pytest.raises(WaybackError):
        cdx = Cdx(url=url, user_agent=user_agent, limit=50, filters=["ghddhfhj"])
        snapshots = cdx.snapshots()

    with pytest.raises(WaybackError):
        cdx = Cdx(url=url, user_agent=user_agent, collapses=["timestamp", "ghdd:hfhj"])
        snapshots = cdx.snapshots()

    url = "https://github.com"
    cdx = Cdx(url=url, user_agent=user_agent, limit=50)
    snapshots = cdx.snapshots()
    c = 0
    for snapshot in snapshots:
        c += 1
        if c > 100:
            break

    url = "https://github.com/*"
    cdx = Cdx(url=url, user_agent=user_agent, collapses=["timestamp"])
    snapshots = cdx.snapshots()
    c = 0
    for snapshot in snapshots:
        c += 1
        if c > 30529:  # deafult limit is 10k
            break

    url = "https://github.com/*"
    cdx = Cdx(url=url, user_agent=user_agent)
    c = 0
    snapshots = cdx.snapshots()

    for snapshot in snapshots:
        c += 1
        if c > 100529:
            break
