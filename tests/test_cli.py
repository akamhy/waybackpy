import requests
from click.testing import CliRunner

from waybackpy import __version__
from waybackpy.cli import main


def test_oldest() -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["--url", " https://github.com ", "--oldest"])
    assert result.exit_code == 0
    assert (
        result.output
        == "Archive URL:\nhttps://web.archive.org/web/2008051421\
0148/http://github.com/\n"
    )


def test_near() -> None:
    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            "--url",
            " https://facebook.com ",
            "--near",
            "--year",
            "2010",
            "--month",
            "5",
            "--day",
            "10",
            "--hour",
            "6",
        ],
    )
    assert result.exit_code == 0
    assert (
        result.output
        == "Archive URL:\nhttps://web.archive.org/web/2010051008\
2647/http://www.facebook.com/\n"
    )


def test_newest() -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["--url", " https://microsoft.com ", "--newest"])
    assert result.exit_code == 0
    assert (
        result.output.find("microsoft.com") != -1
        and result.output.find("Archive URL:\n") != -1
    )


def test_cdx() -> None:
    runner = CliRunner()
    result = runner.invoke(
        main,
        "--url https://twitter.com/jack --cdx --user-agent some-user-agent \
--start-timestamp 2010 --end-timestamp 2012 --collapse urlkey \
--match-type prefix --cdx-print archiveurl --cdx-print length \
--cdx-print digest --cdx-print statuscode --cdx-print mimetype \
--cdx-print original --cdx-print timestamp --cdx-print urlkey".split(
            " "
        ),
    )
    assert result.exit_code == 0
    assert result.output.count("\n") > 3000


def test_save() -> None:
    runner = CliRunner()
    result = runner.invoke(
        main,
        "--url https://yahoo.com --user_agent my-unique-user-agent \
--save --headers".split(
            " "
        ),
    )
    assert result.exit_code == 0
    assert result.output.find("Archive URL:") != -1
    assert (result.output.find("Cached save:\nTrue") != -1) or (
        result.output.find("Cached save:\nFalse") != -1
    )
    assert result.output.find("Save API headers:\n") != -1
    assert result.output.find("yahoo.com") != -1


def test_version() -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["--version"])
    assert result.exit_code == 0
    assert result.output == f"waybackpy version {__version__}\n"


def test_license() -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["--license"])
    assert result.exit_code == 0
    assert (
        result.output
        == requests.get(
            url="https://raw.githubusercontent.com/akamhy/waybackpy/master/LICENSE"
        ).text
        + "\n"
    )


def test_only_url() -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["--url", "https://google.com"])
    assert result.exit_code == 0
    assert (
        result.output
        == "NoCommandFound: Only URL passed, but did not specify what to do with the URL. Use \
--help flag for help using waybackpy.\n"
    )


def test_known_url() -> None:
    # with file generator enabled
    runner = CliRunner()
    result = runner.invoke(
        main, ["--url", "https://akamhy.github.io", "--known-urls", "--file"]
    )
    assert result.exit_code == 0
    assert result.output.count("\n") > 40
    assert result.output.count("akamhy.github.io") > 40
    assert result.output.find("in the current working directory.\n") != -1

    # without file
    runner = CliRunner()
    result = runner.invoke(main, ["--url", "https://akamhy.github.io", "--known-urls"])
    assert result.exit_code == 0
    assert result.output.count("\n") > 40
    assert result.output.count("akamhy.github.io") > 40
