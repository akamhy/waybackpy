# -*- coding: utf-8 -*-
import argparse
from waybackpy.wrapper import Url

if sys.version_info < (3, 0): # If the python ver 2.xxx
    from __future__ import print_function

def command_line():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", help="URL on which Wayback machine operations would occur.")
    parser.add_argument("-ua", "--user_agent", help="User agent, default user_agent is \"waybackpy python package - https://github.com/akamhy/waybackpy\".")
    parser.add_argument("-s", "--save", action='store_true', help="Save the URL on the Wayback machine.")
    parser.add_argument("-o", "--oldest", action='store_true', help="Oldest archive for the specified URL.")
    parser.add_argument("-l", "--latest", action='store_true', help="Latest/Newest archive for the specified URL.")
    parser.add_argument("-t", "--total", action='store_true', help="Total number of archives for the specified URL.")
    parser.add_argument("-g", "--get", help="Get the source code of the supplied url. Use '--get help' for extended usage.")

    parser.add_argument("-n", "--near", action='store_true', help="Latest/Newest archive for the specified URL.")
    parser.add_argument("-y", "--year", type=int, help="Year in integer. For use with --near.")
    parser.add_argument("-M", "--month", type=int, help="Month in integer. For use with --near.")
    parser.add_argument("-d", "--day", type=int, help="Day in integer. For use with --near.")
    parser.add_argument("-H", "--hour", type=int, help="Hour in integer. For use with --near.")
    parser.add_argument("-m", "--minute", type=int, help="Minute in integer. For use with --near.")

    args = parser.parse_args()

    if not args.url:
        print("please specify an URL using \"--url https://mywebiste.com\". Use --help for help.")
        return
    else:
        # create the object with or without the user_agent
        if args.user_agent:
            obj = Url(args.url, args.user_agent)
        else:
            obj = Url(args.url)

        if args.save:
            print(obj.save())

        elif args.oldest:
            print(obj.oldest())

        elif args.latest:
            print(obj.newest())

        elif args.total:
            print(obj.total_archives())

        elif args.near:
            _near_args = {}
            if args.year:
                _near_args["year"] = args.year
            if args.year:
                _near_args["month"] = args.month
            if args.year:
                _near_args["day"] = args.day
            if args.year:
                _near_args["hour"] = args.hour
            if args.year:
                _near_args["minute"] = args.minute
            n_args = {x: y for x, y in _near_args.items() if y is not None}
            print(obj.near(**n_args))

        elif args.get:
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
                \n3) latest - get the source code of the latest archive for the supplied url.\
                \n4) save - Create a new archive and get the source code of this new archive for the supplied url.")
        else:
            print("Please specify any operation as an argument. Use 'waybackpy --help' for help using wayback.\
            \nLatest docs and version available at https://github.com/akamhy/waybackpy ")


if __name__ == "__main__":
    command_line()

