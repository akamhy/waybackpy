from waybackpy.wrapper import Url


def test_oldest() -> None:
    url = "https://bing.com"
    oldest_archive = (
        "https://web.archive.org/web/20030726111100/http://www.bing.com:80/"
    )
    wayback = Url(url).oldest()
    assert wayback.archive_url == oldest_archive
    assert str(wayback) == oldest_archive
    assert len(wayback) > 365 * 15  # days in a year times years


def test_newest() -> None:
    url = "https://www.youtube.com/"
    wayback = Url(url).newest()
    assert "youtube" in str(wayback.archive_url)
    assert "archived_snapshots" in str(wayback.json)


def test_near() -> None:
    url = "https://www.google.com"
    wayback = Url(url).near(year=2010, month=10, day=10, hour=10, minute=10)
    assert "20101010" in str(wayback.archive_url)


def test_total_archives() -> None:
    wayback = Url("https://akamhy.github.io")
    assert wayback.total_archives() > 10

    wayback = Url("https://gaha.ef4i3n.m5iai3kifp6ied.cima/gahh2718gs/ahkst63t7gad8")
    assert wayback.total_archives() == 0


def test_known_urls() -> None:
    wayback = Url("akamhy.github.io")
    assert len(list(wayback.known_urls(subdomain=True))) > 40


def test_Save() -> None:
    wayback = Url("https://en.wikipedia.org/wiki/Asymptotic_equipartition_property")
    wayback.save()
    archive_url = str(wayback.archive_url)
    assert archive_url.find("Asymptotic_equipartition_property") != -1
