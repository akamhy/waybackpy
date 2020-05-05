# -*- coding: utf-8 -*-

class TooManyArchivingRequests(Exception):
    """Error when a single url reqeusted for archiving too many times in a short timespam.
    Wayback machine doesn't supports archivng any url too many times in a short period of time.
    """

class ArchivingNotAllowed(Exception):
    """Files like robots.txt are set to deny robot archiving.
    Wayback machine respects these file, will not archive.
    """

class PageNotSaved(Exception):
    """
    When unable to save a webpage.
    """

class ArchiveNotFound(Exception):
    """
    When a page was never archived but client asks for old archive.
    """

class UrlNotFound(Exception):
    """
    Raised when 404 UrlNotFound.
    """

class BadGateWay(Exception):
    """
    Raised when 502 bad gateway.
    """

class InvalidUrl(Exception):
    """
    Raised when url doesn't follow the standard url format.
    """
