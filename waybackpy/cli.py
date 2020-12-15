# -*- coding: utf-8 -*-
import sys
import os
import re
import argparse
import string
import random
from waybackpy.wrapper import Url
from waybackpy.__version__ import __version__


def _save(obj):
    return obj.save()


def _archive_url(obj):
    return obj.archive_url


def _json(obj):
    return obj.JSON


def _oldest(obj):
    return obj.oldest()


def _newest(obj):
    return obj.newest()


def _total_archives(obj):
    return obj.total_archives()


def _near(obj, args):
    _near_args = {}
    if args.year:
        _near_args["year"] = args.year
    if args.month:
        _near_args["month"] = args.month
    if args.day:
        _near_args["day"] = args.day
    if args.hour:
        _near_args["hour"] = args.hour
    if args.minute:
        _near_args["minute"] = args.minute
    return obj.near(**_near_args)


def _save_urls_on_file(input_list, live_url_count):
    m = re.search("https?://([A-Za-z_0-9.-]+).*", input_list[0])
    if m:
        domain = m.group(1)
    else:
        domain = "domain-unknown"

    uid = "".join(
        random.choice(string.ascii_lowercase + string.digits) for _ in range(6)
    )

    file_name = "%s-%d-urls-%s.txt" % (domain, live_url_count, uid)
    file_content = "\n".join(input_list)
    file_path = os.path.join(os.getcwd(), file_name)
    with open(file_path, "w+") as f:
        f.write(file_content)
    return "%s\n\n'%s' saved in current working directory" % (file_content, file_name)


def _known_urls(obj, args):
    """Abbreviations:
    sd = subdomain
    al = alive
    """
    sd = False
    al = False
    if args.subdomain:
        sd = True
    if args.alive:
        al = True
    url_list = obj.known_urls(alive=al, subdomain=sd)
    total_urls = len(url_list)

    if total_urls > 0:
        text = _save_urls_on_file(url_list, total_urls)
    else:
        text = "No known URLs found. Please try a diffrent domain!"

    return text


def _get(obj, args):
    if args.get.lower() == "url":
        output = obj.get()

    elif args.get.lower() == "archive_url":
        output = obj.get(obj.archive_url)

    elif args.get.lower() == "oldest":
        output = obj.get(obj.oldest())

    elif args.get.lower() == "latest" or args.get.lower() == "newest":
        output = obj.get(obj.newest())

    elif args.get.lower() == "save":
        output = obj.get(obj.save())

    else:
        output = "Use get as \"--get 'source'\", 'source' can be one of the followings: \
            \n1) url - get the source code of the url specified using --url/-u.\
            \n2) archive_url - get the source code of the newest archive for the supplied url, alias of newest.\
            \n3) oldest - get the source code of the oldest archive for the supplied url.\
            \n4) newest - get the source code of the newest archive for the supplied url.\
            \n5) save - Create a new archive and get the source code of this new archive for the supplied url."

    return output


def args_handler(args):
    if args.version:
        return "waybackpy version %s" % __version__

    if not args.url:
        return (
            "waybackpy %s \nSee 'waybackpy --help' for help using this tool."
            % __version__
        )

    obj = Url(args.url)
    if args.user_agent:
        obj = Url(args.url, args.user_agent)

    if args.save:
        output = _save(obj)
    elif args.archive_url:
        output = _archive_url(obj)
    elif args.json:
        output = _json(obj)
    elif args.oldest:
        output = _oldest(obj)
    elif args.newest:
        output = _newest(obj)
    elif args.known_urls:
        output = _known_urls(obj, args)
    elif args.total:
        output = _total_archives(obj)
    elif args.near:
        output = _near(obj, args)
    elif args.get:
        output = _get(obj, args)
    else:
        output = (
            "You only specified the URL. But you also need to specify the operation."
            "\nSee 'waybackpy --help' for help using this tool."
        )
    return output


def parse_args(argv):
    parser = argparse.ArgumentParser()

    requiredArgs = parser.add_argument_group("URL argument (required)")
    requiredArgs.add_argument(
        "--url", "-u", help="URL on which Wayback machine operations would occur"
    )

    userAgentArg = parser.add_argument_group("User Agent")
    help_text = 'User agent, default user_agent is "waybackpy python package - https://github.com/akamhy/waybackpy"'
    userAgentArg.add_argument("--user_agent", "-ua", help=help_text)

    saveArg = parser.add_argument_group("Create new archive/save URL")
    saveArg.add_argument(
        "--save", "-s", action="store_true", help="Save the URL on the Wayback machine"
    )

    auArg = parser.add_argument_group("Get the latest Archive")
    auArg.add_argument(
        "--archive_url",
        "-au",
        action="store_true",
        help="Get the latest archive URL, alias for --newest",
    )

    jsonArg = parser.add_argument_group("Get the JSON data")
    jsonArg.add_argument(
        "--json",
        "-j",
        action="store_true",
        help="JSON data of the availability API request",
    )

    oldestArg = parser.add_argument_group("Oldest archive")
    oldestArg.add_argument(
        "--oldest",
        "-o",
        action="store_true",
        help="Oldest archive for the specified URL",
    )

    newestArg = parser.add_argument_group("Newest archive")
    newestArg.add_argument(
        "--newest",
        "-n",
        action="store_true",
        help="Newest archive for the specified URL",
    )

    totalArg = parser.add_argument_group("Total number of archives")
    totalArg.add_argument(
        "--total",
        "-t",
        action="store_true",
        help="Total number of archives for the specified URL",
    )

    getArg = parser.add_argument_group("Get source code")
    getArg.add_argument(
        "--get",
        "-g",
        help="Prints the source code of the supplied url. Use '--get help' for extended usage",
    )

    knownUrlArg = parser.add_argument_group(
        "URLs known and archived to Waybcak Machine for the site."
    )
    knownUrlArg.add_argument(
        "--known_urls", "-ku", action="store_true", help="URLs known for the domain."
    )
    help_text = "Use with '--known_urls' to include known URLs for subdomains."
    knownUrlArg.add_argument("--subdomain", "-sub", action="store_true", help=help_text)
    help_text = "Only include live URLs. Will not inlclude dead links."
    knownUrlArg.add_argument("--alive", "-a", action="store_true", help=help_text)

    nearArg = parser.add_argument_group("Archive close to time specified")
    nearArg.add_argument(
        "--near", "-N", action="store_true", help="Archive near specified time"
    )

    nearArgs = parser.add_argument_group("Arguments that are used only with --near")
    nearArgs.add_argument("--year", "-Y", type=int, help="Year in integer")
    nearArgs.add_argument("--month", "-M", type=int, help="Month in integer")
    nearArgs.add_argument("--day", "-D", type=int, help="Day in integer.")
    nearArgs.add_argument("--hour", "-H", type=int, help="Hour in intege")
    nearArgs.add_argument("--minute", "-MIN", type=int, help="Minute in integer")

    parser.add_argument(
        "--version", "-v", action="store_true", help="Waybackpy version"
    )

    return parser.parse_args(argv[1:])


def main(argv=None):
    if argv is None:
        argv = sys.argv
    args = parse_args(argv)
    output = args_handler(args)
    print(output)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
