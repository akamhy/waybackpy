from waybackpy.utils import (
    latest_version_pypi,
    latest_version_github,
    DEFAULT_USER_AGENT,
)
from waybackpy.__version__ import __version__


def test_default_user_agent():
    assert (
        DEFAULT_USER_AGENT
        == "waybackpy %s - https://github.com/akamhy/waybackpy" % __version__
    )


def test_latest_version():
    package_name = "waybackpy"
    assert latest_version_github(package_name) == latest_version_pypi(package_name)
