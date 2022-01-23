import pytest
import time
from datetime import datetime

from waybackpy.save_api import WaybackMachineSaveAPI


def test_save():
    url = "https://github.com/akamhy/waybackpy"
    user_agent = "Mozilla/5.0 (MacBook Air; M1 Mac OS X 11_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/604.1"
    save_api = WaybackMachineSaveAPI(url, user_agent)
    save_api.save()
    archive_url = save_api.archive_url
    timestamp = save_api.timestamp()
    headers = save_api.headers  # CaseInsensitiveDict
    cached_save = save_api.cached_save
    assert cached_save in [True, False]
    assert archive_url.find("github.com/akamhy/waybackpy") != -1
    assert str(headers).find("github.com/akamhy/waybackpy") != -1
    assert type(save_api.timestamp()) == type(datetime(year=2020, month=10, day=2))
