from waybackpy import __version__
from waybackpy.utils import (
    DEFAULT_USER_AGENT,
    latest_version_github,
    latest_version_pypi,
)


def test_default_user_agent() -> None:
    assert (
        DEFAULT_USER_AGENT
        == f"waybackpy {__version__} - https://github.com/akamhy/waybackpy"
    )


def test_latest_version() -> None:
    package_name = "waybackpy"
    assert latest_version_github(package_name) == latest_version_pypi(package_name)
