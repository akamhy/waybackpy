# -*- coding: utf-8 -*-
from datetime import datetime
from urllib.request import Request, urlopen
import urllib.error

# YYYYMMDDhhmmss

class TooManyArchivingRequestsError(Exception):
    """
    An error when a single url is archived multiple times in a short timespam..
    """
    pass

class ArchivingNotAllowed(Exception):
    pass

def save(url,UA="pywayback python module"):
    base_save_url = "https://web.archive.org/save/"
    request_url = base_save_url + url
    hdr = { 'User-Agent' : '%s' % UA }
    req = Request(request_url, headers=hdr)
    try:
        response = urlopen(req)
    except urllib.error.HTTPError as e:
        raise TooManyArchivingRequestsError(e)
    # print(response.read())
    header = response.headers
    if "exclusion.robots.policy" in str(header):
        raise ArchivingNotAllowed("Can not archive %s. Disabled by site owner." % (url))
    archive_id = header['Content-Location']
    print(header)
    archived_url = "https://web.archive.org" + archive_id
    return archived_url

def near(
    url,
    year=datetime.utcnow().strftime('%Y'),
    month=datetime.utcnow().strftime('%m'),
    day=datetime.utcnow().strftime('%d'),
    hour=datetime.utcnow().strftime('%H'),
    minute=datetime.utcnow().strftime('%M'),
    ):
    timestamp = str(year)+str(month)+str(day)+str(hour)+str(minute)
    Rurl = "https://archive.org/wayback/available?url=%s&timestamp=%s" % (str(url), str(timestamp))
    response = urlopen(Rurl) #nosec
    encoding = response.info().get_content_charset('utf8')
    import json
    data = json.loads(response.read().decode(encoding))
    archive_url = (data["archived_snapshots"]["closest"]["url"])
    return archive_url

def oldest(url):
    return near(url,1995)

def newest(url):
    return near(url)
