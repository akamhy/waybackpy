import click
import re
import os
import json as JSON
import random
import requests
import string
from .__version__ import __version__
from .utils import DEFAULT_USER_AGENT
from .cdx_api import WaybackMachineCDXServerAPI
from .save_api import WaybackMachineSaveAPI
from .availability_api import WaybackMachineAvailabilityAPI
from .wrapper import Url


@click.command()
@click.option(
    "-u", "--url", help="URL on which Wayback machine operations are to be performed."
)
@click.option(
    "-ua",
    "--user-agent",
    "--user_agent",
    default=DEFAULT_USER_AGENT,
    help="User agent, default value is '%s'." % DEFAULT_USER_AGENT,
)
@click.option("-v", "--version", is_flag=True, default=False, help="waybackpy version.")
@click.option(
    "-l", "--license", is_flag=True, default=False, help="license of Waybackpy."
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
def main(
    url,
    user_agent,
    version,
    license,
    newest,
    oldest,
    json,
    near,
    year,
    month,
    day,
    hour,
    minute,
    save,
    headers,
    known_urls,
    subdomain,
    file,
    cdx,
    start_timestamp,
    end_timestamp,
    filter,
    match_type,
    gzip,
    collapse,
    limit,
    cdx_print,
):
    """\b
                         _                _
                        | |              | |
    __      ____ _ _   _| |__   __ _  ___| | ___ __  _   _
    \ \ /\ / / _` | | | | '_ \ / _` |/ __| |/ / '_ \| | | |
     \ V  V / (_| | |_| | |_) | (_| | (__|   <| |_) | |_| |
      \_/\_/ \__,_|\__, |_.__/ \__,_|\___|_|\_\ .__/ \__, |
                    __/ |                     | |     __/ |
                   |___/                      |_|    |___/

    Python package & CLI tool that interfaces the Wayback Machine APIs

    Repository: https://github.com/akamhy/waybackpy

    Documentation: https://github.com/akamhy/waybackpy/wiki/CLI-docs

    waybackpy - CLI usage(Demo video): https://asciinema.org/a/464367

    Released under the MIT License. Use the flag --license for license.

    """

    if version:
        click.echo("waybackpy version %s" % __version__)
        return

    if license:
        click.echo(
            requests.get(
                url="https://raw.githubusercontent.com/akamhy/waybackpy/master/LICENSE"
            ).text
        )
        return

    if not url:
        click.echo("No URL detected. Please provide an URL.")
        return

    if (
        url
        and not version
        and not oldest
        and not newest
        and not near
        and not save
        and not known_urls
        and not cdx
    ):
        click.echo(
            "Only URL passed, but did not specify what to do with the URL. Use --help flag for help using waybackpy."
        )
        return

    def echo_availability_api(availability_api_instance):
        click.echo("Archive URL:")
        if not availability_api_instance.archive_url:
            archive_url = (
                "NO ARCHIVE FOUND - The requested URL is probably "
                + "not yet archived or if the URL was recently archived then it is "
                + "not yet available via the Wayback Machine's availability API "
                + "because of database lag and should be available after some time."
            )
        else:
            archive_url = availability_api_instance.archive_url
        click.echo(archive_url)
        if json:
            click.echo("JSON response:")
            click.echo(JSON.dumps(availability_api_instance.JSON))

    availability_api = WaybackMachineAvailabilityAPI(url, user_agent=user_agent)

    if oldest:
        availability_api.oldest()
        echo_availability_api(availability_api)
        return

    if newest:
        availability_api.newest()
        echo_availability_api(availability_api)
        return

    if near:
        near_args = {}
        keys = ["year", "month", "day", "hour", "minute"]
        args_arr = [year, month, day, hour, minute]
        for key, arg in zip(keys, args_arr):
            if arg:
                near_args[key] = arg
        availability_api.near(**near_args)
        echo_availability_api(availability_api)
        return

    if save:
        save_api = WaybackMachineSaveAPI(url, user_agent=user_agent)
        save_api.save()
        click.echo("Archive URL:")
        click.echo(save_api.archive_url)
        click.echo("Cached save:")
        click.echo(save_api.cached_save)
        if headers:
            click.echo("Save API headers:")
            click.echo(save_api.headers)
        return

    def save_urls_on_file(url_gen):
        domain = None
        sys_random = random.SystemRandom()
        uid = "".join(
            sys_random.choice(string.ascii_lowercase + string.digits) for _ in range(6)
        )
        url_count = 0

        for url in url_gen:
            url_count += 1
            if not domain:
                match = re.search("https?://([A-Za-z_0-9.-]+).*", url)

                domain = "domain-unknown"

                if match:
                    domain = match.group(1)

                file_name = "{domain}-urls-{uid}.txt".format(domain=domain, uid=uid)
                file_path = os.path.join(os.getcwd(), file_name)
                if not os.path.isfile(file_path):
                    open(file_path, "w+").close()

            with open(file_path, "a") as f:
                f.write("{url}\n".format(url=url))

            click.echo(url)

        if url_count > 0:
            click.echo(
                "\n\n'{file_name}' saved in current working directory".format(
                    file_name=file_name
                )
            )
        else:
            click.echo("No known URLs found. Please try a diffrent input!")

    if known_urls:
        wayback = Url(url, user_agent)
        url_gen = wayback.known_urls(subdomain=subdomain)

        if file:
            return save_urls_on_file(url_gen)
        else:
            for url in url_gen:
                click.echo(url)

    if cdx:
        filters = list(filter)
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
                output_string = ""
                if any(val in cdx_print for val in ["urlkey", "url-key", "url_key"]):
                    output_string = output_string + snapshot.urlkey + " "
                if any(
                    val in cdx_print
                    for val in ["timestamp", "time-stamp", "time_stamp"]
                ):
                    output_string = output_string + snapshot.timestamp + " "
                if "original" in cdx_print:
                    output_string = output_string + snapshot.original + " "
                if "original" in cdx_print:
                    output_string = output_string + snapshot.original + " "
                if any(
                    val in cdx_print for val in ["mimetype", "mime-type", "mime_type"]
                ):
                    output_string = output_string + snapshot.mimetype + " "
                if any(
                    val in cdx_print
                    for val in ["statuscode", "status-code", "status_code"]
                ):
                    output_string = output_string + snapshot.statuscode + " "
                if "digest" in cdx_print:
                    output_string = output_string + snapshot.digest + " "
                if "length" in cdx_print:
                    output_string = output_string + snapshot.length + " "
                if any(
                    val in cdx_print
                    for val in ["archiveurl", "archive-url", "archive_url"]
                ):
                    output_string = output_string + snapshot.archive_url + " "
                click.echo(output_string)


if __name__ == "__main__":
    main()
