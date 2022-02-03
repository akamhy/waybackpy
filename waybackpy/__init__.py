__title__ = "waybackpy"
__description__ = (
    "Python package that interfaces with the Internet Archive's Wayback Machine APIs. "
    "Archive pages and retrieve archived pages easily."
)
__url__ = "https://akamhy.github.io/waybackpy/"
__version__ = "3.0.2"
__download_url__ = (
    "https://github.com/akamhy/waybackpy/archive/{version}.tar.gz".format(
        version=__version__
    )
)
__author__ = "Akash Mahanty"
__author_email__ = "akamhy@yahoo.com"
__license__ = "MIT"
__copyright__ = "Copyright 2020-2022 Akash Mahanty et al."

from .availability_api import WaybackMachineAvailabilityAPI
from .cdx_api import WaybackMachineCDXServerAPI
from .save_api import WaybackMachineSaveAPI
from .wrapper import Url

__all__ = [
    "__author__",
    "__author_email__",
    "__copyright__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__download_url__",
    "__version__",
    "WaybackMachineAvailabilityAPI",
    "WaybackMachineCDXServerAPI",
    "WaybackMachineSaveAPI",
    "Url",
]
