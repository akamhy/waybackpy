"""Module initializer and provider of static information."""

__version__ = "3.0.6"

from .availability_api import WaybackMachineAvailabilityAPI
from .cdx_api import WaybackMachineCDXServerAPI
from .save_api import WaybackMachineSaveAPI
from .wrapper import Url

__all__ = [
    "__version__",
    "WaybackMachineAvailabilityAPI",
    "WaybackMachineCDXServerAPI",
    "WaybackMachineSaveAPI",
    "Url",
]
