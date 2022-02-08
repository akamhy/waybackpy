"""
Module that makes waybackpy a CLI tool.
"""

import os
import random
import re
import string
from json import dumps
from typing import Generator, List, Optional

import click
import requests

from . import __version__
from .availability_api import WaybackMachineAvailabilityAPI
from .cdx_api import WaybackMachineCDXServerAPI
from .save_api import WaybackMachineSaveAPI
from .utils import DEFAULT_USER_AGENT
from .wrapper import Url


def echo_availability_api(
    availability_api_instance: WaybackMachineAvailabilityAPI, json: bool
) -> None:
    """
    Output availability API depending functions.
    Near, oldest and newest output by this method.
    """
    if not availability_api_instance.archive_url:
        archive_url = (
            "NO ARCHIVE FOUND - The requested URL is probably "
            + "not yet archived or if the URL was recently archived then it is "
            + "not yet available via the Wayback Machine's availability API "
            + "because of database lag and should be available after some time."
        )
    else:
        archive_url = availability_api_instance.archive_url
    click.echo("Archive URL:")
    click.echo(archive_url)
    if json:
        click.echo("JSON response:")
        click.echo(dumps(availability_api_instance.json))


def save_urls_on_file(url_gen: Generator[str, None, None]) -> None:
    """
    Save output of CDX API on file.
    Mainly here because of backwards compatibility.
    """
    domain = None
    sys_random = random.SystemRandom()
    uid = "".join(
        sys_random.choice(string.ascii_lowercase + string.digits) for _ in range(6)
    )
    url_count = 0
    file_name = None

    for url in url_gen:
        url_count += 1
        if not domain:
            match = re.search("https?://([A-Za-z_0-9.-]+).*", url)

            domain = "domain-unknown"

            if match:
                domain = match.group(1)

            file_name = f"{domain}-urls-{uid}.txt"
            file_path = os.path.join(os.getcwd(), file_name)
            if not os.path.isfile(file_path):
                open(file_path, "w+", encoding="utf-8").close()

        with open(file_path, "a", encoding="utf-8") as file:
            file.write(f"{url}\n")

        click.echo(url)

    if url_count > 0:
        click.echo(
            f"\n\n{url_count} URLs saved inside '{file_name}' in the current "
            + "working directory."
        )
    else:
        click.echo("No known URLs found. Please try a diffrent input!")


@click.command()
@click.option(
    "-u", "--url", help="URL on which Wayback machine operations are to be performed."
)
@click.option(
    "-ua",
    "--user-agent",
    "--user_agent",
    default=DEFAULT_USER_AGENT,
    help=f"User agent, default value is '{DEFAULT_USER_AGENT}'.",
)
@click.option("-v", "--version", is_flag=True, default=False, help="waybackpy version.")
@click.option(
    "-l",
    "--show-license",
    "--show_license",
    "--license",
    is_flag=True,
    default=False,
    help="Show license of Waybackpy.",
)
@click.option(
    "-n",
    "--newest",
    "-au",
    "--archive_url",
    "--archive-url",
    default=False,
    is_flag=True,
    help="Retrieve the newest archive of URL.",
)
@click.option(
    "-o",
    "--oldest",
    default=False,
    is_flag=True,
    help="Retrieve the oldest archive of URL.",
)
@click.option(
    "-j",
    "--json",
    default=False,
    is_flag=True,
    help="JSON data returned by the availability API.",
)
@click.option(
    "-N",
    "--near",
    default=False,
    is_flag=True,
    help="Archive close to a specified time.",
)
@click.option("-Y", "--year", type=click.IntRange(1994, 9999), help="Year in integer.")
@click.option("-M", "--month", type=click.IntRange(1, 12), help="Month in integer.")
@click.option("-D", "--day", type=click.IntRange(1, 31), help="Day in integer.")
@click.option("-H", "--hour", type=click.IntRange(0, 24), help="Hour in integer.")
@click.option("-MIN", "--minute", type=click.IntRange(0, 60), help="Minute in integer.")
@click.option(
    "-s",
    "--save",
    default=False,
    is_flag=True,
    help="Save the specified URL's webpage and print the archive URL.",
)
@click.option(
    "-h",
    "--headers",
    default=False,
    is_flag=True,
    help="Headers data of the SavePageNow API.",
)
@click.option(
    "-ku",
    "--known-urls",
    "--known_urls",
    default=False,
    is_flag=True,
    help="List known URLs. Uses CDX API.",
)
@click.option(
    "-sub",
    "--subdomain",
    default=False,
    is_flag=True,
    help="Use with '--known_urls' to include known URLs for subdomains.",
)
@click.option(
    "-f",
    "--file",
    default=False,
    is_flag=True,
    help="Use with '--known_urls' to save the URLs in file at current directory.",
)
@click.option(
    "-c",
    "--cdx",
    default=False,
    is_flag=True,
    help="Flag for using CDX API.",
)
@click.option(
    "-st",
    "--start-timestamp",
    "--start_timestamp",
    help="Start timestamp for CDX API in yyyyMMddhhmmss format.",
)
@click.option(
    "-et",
    "--end-timestamp",
    "--end_timestamp",
    help="End timestamp for CDX API in yyyyMMddhhmmss format.",
)
@click.option(
    "-f",
    "--cdx-filter",
    "--cdx_filter",
    "--filter",
    multiple=True,
    help="Filter on a specific field or all the CDX fields.",
)
@click.option(
    "-mt",
    "--match-type",
    "--match_type",
    help="The default behavior is to return matches for an exact URL. "
    + "However, the CDX server can also return results matching a certain prefix, "
    + "a certain host, or all sub-hosts by using the match_type",
)
@click.option(
    "-gz",
    "--gzip",
    help="To disable gzip compression pass false as argument to this parameter. "
    + "The default behavior is gzip compression enabled.",
)
@click.option(
    "-c",
    "--collapse",
    multiple=True,
    help="Filtering or 'collapse' results based on a field, or a substring of a field.",
)
@click.option(
    "-l",
    "--limit",
    help="Number of maximum record that CDX API is asked to return per API call, "
    + "default value is 500 records.",
)
@click.option(
    "-cp",
    "--cdx-print",
    "--cdx_print",
    multiple=True,
    help="Print only certain fields of the CDX API response, "
    + "if this parameter is not used then the plain text response of the CDX API "
    + "will be printed.",
)
def main(  # pylint: disable=no-value-for-parameter
    user_agent: str,
    version: bool,
    show_license: bool,
    newest: bool,
    oldest: bool,
    json: bool,
    near: bool,
    save: bool,
    headers: bool,
    known_urls: bool,
    subdomain: bool,
    file: bool,
    cdx: bool,
    cdx_filter: List[str],
    collapse: List[str],
    cdx_print: List[str],
    url: Optional[str] = None,
    year: Optional[int] = None,
    month: Optional[int] = None,
    day: Optional[int] = None,
    hour: Optional[int] = None,
    minute: Optional[int] = None,
    start_timestamp: Optional[str] = None,
    end_timestamp: Optional[str] = None,
    match_type: Optional[str] = None,
    gzip: Optional[str] = None,
    limit: Optional[str] = None,
) -> None:
    """\b
                         _                _
                        | |              | |
    __      ____ _ _   _| |__   __ _  ___| | ___ __  _   _
    \\ \\ /\\ / / _` | | | | '_ \\ / _` |/ __| |/ / '_ \\| | | |
     \\ V  V / (_| | |_| | |_) | (_| | (__|   <| |_) | |_| |
      \\_/\\_/ \\__,_|\\__, |_.__/ \\__,_|\\___|_|\\_\\ .__/ \\__, |
                    __/ |                     | |     __/ |
                   |___/                      |_|    |___/

    Python package & CLI tool that interfaces the Wayback Machine APIs

    Repository: https://github.com/akamhy/waybackpy

    Documentation: https://github.com/akamhy/waybackpy/wiki/CLI-docs

    waybackpy - CLI usage(Demo video): https://asciinema.org/a/464367

    Released under the MIT License. Use the flag --license for license.

    """
    if version:
        click.echo(f"waybackpy version {__version__}")

    elif show_license:
        click.echo(
            requests.get(
                url="https://raw.githubusercontent.com/akamhy/waybackpy/master/LICENSE"
            ).text
        )
    elif url is None:
        click.echo("No URL detected. Please provide an URL.", err=True)

    elif oldest:
        availability_api = WaybackMachineAvailabilityAPI(url, user_agent=user_agent)
        availability_api.oldest()
        echo_availability_api(availability_api, json)

    elif newest:
        availability_api = WaybackMachineAvailabilityAPI(url, user_agent=user_agent)
        availability_api.newest()
        echo_availability_api(availability_api, json)

    elif near:
        availability_api = WaybackMachineAvailabilityAPI(url, user_agent=user_agent)
        near_args = {}
        keys = ["year", "month", "day", "hour", "minute"]
        args_arr = [year, month, day, hour, minute]
        for key, arg in zip(keys, args_arr):
            if arg:
                near_args[key] = arg
        availability_api.near(**near_args)
        echo_availability_api(availability_api, json)

    elif save:
        save_api = WaybackMachineSaveAPI(url, user_agent=user_agent)
        save_api.save()
        click.echo("Archive URL:")
        click.echo(save_api.archive_url)
        click.echo("Cached save:")
        click.echo(save_api.cached_save)
        if headers:
            click.echo("Save API headers:")
            click.echo(save_api.headers)

    elif known_urls:
        wayback = Url(url, user_agent)
        url_gen = wayback.known_urls(subdomain=subdomain)

        if file:
            save_urls_on_file(url_gen)
        else:
            for url_ in url_gen:
                click.echo(url_)

    elif cdx:
        filters = list(cdx_filter)
        collapses = list(collapse)
        cdx_print = list(cdx_print)

        cdx_api = WaybackMachineCDXServerAPI(
            url,
            user_agent=user_agent,
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp,
            filters=filters,
            match_type=match_type,
            gzip=gzip,
            collapses=collapses,
            limit=limit,
        )

        snapshots = cdx_api.snapshots()

        for snapshot in snapshots:
            if len(cdx_print) == 0:
                click.echo(snapshot)
            else:
                output_string = []
                if any(val in cdx_print for val in ["urlkey", "url-key", "url_key"]):
                    output_string.append(snapshot.urlkey)
                if any(
                    val in cdx_print
                    for val in ["timestamp", "time-stamp", "time_stamp"]
                ):
                    output_string.append(snapshot.timestamp)
                if "original" in cdx_print:
                    output_string.append(snapshot.original)
                if any(
                    val in cdx_print for val in ["mimetype", "mime-type", "mime_type"]
                ):
                    output_string.append(snapshot.mimetype)
                if any(
                    val in cdx_print
                    for val in ["statuscode", "status-code", "status_code"]
                ):
                    output_string.append(snapshot.statuscode)
                if "digest" in cdx_print:
                    output_string.append(snapshot.digest)
                if "length" in cdx_print:
                    output_string.append(snapshot.length)
                if any(
                    val in cdx_print
                    for val in ["archiveurl", "archive-url", "archive_url"]
                ):
                    output_string.append(snapshot.archive_url)

                click.echo(" ".join(output_string))

    else:
        click.echo(
            "Only URL passed, but did not specify what to do with the URL. "
            "Use --help flag for help using waybackpy.",
            err=True,
        )


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
