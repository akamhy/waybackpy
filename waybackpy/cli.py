# -*- coding: utf-8 -*-
from __future__ import print_function
import argparse
from waybackpy.wrapper import Url
from waybackpy.__version__ import __version__

def _save(obj):
    print(obj.save())

def _oldest(obj):
    print(obj.oldest())

def _newest(obj):
    print(obj.newest())

def _total_archives(obj):
    print(obj.total_archives())

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
    print(obj.near(**_near_args))

def _get(obj, args):
    if args.get.lower() == "url":
        print(obj.get())

    elif args.get.lower() == "oldest":
        print(obj.get(obj.oldest()))

    elif args.get.lower() == "latest" or args.get.lower() == "newest":
        print(obj.get(obj.newest()))

    elif args.get.lower() == "save":
        print(obj.get(obj.save()))

    else:
        print("Please use get as \"--get 'source'\", 'source' can be one of the followings: \
        \n1) url - get the source code of the url specified using --url/-u.\
        \n2) oldest - get the source code of the oldest archive for the supplied url.\
        \n3) newest - get the source code of the newest archive for the supplied url.\
        \n4) save - Create a new archive and get the source code of this new archive for the supplied url.")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", help="URL on which Wayback machine operations would occur.")
    parser.add_argument("-ua", "--user_agent", help="User agent, default user_agent is \"waybackpy python package - https://github.com/akamhy/waybackpy\".")
    parser.add_argument("-s", "--save", action='store_true', help="Save the URL on the Wayback machine.")
    parser.add_argument("-o", "--oldest", action='store_true', help="Oldest archive for the specified URL.")
    parser.add_argument("-n", "--newest", action='store_true', help="Newest archive for the specified URL.")
    parser.add_argument("-t", "--total", action='store_true', help="Total number of archives for the specified URL.")
    parser.add_argument("-g", "--get", help="Prints the source code of the supplied url. Use '--get help' for extended usage.")

    parser.add_argument("-n", "--near", action='store_true', help="Latest/Newest archive for the specified URL.")
    parser.add_argument("-y", "--year", type=int, help="Year in integer. For use with --near.")
    parser.add_argument("-M", "--month", type=int, help="Month in integer. For use with --near.")
    parser.add_argument("-d", "--day", type=int, help="Day in integer. For use with --near.")
    parser.add_argument("-H", "--hour", type=int, help="Hour in integer. For use with --near.")
    parser.add_argument("-m", "--minute", type=int, help="Minute in integer. For use with --near.")
    parser.add_argument("-v", "--version", action='store_true', help="Prints the waybackpy version.")

    args = parser.parse_args()

    if not args.url:
        print("please specify an URL using \"--url https://mywebiste.com\". Use --help for help.")
        return

    # create the object with or without the user_agent
    if args.user_agent:
        obj = Url(args.url, args.user_agent)
    else:
        obj = Url(args.url)

    print(repr(obj))

    if args.save:
        _save(obj)
    elif args.oldest:
        _oldest(obj)
    elif args.newest:
        _newest(obj)
    elif args.total:
        _total_archives(obj)
    elif args.near:
        _near(obj, args)
    elif args.get:
        _get(obj, args)
    elif args.version:
        print(__version__)
    else:
        print("Usage: youtube-dl [OPTIONS] URL [URL...].\
        \nwaybackpy: error: You must provide at least one URL. See --help\
        \nLatest docs and version available at https://github.com/akamhy/waybackpy")


if __name__ == "__main__":
    main()
