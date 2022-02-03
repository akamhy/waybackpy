import requests

from .__version__ import __version__

DEFAULT_USER_AGENT = "waybackpy %s - https://github.com/akamhy/waybackpy" % __version__


def latest_version_pypi(package_name, user_agent=DEFAULT_USER_AGENT):
    request_url = "https://pypi.org/pypi/" + package_name + "/json"
    headers = {"User-Agent": user_agent}
    response = requests.get(request_url, headers=headers)
    data = response.json()
    return data["info"]["version"]


def latest_version_github(package_name, user_agent=DEFAULT_USER_AGENT):
    request_url = (
        "https://api.github.com/repos/akamhy/" + package_name + "/releases?per_page=1"
    )
    headers = {"User-Agent": user_agent}
    response = requests.get(request_url, headers=headers)
    data = response.json()
    return data[0]["tag_name"]
