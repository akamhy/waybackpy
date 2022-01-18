<div align="center">

<img src="https://raw.githubusercontent.com/akamhy/waybackpy/master/assets/waybackpy_logo.svg"><br>

<h3>Python package & CLI tool that interfaces with the Wayback Machine API</h3>

</div>

<p align="center">
<a href="https://pypi.org/project/waybackpy/"><img alt="pypi" src="https://img.shields.io/pypi/v/waybackpy.svg"></a>
<a href="https://github.com/akamhy/waybackpy/blob/master/CONTRIBUTING.md"><img alt="Contributions Welcome" src="https://img.shields.io/static/v1.svg?label=Contributions&message=Welcome&color=0059b3&style=flat-square"></a>
<a href="https://pepy.tech/project/waybackpy?versions=2*&versions=1*&versions=3*"><img alt="Downloads" src="https://pepy.tech/badge/waybackpy/month"></a>
<a href="https://github.com/akamhy/waybackpy/commits/master"><img alt="GitHub lastest commit" src="https://img.shields.io/github/last-commit/akamhy/waybackpy?color=blue&style=flat-square"></a>
<a href="#"><img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/waybackpy?style=flat-square"></a>
</p>

-----------------------------------------------------------------------------------------------------------------------------------------------

## ⭐️ Introduction
Waybackpy is a [Python package](https://www.udacity.com/blog/2021/01/what-is-a-python-package.html) and a CLI tool that interfaces with the Wayback Machine API.

 Wayback Machine has 3 client side APIs.

  - Save API
  - Availability API
  - CDX API

All three of these can be accessed by waybackpy.


### 🏗 Installation

Using [pip](https://en.wikipedia.org/wiki/Pip_(package_manager)):

```bash
pip install waybackpy
```

Install directly from GitHub:

```bash
pip install git+https://github.com/akamhy/waybackpy.git
```

### Docker Image
Docker Hub : <https://hub.docker.com/r/secsi/waybackpy>

Docker image is automatically updated on every release by [Regulary and Automatically Updated Docker Images](https://github.com/cybersecsi/RAUDI) (RAUDI). 

RAUDI is a tool by SecSI (<https://secsi.io>), an Italian cybersecurity startup.



### Usage

#### As a Python package

##### Save API aka SavePageNow
```python
>>> from waybackpy import WaybackMachineSaveAPI
>>> url = "https://github.com"
>>> user_agent = "Mozilla/5.0 (Windows NT 5.1; rv:40.0) Gecko/20100101 Firefox/40.0"
>>> 
>>> save_api = WaybackMachineSaveAPI(url, user_agent)
>>> save_api.save()
https://web.archive.org/web/20220118125249/https://github.com/
>>> save_api.cached_save
False
>>> save_api.timestamp()
datetime.datetime(2022, 1, 18, 12, 52, 49)
```

##### Availability API
```python
>>> from waybackpy import WaybackMachineAvailabilityAPI
>>> 
>>> url = "https://google.com"
>>> user_agent = "Mozilla/5.0 (Windows NT 5.1; rv:40.0) Gecko/20100101 Firefox/40.0"
>>> 
>>> availability_api = WaybackMachineAvailabilityAPI(url, user_agent)
>>> 
>>> availability_api.oldest()
https://web.archive.org/web/19981111184551/http://google.com:80/
>>> 
>>> availability_api.newest()
https://web.archive.org/web/20220118150444/https://www.google.com/
>>> 
>>> availability_api.near(year=2010, month=10, day=10, hour=10)
https://web.archive.org/web/20101010101708/http://www.google.com/
```

##### CDX API aka CDXServerAPI
```python
>>> from waybackpy import WaybackMachineCDXServerAPI
>>> url = "https://pypi.org"
>>> user_agent = "Mozilla/5.0 (Windows NT 5.1; rv:40.0) Gecko/20100101 Firefox/40.0"
>>> cdx = WaybackMachineCDXServerAPI(url, user_agent, start_timestamp=2016, end_timestamp=2017)
>>> for item in cdx.snapshots():
...     print(item.archive_url)
... 
https://web.archive.org/web/20160110011047/http://pypi.org/
https://web.archive.org/web/20160305104847/http://pypi.org/
.
. # URLS REDACTED FOR READABILITY
.
https://web.archive.org/web/20171127171549/https://pypi.org/
https://web.archive.org/web/20171206002737/http://pypi.org:80/
```

> Documentation at <https://github.com/akamhy/waybackpy/wiki/Python-package-docs>.


#### As a CLI tool
```bash
$ waybackpy --save --url "https://en.wikipedia.org/wiki/Social_media" --user_agent "my-unique-user-agent"
https://web.archive.org/web/20200719062108/https://en.wikipedia.org/wiki/Social_media

$ waybackpy --oldest --url "https://en.wikipedia.org/wiki/Humanoid" --user_agent "my-unique-user-agent"
https://web.archive.org/web/20040415020811/http://en.wikipedia.org:80/wiki/Humanoid

$ waybackpy --newest --url "https://en.wikipedia.org/wiki/Remote_sensing" --user_agent "my-unique-user-agent"
https://web.archive.org/web/20201221130522/https://en.wikipedia.org/wiki/Remote_sensing
```
> CLI documentation is at <https://github.com/akamhy/waybackpy/wiki/CLI-docs>.

### 🛡 License
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/akamhy/waybackpy/blob/master/LICENSE)

Released under the MIT License. See [license](https://github.com/akamhy/waybackpy/blob/master/LICENSE) for details.
