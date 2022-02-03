import requests

from . import __version__

DEFAULT_USER_AGENT: str = (
    f"waybackpy {__version__} - https://github.com/akamhy/waybackpy"
)


def latest_version_pypi(package_name: str, user_agent: str = DEFAULT_USER_AGENT) -> str:
    request_url = "https://pypi.org/pypi/" + package_name + "/json"
    headers = {"User-Agent": user_agent}
    response = requests.get(request_url, headers=headers)
    data = response.json()
    if (
        data is not None
        and "info" in data
        and data["info"] is not None
        and "version" in data["info"]
        and data["info"]["version"] is not None
    ):
        return str(data["info"]["version"])
    else:
        raise ValueError("Could not get latest pypi version")


def latest_version_github(
    package_name: str, user_agent: str = DEFAULT_USER_AGENT
) -> str:
    request_url = (
        "https://api.github.com/repos/akamhy/" + package_name + "/releases?per_page=1"
    )
    headers = {"User-Agent": user_agent}
    response = requests.get(request_url, headers=headers)
    data = response.json()
    if (
        data is not None
        and len(data) > 0
        and data[0] is not None
        and "tag_name" in data[0]
    ):
        return str(data[0]["tag_name"])
    else:
        raise ValueError("Could not get latest github version")
