# -*- coding: utf-8 -*-


class WaybackError(Exception):
    """
    Raised when Wayback Machine API Service is unreachable/down.
    """


class URLError(Exception):
    """
    Raised when malformed URLs are passed as arguments.
    """
