# -*- coding: utf-8 -*-
from __future__ import print_function
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

def _get(obj, args):
    if args.get.lower() == "url":
        return (obj.get())

    elif args.get.lower() == "oldest":
        return (obj.get(obj.oldest()))

    elif args.get.lower() == "latest" or args.get.lower() == "newest":
        return (obj.get(obj.newest()))

    elif args.get.lower() == "save":
        return (obj.get(obj.save()))

    else:
        return ("Use get as \"--get 'source'\", 'source' can be one of the followings: \
        \n1) url - get the source code of the url specified using --url/-u.\
        \n2) oldest - get the source code of the oldest archive for the supplied url.\
        \n3) newest - get the source code of the newest archive for the supplied url.\
        \n4) save - Create a new archive and get the source code of this new archive for the supplied url.")

def args_handler(args):
    if args.version:
        return (__version__)

    if not args.url:
        return ("Specify an URL. See --help")


    if args.user_agent:
        obj = Url(args.url, args.user_agent)
    else:
        obj = Url(args.url)

    if args.save:
        return _save(obj)
    elif args.oldest:
        return _oldest(obj)
    elif args.newest:
        return _newest(obj)
    elif args.total:
        return _total_archives(obj)
    elif args.near:
        return _near(obj, args)
    elif args.get:
        return _get(obj, args)
    else:
        return ("Usage: waybackpy --url [URL] --user_agent [USER AGENT] [OPTIONS]. See --help")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", help="URL on which Wayback machine operations would occur.")
    parser.add_argument("-ua", "--user_agent", help="User agent, default user_agent is \"waybackpy python package - https://github.com/akamhy/waybackpy\".")
    parser.add_argument("-s", "--save", action='store_true', help="Save the URL on the Wayback machine.")
    parser.add_argument("-o", "--oldest", action='store_true', help="Oldest archive for the specified URL.")
    parser.add_argument("-n", "--newest", action='store_true', help="Newest archive for the specified URL.")
    parser.add_argument("-t", "--total", action='store_true', help="Total number of archives for the specified URL.")
    parser.add_argument("-g", "--get", help="Prints the source code of the supplied url. Use '--get help' for extended usage.")
    parser.add_argument("-v", "--version", action='store_true', help="Prints the waybackpy version.")

    parser.add_argument("-N", "--near", action='store_true', help="Latest/Newest archive for the specified URL.")
    parser.add_argument("-Y", "--year", type=int, help="Year in integer. For use with --near.")
    parser.add_argument("-M", "--month", type=int, help="Month in integer. For use with --near.")
    parser.add_argument("-D", "--day", type=int, help="Day in integer. For use with --near.")
    parser.add_argument("-H", "--hour", type=int, help="Hour in integer. For use with --near.")
    parser.add_argument("-MIN", "--minute", type=int, help="Minute in integer. For use with --near.")

    args = parser.parse_args()

    print(args_handler(args))



if __name__ == "__main__":
    main()
