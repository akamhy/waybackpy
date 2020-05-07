# -*- coding: utf-8 -*-
import json
from datetime import datetime
from waybackpy.exceptions import TooManyArchivingRequests, ArchivingNotAllowed, PageNotSaved, ArchiveNotFound, UrlNotFound, BadGateWay, InvalidUrl, WaybackUnavailable
try:
    from urllib.request import Request, urlopen
    from urllib.error import HTTPError, URLError
except ImportError:
    from urllib2 import Request, urlopen, HTTPError, URLError


default_UA = "waybackpy python package"

def url_check(url):
    if "." not in url:
        raise InvalidUrl("'%s' is not a vaild url." % url)

def clean_url(url):
    return str(url).strip().replace(" ","_")

def wayback_timestamp(**kwargs):
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

def handle_HTTPError(e):
    if e.code == 502:
        raise BadGateWay(e)
    elif e.code == 503:
        raise WaybackUnavailable(e)
    elif e.code == 429:
        raise TooManyArchivingRequests(e)
    elif e.code == 404:
        raise UrlNotFound(e)

def save(url, UA=default_UA):
    url_check(url)
    request_url = ("https://web.archive.org/save/" + clean_url(url))

    hdr = { 'User-Agent' : '%s' % UA } #nosec
    req = Request(request_url, headers=hdr) #nosec


    try:
        response = urlopen(req) #nosec
    except HTTPError as e:
        if handle_HTTPError(e) is None:
            raise PageNotSaved(e)
    except URLError:
        try:
            response = urlopen(req) #nosec
        except URLError as e:
            raise UrlNotFound(e)

    header = response.headers

    if "exclusion.robots.policy" in str(header):
        raise ArchivingNotAllowed("Can not archive %s. Disabled by site owner." % (url))

    return "https://web.archive.org" + header['Content-Location']

def get(url, encoding=None, UA=default_UA):
    url_check(url)
    hdr = { 'User-Agent' : '%s' % UA }
    req = Request(clean_url(url), headers=hdr) #nosec

    try:
        resp=urlopen(req) #nosec
    except URLError:
        try:
            resp=urlopen(req) #nosec
        except URLError as e:
            raise UrlNotFound(e)

    if encoding is None:
        try:
            encoding= resp.headers['content-type'].split('charset=')[-1]
        except AttributeError:
            encoding = "UTF-8"

    return resp.read().decode(encoding.replace("text/html", "UTF-8", 1))

def near(url, **kwargs):

    try:
        url = kwargs["url"]
    except KeyError:
        url = url

    year=kwargs.get("year", datetime.utcnow().strftime('%Y'))
    month=kwargs.get("month", datetime.utcnow().strftime('%m'))
    day=kwargs.get("day", datetime.utcnow().strftime('%d'))
    hour=kwargs.get("hour", datetime.utcnow().strftime('%H'))
    minute=kwargs.get("minute", datetime.utcnow().strftime('%M'))
    UA=kwargs.get("UA", default_UA)

    url_check(url)
    timestamp = wayback_timestamp(year=year,month=month,day=day,hour=hour,minute=minute)
    request_url = "https://archive.org/wayback/available?url=%s&timestamp=%s" % (clean_url(url), str(timestamp))
    hdr = { 'User-Agent' : '%s' % UA }
    req = Request(request_url, headers=hdr) # nosec

    try:
        response = urlopen(req) #nosec
    except HTTPError as e:
        handle_HTTPError(e)

    data = json.loads(response.read().decode("UTF-8"))
    if not data["archived_snapshots"]:
        raise ArchiveNotFound("'%s' is not yet archived." % url)

    archive_url = (data["archived_snapshots"]["closest"]["url"])
    # wayback machine returns http sometimes, idk why? But they support https
    archive_url = archive_url.replace("http://web.archive.org/web/","https://web.archive.org/web/",1)
    return archive_url

def oldest(url, UA=default_UA, year=1994):
    return near(url, year=year, UA=UA)

def newest(url, UA=default_UA):
    return near(url, UA=UA)

def total_archives(url, UA=default_UA):
    url_check(url)

    hdr = { 'User-Agent' : '%s' % UA }
    request_url = "https://web.archive.org/cdx/search/cdx?url=%s&output=json" % clean_url(url)
    req = Request(request_url, headers=hdr) # nosec

    try:
        response = urlopen(req) #nosec
    except HTTPError as e:
        handle_HTTPError(e)

    return (len(json.loads(response.read())))
