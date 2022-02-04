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

     All other exceptions are inherited from this class.
    """

    pass


class RedirectSaveError(WaybackError):
    """
    Raised when the original URL is redirected and the
    redirect URL is archived but not the original URL.
    """

    pass


class URLError(Exception):
    """
    Raised when malformed URLs are passed as arguments.
    """

    pass


class MaximumRetriesExceeded(WaybackError):
    """
    MaximumRetriesExceeded
    """

    pass


class MaximumSaveRetriesExceeded(MaximumRetriesExceeded):
    """
    MaximumSaveRetriesExceeded
    """

    pass


class ArchiveNotInAvailabilityAPIResponse(WaybackError):
    """
    Could not parse the archive in the JSON response of the availability API.
    """

    pass


class InvalidJSONInAvailabilityAPIResponse(WaybackError):
    """
    availability api returned invalid JSON
    """

    pass
