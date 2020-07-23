# -*- coding: utf-8 -*-
import sys
import os
import pytest
import argparse

sys.path.append("..")
import waybackpy.cli as cli  # noqa: E402
from waybackpy.wrapper import  Url  # noqa: E402

if sys.version_info > (3, 7):
    def test_save():
        obj = Url("https://pypi.org/user/akamhy/", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/8.0.8 Safari/600.8.9")
        cli._save(obj)
else:
    pass

def test_get():
    args = argparse.Namespace(get='oldest')
    obj = Url("https://pypi.org/user/akamhy/", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/8.0.8 Safari/600.8.9")
    cli._get(obj, args)
    args = argparse.Namespace(get='newest')
    cli._get(obj, args)
    args = argparse.Namespace(get='url')
    cli._get(obj, args)
    if sys.version_info > (3, 7):
        args = argparse.Namespace(get='save')
        cli._get(obj, args)
    else:
        pass

def test_oldest():
    obj = Url("https://pypi.org/user/akamhy/", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/8.0.8 Safari/600.8.9")
    cli._oldest(obj)

def test_newest():
    obj = Url("https://pypi.org/user/akamhy/", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/8.0.8 Safari/600.8.9")
    cli._newest(obj)

def test_near():
    args = argparse.Namespace(year=2020, month=6, day=1, hour=1, minute=1)
    obj = Url("https://pypi.org/user/akamhy/", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/8.0.8 Safari/600.8.9")
    cli._near(obj, args)
