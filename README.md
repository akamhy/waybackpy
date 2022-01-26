<div align="center">

<img src="https://raw.githubusercontent.com/akamhy/waybackpy/master/assets/waybackpy_logo.svg"><br>

<h3>A Python package & CLI tool that interfaces with the Wayback Machine API</h3>

</div>

<p align="center">
<a href="https://github.com/akamhy/waybackpy/actions?query=workflow%3ATests"><img alt="Unit Tests" src="https://github.com/akamhy/waybackpy/workflows/Tests/badge.svg"></a>
<a href="https://pypi.org/project/waybackpy/"><img alt="pypi" src="https://img.shields.io/pypi/v/waybackpy.svg"></a>
<a href="https://pepy.tech/project/waybackpy?versions=2*&versions=1*&versions=3*"><img alt="Downloads" src="https://pepy.tech/badge/waybackpy/month"></a>
<a href="https://github.com/akamhy/waybackpy/commits/master"><img alt="GitHub lastest commit" src="https://img.shields.io/github/last-commit/akamhy/waybackpy?color=blue&style=flat-square"></a>
<a href="#"><img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/waybackpy?style=flat-square"></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
</p>

-----------------------------------------------------------------------------------------------------------------------------------------------

## ⭐️ Introduction
Waybackpy is a [Python package](https://www.udacity.com/blog/2021/01/what-is-a-python-package.html) and a [CLI](https://www.w3schools.com/whatis/whatis_cli.asp) tool that interfaces with the [Wayback Machine](https://en.wikipedia.org/wiki/Wayback_Machine) API.

 Wayback Machine has 3 client side [API](https://www.redhat.com/en/topics/api/what-are-application-programming-interfaces)s.

  - [Save API](https://github.com/akamhy/waybackpy/wiki/Wayback-Machine-APIs#save-api)
  - [Availability API](https://github.com/akamhy/waybackpy/wiki/Wayback-Machine-APIs#availability-api)
  - [CDX API](https://github.com/akamhy/waybackpy/wiki/Wayback-Machine-APIs#cdx-api)

These three APIs can be accessed via the waybackpy either by importing it in a script or from the CLI.


### 🏗 Installation

**Using [pip](https://en.wikipedia.org/wiki/Pip_(package_manager)), from [PyPI](https://pypi.org/) (recommended)**:

```bash
pip install waybackpy
```


**Using [conda](https://en.wikipedia.org/wiki/Conda_(package_manager)), from [conda-forge](https://conda-forge.org/) (recommended)**:

See also [waybackpy feedstock](https://github.com/conda-forge/waybackpy-feedstock).

```bash
conda install waybackpy
```


**Install directly from [this git repository](https://github.com/akamhy/waybackpy) (NOT recommended)**:

```bash
pip install git+https://github.com/akamhy/waybackpy.git
```


### 🐳 Docker Image
Docker Hub : <https://hub.docker.com/r/secsi/waybackpy>

[Docker image](https://searchitoperations.techtarget.com/definition/Docker-image) is automatically updated on every release by [Regulary and Automatically Updated Docker Images](https://github.com/cybersecsi/RAUDI) (RAUDI).

RAUDI is a tool by SecSI (<https://secsi.io>), an Italian cybersecurity startup.


### 🚀 Usage

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

> Documentation is at <https://github.com/akamhy/waybackpy/wiki/Python-package-docs>.


#### As a CLI tool

Demo video on [asciinema.org](https://asciinema.org), you can copy the text from video:

[![asciicast](https://asciinema.org/a/464367.svg)](https://asciinema.org/a/464367)

> CLI documentation is at <https://github.com/akamhy/waybackpy/wiki/CLI-docs>.

### 🛡 License
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/akamhy/waybackpy/blob/master/LICENSE)

Copyright (c) 2020-2022 Akash Mahanty Et al.

Released under the MIT License. See [license](https://github.com/akamhy/waybackpy/blob/master/LICENSE) for details.
