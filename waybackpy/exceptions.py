"""
waybackpy.exceptions
~~~~~~~~~~~~~~~~~~~
This module contains the set of Waybackpy's exceptions.
"""


class WaybackError(Exception):
    """
    Raised when Waybackpy can not return what you asked for.
     1) Wayback Machine API Service is unreachable/down.
     2) You passed illegal arguments.
    """


class RedirectSaveError(WaybackError):
    """
    Raised when the original URL is redirected and the
    redirect URL is archived but not the original URL.
    """


class URLError(Exception):
    """
    Raised when malformed URLs are passed as arguments.
    """


class MaximumRetriesExceeded(WaybackError):
    """
    MaximumRetriesExceeded
    """


class MaximumSaveRetriesExceeded(MaximumRetriesExceeded):
    """
    MaximumSaveRetriesExceeded
    """
