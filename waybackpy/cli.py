# -*- coding: utf-8 -*-
import sys
import os
import re
import argparse
import string
import random
from waybackpy.wrapper import Url
from waybackpy.__version__ import __version__
from waybackpy.exceptions import WaybackError


def _save(obj):
    try:
        return obj.save()
    except Exception as err:
        e = str(err)
        m = re.search(r"Header:\n(.*)", e)
        if m:
            header = m.group(1)
        if "No archive URL found in the API response" in e:
            return (
                "\n[waybackpy] Can not save/archive your link.\n[waybackpy] This\
                 could happen because either your waybackpy (%s) is likely out of\
                 date or Wayback Machine is malfunctioning.\n[waybackpy] Visit\
                 https://github.com/akamhy/waybackpy for the latest version of \
                waybackpy.\n[waybackpy] API response Header :\n%s"
                % (__version__, header)
            )
        return WaybackError(err)


def _archive_url(obj):
    return obj.archive_url


def _json(obj):
    return obj.JSON


def handle_not_archived_error(e, obj):
    m = re.search(r"archive\sfor\s\'(.*?)\'\stry", str(e))
    if m:
        url = m.group(1)
        ua = obj.user_agent
        if "github.com/akamhy/waybackpy" in ua:
            ua = "YOUR_USER_AGENT_HERE"
        return (
            "\n[Waybackpy] Can not find archive for '%s'.\n[Waybackpy] You can"
            " save the URL using the following command:\n[Waybackpy] waybackpy --"
            'user_agent "%s" --url "%s" --save' % (url, ua, url)
        )
    return WaybackError(e)


def _oldest(obj):
    try:
        return obj.oldest()
    except Exception as e:
        return handle_not_archived_error(e, obj)


def _newest(obj):
    try:
        return obj.newest()
    except Exception as e:
        return handle_not_archived_error(e, obj)


def _total_archives(obj):
    return obj.total_archives()


def _near(obj, args):
    _near_args = {}
    args_arr = [args.year, args.month, args.day, args.hour, args.minute]
    keys = ["year", "month", "day", "hour", "minute"]

    for key, arg in zip(keys, args_arr):
        if arg:
            _near_args[key] = arg

    try:
        return obj.near(**_near_args)
    except Exception as e:
        return handle_not_archived_error(e, obj)


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
        return obj.get()

    if args.get.lower() == "archive_url":
        return obj.get(obj.archive_url)

    if args.get.lower() == "oldest":
        return obj.get(obj.oldest())

    if args.get.lower() == "latest" or args.get.lower() == "newest":
        return obj.get(obj.newest())

    if args.get.lower() == "save":
        return obj.get(obj.save())


    return "Use get as \"--get 'source'\", 'source' can be one of the followings: \
        \n1) url - get the source code of the url specified using --url/-u.\
        \n2) archive_url - get the source code of the newest archive for the supplied url, alias of newest.\
        \n3) oldest - get the source code of the oldest archive for the supplied url.\
        \n4) newest - get the source code of the newest archive for the supplied url.\
        \n5) save - Create a new archive and get the source code of this new archive for the supplied url."


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
        return _save(obj)
    if args.archive_url:
        return _archive_url(obj)
    if args.json:
        return _json(obj)
    if args.oldest:
        return _oldest(obj)
    if args.newest:
        return _newest(obj)
    if args.known_urls:
        return _known_urls(obj, args)
    if args.total:
        return _total_archives(obj)
    if args.near:
        return _near(obj, args)
    if args.get:
        return _get(obj, args)

    return (
            "You only specified the URL. But you also need to specify the operation."
            "\nSee 'waybackpy --help' for help using this tool."
        )


def add_userAgentArg(userAgentArg):
    help_text = 'User agent, default user_agent is "waybackpy python package - https://github.com/akamhy/waybackpy"'
    userAgentArg.add_argument("--user_agent", "-ua", help=help_text)

def add_saveArg(saveArg):
    saveArg.add_argument(
        "--save", "-s", action="store_true", help="Save the URL on the Wayback machine"
    )

def add_auArg(auArg):
    auArg.add_argument(
        "--archive_url",
        "-au",
        action="store_true",
        help="Get the latest archive URL, alias for --newest",
    )

def add_jsonArg(jsonArg):
    jsonArg.add_argument(
        "--json",
        "-j",
        action="store_true",
        help="JSON data of the availability API request",
    )

def add_oldestArg(oldestArg):
    oldestArg.add_argument(
        "--oldest",
        "-o",
        action="store_true",
        help="Oldest archive for the specified URL",
    )

def add_newestArg(newestArg):
    newestArg.add_argument(
        "--newest",
        "-n",
        action="store_true",
        help="Newest archive for the specified URL",
    )

def add_totalArg(totalArg):
    totalArg.add_argument(
        "--total",
        "-t",
        action="store_true",
        help="Total number of archives for the specified URL",
    )

def add_getArg(getArg):
    getArg.add_argument(
        "--get",
        "-g",
        help="Prints the source code of the supplied url. Use '--get help' for extended usage",
    )

def add_knownUrlArg(knownUrlArg):
    knownUrlArg.add_argument(
        "--known_urls", "-ku", action="store_true", help="URLs known for the domain."
    )
    help_text = "Use with '--known_urls' to include known URLs for subdomains."
    knownUrlArg.add_argument("--subdomain", "-sub", action="store_true", help=help_text)
    help_text = "Only include live URLs. Will not inlclude dead links."
    knownUrlArg.add_argument("--alive", "-a", action="store_true", help=help_text)


def add_nearArgs(nearArgs):
    nearArgs.add_argument("--year", "-Y", type=int, help="Year in integer")
    nearArgs.add_argument("--month", "-M", type=int, help="Month in integer")
    nearArgs.add_argument("--day", "-D", type=int, help="Day in integer.")
    nearArgs.add_argument("--hour", "-H", type=int, help="Hour in intege")
    nearArgs.add_argument("--minute", "-MIN", type=int, help="Minute in integer")

def parse_args(argv):
    parser = argparse.ArgumentParser()

    requiredArgs = parser.add_argument_group("URL argument (required)")
    requiredArgs.add_argument(
        "--url", "-u", help="URL on which Wayback machine operations would occur"
    )

    userAgentArg = parser.add_argument_group("User Agent")
    add_userAgentArg(userAgentArg)

    saveArg = parser.add_argument_group("Create new archive/save URL")
    add_saveArg(saveArg)

    auArg = parser.add_argument_group("Get the latest Archive")
    add_auArg(auArg)

    jsonArg = parser.add_argument_group("Get the JSON data")
    add_jsonArg(jsonArg)

    oldestArg = parser.add_argument_group("Oldest archive")
    add_oldestArg(oldestArg)

    newestArg = parser.add_argument_group("Newest archive")
    add_newestArg(newestArg)

    totalArg = parser.add_argument_group("Total number of archives")
    add_totalArg(totalArg)

    getArg = parser.add_argument_group("Get source code")
    add_getArg(getArg)

    knownUrlArg = parser.add_argument_group(
        "URLs known and archived to Waybcak Machine for the site."
    )
    add_knownUrlArg(knownUrlArg)

    nearArg = parser.add_argument_group("Archive close to time specified")
    nearArg.add_argument(
        "--near", "-N", action="store_true", help="Archive near specified time"
    )
    #The following is adding supplementary args used with near.
    nearArgs = parser.add_argument_group("Arguments that are used only with --near")
    add_nearArgs(nearArgs)

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
