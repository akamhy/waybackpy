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

    All other exceptions are inherited from this main exception.
    """


class NoCDXRecordFound(WaybackError):
    """
    No records returned by the CDX server for a query.
    Raised when the user invokes near(), newest() or oldest() methods
    and there are no archives.
    """


class BlockedSiteError(WaybackError):
    """
    Raised when the archives for website/URLs that was excluded from Wayback
    Machine are requested via the CDX server API.
    """


class TooManyRequestsError(WaybackError):
    """
    Raised when you make more than 15 requests per
    minute and the Wayback Machine returns 429.

    See https://github.com/akamhy/waybackpy/issues/131
    """


class MaximumRetriesExceeded(WaybackError):
    """
    MaximumRetriesExceeded
    """


class MaximumSaveRetriesExceeded(MaximumRetriesExceeded):
    """
    MaximumSaveRetriesExceeded
    """


class ArchiveNotInAvailabilityAPIResponse(WaybackError):
    """
    Could not parse the archive in the JSON response of the availability API.
    """


class InvalidJSONInAvailabilityAPIResponse(WaybackError):
    """
    availability api returned invalid JSON
    """
