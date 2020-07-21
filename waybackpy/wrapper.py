# -*- coding: utf-8 -*-

import re
import sys
import json
from datetime import datetime
from waybackpy.exceptions import WaybackError

if sys.version_info >= (3, 0):  # If the python ver >= 3
    from urllib.request import Request, urlopen
    from urllib.error import URLError
else: # For python2.x
    from urllib2 import Request, urlopen, URLError

default_UA = "waybackpy python package - https://github.com/akamhy/waybackpy"

class Url():
    """waybackpy Url object"""


    def __init__(self, url, user_agent=default_UA):
        self.url = url
        self.user_agent = user_agent
        self.url_check() # checks url validity on init.

    def __repr__(self):
        """Representation of the object."""
        return "waybackpy.Url(url=%s, user_agent=%s)" % (self.url, self.user_agent)

    def __str__(self):
        """String representation of the object."""
        return "%s" % self.clean_url()

    def __len__(self):
        """Length of the URL."""
        return len(self.clean_url())

    def url_check(self):
        """Check for common URL problems."""
        if "." not in self.url:
            raise URLError("'%s' is not a vaild url." % self.url)
        return True

    def clean_url(self):
        """Fix the URL, if possible."""
        return str(self.url).strip().replace(" ","_")

    def wayback_timestamp(self, **kwargs):
        """Return the formatted the timestamp."""
        return (
          str(kwargs["year"])
          +
          str(kwargs["month"]).zfill(2)
          +
          str(kwargs["day"]).zfill(2)
          +
          str(kwargs["hour"]).zfill(2)
          +
          str(kwargs["minute"]).zfill(2)
          )

    def save(self):
        """Create a new archives for an URL on the Wayback Machine."""
        request_url = ("https://web.archive.org/save/" + self.clean_url())
        hdr = { 'User-Agent' : '%s' % self.user_agent } #nosec
        req = Request(request_url, headers=hdr) #nosec
        header = self.get_response(req).headers

        def archive_url_parser(header):
            """Parse out the archive from header."""
            #Regex1
            arch = re.search(r"rel=\"memento.*?(web\.archive\.org/web/[0-9]{14}/.*?)>", str(header))
            if arch:
                return arch.group(1)
            #Regex2
            arch = re.search(r"X-Cache-Key:\shttps(.*)[A-Z]{2}", str(header))
            if arch:
                return arch.group(1)
            raise WaybackError(
                "No archive url found in the API response. Visit https://github.com/akamhy/waybackpy for latest version of waybackpy.\nHeader:\n%s" % str(header)
            )

        return "https://" + archive_url_parser(header)

    def get(self, url=None, user_agent=None, encoding=None):
        """Returns the source code of the supplied URL. Auto detects the encoding if not supplied."""

        if not url:
            url = self.clean_url()
        if not user_agent:
            user_agent = self.user_agent

        hdr = { 'User-Agent' : '%s' % user_agent }
        req = Request(url, headers=hdr) #nosec
        response = self.get_response(req)
        if not encoding:
            try:
                encoding= response.headers['content-type'].split('charset=')[-1]
            except AttributeError:
                encoding = "UTF-8"
        return response.read().decode(encoding.replace("text/html", "UTF-8", 1))

    def get_response(self, req):
        """Get response for the supplied request."""
        try:
            response = urlopen(req) #nosec
        except Exception:
            try:
                 response = urlopen(req) #nosec
            except Exception as e:
                waybackraise = WaybackError(e)
                waybackraise.__cause__ = None #Suppress the urllib2/3 Exception
                raise waybackraise
        return response

    def near(self, **kwargs):
        """ Returns the archived from Wayback Machine for an URL closest to the time supplied.
            Supported params are year, month, day, hour and minute.
            The non supplied parameters are default to the runtime time.
        """
        year=kwargs.get("year", datetime.utcnow().strftime('%Y'))
        month=kwargs.get("month", datetime.utcnow().strftime('%m'))
        day=kwargs.get("day", datetime.utcnow().strftime('%d'))
        hour=kwargs.get("hour", datetime.utcnow().strftime('%H'))
        minute=kwargs.get("minute", datetime.utcnow().strftime('%M'))
        timestamp = self.wayback_timestamp(year=year,month=month,day=day,hour=hour,minute=minute)
        request_url = "https://archive.org/wayback/available?url=%s&timestamp=%s" % (self.clean_url(), str(timestamp))
        hdr = { 'User-Agent' : '%s' % self.user_agent }
        req = Request(request_url, headers=hdr) # nosec
        response = self.get_response(req)
        data = json.loads(response.read().decode("UTF-8"))
        if not data["archived_snapshots"]:
            raise WaybackError("'%s' is not yet archived. Use wayback.Url(url, user_agent).save() to create a new archive." % self.clean_url())
        archive_url = (data["archived_snapshots"]["closest"]["url"])
        # wayback machine returns http sometimes, idk why? But they support https
        archive_url = archive_url.replace("http://web.archive.org/web/","https://web.archive.org/web/",1)
        return archive_url

    def oldest(self, year=1994):
        """Returns the oldest archive from Wayback Machine for an URL."""
        return self.near(year=year)

    def newest(self):
        """Returns the newest archive on Wayback Machine for an URL, sometimes you may not get the newest archive because wayback machine DB lag."""
        return self.near()

    def total_archives(self):
        """Returns the total number of archives on Wayback Machine for an URL."""
        hdr = { 'User-Agent' : '%s' % self.user_agent }
        request_url = "https://web.archive.org/cdx/search/cdx?url=%s&output=json&fl=statuscode" % self.clean_url()
        req = Request(request_url, headers=hdr) # nosec
        response = self.get_response(req)
        return str(response.read()).count(",") # Most efficient method to count number of archives (yet)

def command_line():
    pass

if __name__ == "__main__":
    command_line()
