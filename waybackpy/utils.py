"""
Utility functions and shared variables like DEFAULT_USER_AGENT are here.
"""

from . import __version__

DEFAULT_USER_AGENT: str = (
    f"waybackpy {__version__} - https://github.com/akamhy/waybackpy"
)
