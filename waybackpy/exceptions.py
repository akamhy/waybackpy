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


class URLError(Exception):
    """
    Raised when malformed URLs are passed as arguments.
    """
