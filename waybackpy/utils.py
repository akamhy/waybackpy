"""
Utility functions and shared variables like DEFAULT_USER_AGENT are here.
"""

from datetime import datetime

from . import __version__

DEFAULT_USER_AGENT: str = (
    f"waybackpy {__version__} - https://github.com/akamhy/waybackpy"
)


def unix_timestamp_to_wayback_timestamp(unix_timestamp: int) -> str:
    """
    Converts Unix time to Wayback Machine timestamp, Wayback Machine
    timestamp format is yyyyMMddhhmmss.
    """
    return datetime.utcfromtimestamp(int(unix_timestamp)).strftime("%Y%m%d%H%M%S")


def wayback_timestamp(**kwargs: int) -> str:
    """
    Prepends zero before the year, month, day, hour and minute so that they
    are conformable with the YYYYMMDDhhmmss Wayback Machine timestamp format.
    """
    return "".join(
        str(kwargs[key]).zfill(2) for key in ["year", "month", "day", "hour", "minute"]
    )
