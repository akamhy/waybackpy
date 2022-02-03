from waybackpy.cdx_api import WaybackMachineCDXServerAPI


def test_a() -> None:
    user_agent = "Mozilla/5.0 (MacBook Air; M1 Mac OS X 11_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/604.1"
    url = "https://twitter.com/jack"

    wayback = WaybackMachineCDXServerAPI(
        url=url,
        user_agent=user_agent,
        match_type="prefix",
        collapses=["urlkey"],
        start_timestamp="201001",
        end_timestamp="201002",
    )
    #  timeframe bound prefix matching enabled along with active urlkey based collapsing

    snapshots = wayback.snapshots()  # <class 'generator'>

    for snapshot in snapshots:
        assert snapshot.timestamp.startswith("2010")


def test_b() -> None:
    user_agent = "Mozilla/5.0 (MacBook Air; M1 Mac OS X 11_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/604.1"
    url = "https://www.google.com"

    wayback = WaybackMachineCDXServerAPI(
        url=url, user_agent=user_agent, start_timestamp="202101", end_timestamp="202112"
    )
    #  timeframe bound prefix matching enabled along with active urlkey based collapsing

    snapshots = wayback.snapshots()  # <class 'generator'>

    for snapshot in snapshots:
        assert snapshot.timestamp.startswith("2021")
