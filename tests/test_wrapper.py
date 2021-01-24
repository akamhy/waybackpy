import sys
import pytest
import random
import requests
from datetime import datetime

from waybackpy.wrapper import Url


user_agent = "Mozilla/5.0 (Windows NT 6.2; rv:20.0) Gecko/20121202 Firefox/20.0"


def test_url_check():
    """No API Use"""
    broken_url = "http://wwwgooglecom/"
    with pytest.raises(Exception):
        Url(broken_url, user_agent)


def test_near():
    with pytest.raises(Exception):
        NeverArchivedUrl = (
            "https://ee_3n.wrihkeipef4edia.org/rwti5r_ki/Nertr6w_rork_rse7c_urity"
        )
        target = Url(NeverArchivedUrl, user_agent)
        target.near(year=2010)


def test_json():
    url = "github.com/akamhy/waybackpy"
    target = Url(url, user_agent)
    assert "archived_snapshots" in str(target.JSON)
