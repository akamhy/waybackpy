# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
import os
import re
import argparse
from waybackpy.wrapper import Url
from waybackpy.__version__ import __version__

def _save(obj):
    return (obj.save())

def _oldest(obj):
    return (obj.oldest())

def _newest(obj):
    return (obj.newest())

def _total_archives(obj):
    return (obj.total_archives())

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
    return (obj.near(**_near_args))

def _known_urls(obj, args):
    sd = False
    al = False
    if args.subdomain:
        sd = True
    if args.alive:
        al = True
    url_list = obj.known_urls(alive=al, subdomain=sd)
    total_urls = len(url_list)

    if total_urls > 0:
        m = re.search('https?://([A-Za-z_0-9.-]+).*', url_list[0])
        if m:
            domain = m.group(1)
        else:
            domain = "waybackpy-known"
        dir_path = os.path.abspath(os.getcwd())
        file_name = dir_path + "/%s-%d-urls.txt" % (domain, total_urls)
        text = "\n".join(url_list) + "\n"
        with open(file_name, "a+") as f:
            f.write(text)
        text =  text + "%d URLs found and saved in ./%s-%d-urls.txt" % (
            total_urls, domain, total_urls
            )

    else:
        text = "No known URLs found. Please try a diffrent domain!"

    return text

def _get(obj, args):
    if args.get.lower() == "url":
        return (obj.get())

    if args.get.lower() == "oldest":
        return (obj.get(obj.oldest()))

    if args.get.lower() == "latest" or args.get.lower() == "newest":
        return (obj.get(obj.newest()))

    if args.get.lower() == "save":
        return (obj.get(obj.save()))

    return ("Use get as \"--get 'source'\", 'source' can be one of the followings: \
        \n1) url - get the source code of the url specified using --url/-u.\
        \n2) oldest - get the source code of the oldest archive for the supplied url.\
        \n3) newest - get the source code of the newest archive for the supplied url.\
        \n4) save - Create a new archive and get the source code of this new archive for the supplied url.")

def args_handler(args):
    if args.version:
        return ("waybackpy version %s" % __version__)

    if not args.url:
        return ("waybackpy %s \nSee 'waybackpy --help' for help using this tool." % __version__)

    if args.user_agent:
        obj = Url(args.url, args.user_agent)
    else:
        obj = Url(args.url)

    if args.save:
        return _save(obj)
    if args.oldest:
        return _oldest(obj)
    if args.newest:
        return _newest(obj)
    if args.total:
        return _total_archives(obj)
    if args.near:
        return _near(obj, args)
    if args.known_urls:
        return _known_urls(obj, args)
    if args.get:
        return _get(obj, args)
    return ("You only specified the URL. But you also need to specify the operation.\nSee 'waybackpy --help' for help using this tool.")

def parse_args(argv):
    parser = argparse.ArgumentParser()

    requiredArgs = parser.add_argument_group('URL argument (required)')
    requiredArgs.add_argument("--url", "-u", help="URL on which Wayback machine operations would occur")

    userAgentArg = parser.add_argument_group('User Agent')
    userAgentArg.add_argument("--user_agent", "-ua", help="User agent, default user_agent is \"waybackpy python package - https://github.com/akamhy/waybackpy\"")
    
    saveArg = parser.add_argument_group("Create new archive/save URL")
    saveArg.add_argument("--save", "-s", action='store_true', help="Save the URL on the Wayback machine")
    
    oldestArg = parser.add_argument_group("Oldest archive")
    oldestArg.add_argument("--oldest", "-o", action='store_true', help="Oldest archive for the specified URL")
    
    newestArg = parser.add_argument_group("Newest archive")
    newestArg.add_argument("--newest", "-n", action='store_true', help="Newest archive for the specified URL")
    
    totalArg = parser.add_argument_group("Total number of archives")
    totalArg.add_argument("--total", "-t", action='store_true', help="Total number of archives for the specified URL")
    
    getArg = parser.add_argument_group("Get source code")
    getArg.add_argument("--get", "-g", help="Prints the source code of the supplied url. Use '--get help' for extended usage")

    knownUrlArg = parser.add_argument_group("URLs known and archived to Waybcak Machine for the site.")
    knownUrlArg.add_argument("--known_urls", "-ku", action='store_true', help="URLs known for the domain.")
    knownUrlArg.add_argument("--subdomain", "-sub", action='store_true', help="Use with '--known_urls' to include known URLs for subdomains.")
    knownUrlArg.add_argument("--alive", "-a", action='store_true', help="Only include live URLs. Will not inlclude dead links.")


    nearArg = parser.add_argument_group('Archive close to time specified')
    nearArg.add_argument("--near", "-N", action='store_true', help="Archive near specified time")

    nearArgs = parser.add_argument_group('Arguments that are used only with --near')
    nearArgs.add_argument("--year", "-Y", type=int, help="Year in integer")
    nearArgs.add_argument("--month", "-M", type=int, help="Month in integer")
    nearArgs.add_argument("--day", "-D", type=int, help="Day in integer.")
    nearArgs.add_argument("--hour", "-H", type=int, help="Hour in intege")
    nearArgs.add_argument("--minute", "-MIN", type=int, help="Minute in integer")

    parser.add_argument("--version", "-v", action='store_true', help="Waybackpy version")
    
    return parser.parse_args(argv[1:])

def main(argv=None):
    if argv is None:
        argv = sys.argv
    args = parse_args(argv)
    output = args_handler(args)
    print(output)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
