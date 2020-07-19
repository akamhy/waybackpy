# waybackpy

[![Build Status](https://img.shields.io/travis/akamhy/waybackpy.svg?label=Travis%20CI&logo=travis&style=flat-square)](https://travis-ci.org/akamhy/waybackpy)
[![Downloads](https://img.shields.io/pypi/dm/waybackpy.svg)](https://pypistats.org/packages/waybackpy)
[![Release](https://img.shields.io/github/v/release/akamhy/waybackpy.svg)](https://github.com/akamhy/waybackpy/releases)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/255459cede9341e39436ec8866d3fb65)](https://www.codacy.com/manual/akamhy/waybackpy?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=akamhy/waybackpy&amp;utm_campaign=Badge_Grade)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/akamhy/waybackpy/blob/master/LICENSE)
[![Maintainability](https://api.codeclimate.com/v1/badges/942f13d8177a56c1c906/maintainability)](https://codeclimate.com/github/akamhy/waybackpy/maintainability)
[![CodeFactor](https://www.codefactor.io/repository/github/akamhy/waybackpy/badge)](https://www.codefactor.io/repository/github/akamhy/waybackpy)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
![pypi](https://img.shields.io/pypi/v/waybackpy.svg)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/waybackpy?style=flat-square)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/akamhy/waybackpy/graphs/commit-activity)
[![codecov](https://codecov.io/gh/akamhy/waybackpy/branch/master/graph/badge.svg)](https://codecov.io/gh/akamhy/waybackpy)
![](https://img.shields.io/github/repo-size/akamhy/waybackpy.svg?label=Repo%20size&style=flat-square)
![contributions welcome](https://img.shields.io/static/v1.svg?label=Contributions&message=Welcome&color=0059b3&style=flat-square)


![Internet Archive](https://upload.wikimedia.org/wikipedia/commons/thumb/8/84/Internet_Archive_logo_and_wordmark.svg/84px-Internet_Archive_logo_and_wordmark.svg.png)
![Wayback Machine](https://upload.wikimedia.org/wikipedia/commons/thumb/0/01/Wayback_Machine_logo_2010.svg/284px-Wayback_Machine_logo_2010.svg.png)

Waybackpy is a Python library that interfaces with the [Internet Archive](https://en.wikipedia.org/wiki/Internet_Archive)'s [Wayback Machine](https://en.wikipedia.org/wiki/Wayback_Machine) API. Archive pages and retrieve archived pages easily.

Table of contents
=================
<!--ts-->

* [Installation](#installation)

* [Usage](#usage)
  * [Saving an url using save()](#capturing-aka-saving-an-url-using-save)
  * [Receiving the oldest archive for an URL Using oldest()](#receiving-the-oldest-archive-for-an-url-using-oldest)
  * [Receiving the recent most/newest archive for an URL using newest()](#receiving-the-newest-archive-for-an-url-using-newest)
  * [Receiving archive close to a specified year, month, day, hour, and minute using near()](#receiving-archive-close-to-a-specified-year-month-day-hour-and-minute-using-near)
  * [Get the content of webpage using get()](#get-the-content-of-webpage-using-get)
  * [Count total archives for an URL using total_archives()](#count-total-archives-for-an-url-using-total_archives)


* [Tests](#tests)

* [Dependency](#dependency)

* [License](#license)

<!--te-->

## Installation
Using [pip](https://en.wikipedia.org/wiki/Pip_(package_manager)):
```bash
pip install waybackpy
```


## Usage

#### Capturing aka Saving an url using save()
```python
import waybackpy

new_archive_url = waybackpy.Url(

    url = "https://en.wikipedia.org/wiki/Multivariable_calculus",
    user_agent = "Mozilla/5.0 (Windows NT 5.1; rv:40.0) Gecko/20100101 Firefox/40.0"
    
).save()

print(new_archive_url)
```
```bash
https://web.archive.org/web/20200504141153/https://github.com/akamhy/waybackpy
```
<sub>Try this out in your browser @ <https://repl.it/@akamhy/WaybackPySaveExample></sub>



#### Receiving the oldest archive for an URL using oldest()
```python
import waybackpy

oldest_archive_url = waybackpy.Url(

    "https://www.google.com/",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:40.0) Gecko/20100101 Firefox/40.0"
    
).oldest()

print(oldest_archive_url)
```
```bash
http://web.archive.org/web/19981111184551/http://google.com:80/
```
<sub>Try this out in your browser @ <https://repl.it/@akamhy/WaybackPyOldestExample></sub>



#### Receiving the newest archive for an URL using newest()
```python
import waybackpy

newest_archive_url = waybackpy.Url(

    "https://www.facebook.com/",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:39.0) Gecko/20100101 Firefox/39.0"
    
).newest()

print(newest_archive_url)
```
```bash
https://web.archive.org/web/20200714013225/https://www.facebook.com/
```
<sub>Try this out in your browser @ <https://repl.it/@akamhy/WaybackPyNewestExample></sub>



#### Receiving archive close to a specified year, month, day, hour, and minute using near()
```python
from waybackpy import Url

user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:38.0) Gecko/20100101 Firefox/38.0"
github_url = "https://github.com/"


github_wayback_obj = Url(github_url, user_agent)

# Do not pad (don't use zeros in the month, year, day, minute, and hour arguments). e.g. For January, set month = 1 and not month = 01.
```
```python
github_archive_near_2010 = github_wayback_obj.near(year=2010)
print(github_archive_near_2010)
```
```bash
https://web.archive.org/web/20100719134402/http://github.com/
```
```python
github_archive_near_2011_may = github_wayback_obj.near(year=2011, month=5)
print(github_archive_near_2011_may)
```
```bash
https://web.archive.org/web/20110519185447/https://github.com/
```
```python
github_archive_near_2015_january_26 = github_wayback_obj.near(
    year=2015, month=1, day=26
)
print(github_archive_near_2015_january_26)
```
```bash
https://web.archive.org/web/20150127031159/https://github.com
```
```python
github_archive_near_2018_4_july_9_2_am = github_wayback_obj.near(
    year=2018, month=7, day=4, hour = 9, minute = 2
)
print(github_archive_near_2018_4_july_9_2_am)
```
```bash
https://web.archive.org/web/20180704090245/https://github.com/

```

<sub>The library doesn't supports seconds yet. You are encourged to create a PR ;)</sub>

<sub>Try this out in your browser @ <https://repl.it/@akamhy/WaybackPyNearExample></sub>



#### Get the content of webpage using get()
```python
import waybackpy

google_url = "https://www.google.com/"

User_Agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36"

waybackpy_url_object = waybackpy.Url(google_url, User_Agent)


# If no argument is passed in get(), it gets the source of the Url used to create the object.
current_google_url_source = waybackpy_url_object.get()
print(current_google_url_source)


# The following chunk of code will force a new archive of google.com and get the source of the archived page.
# waybackpy_url_object.save() type is string.
google_newest_archive_source = waybackpy_url_object.get(
    waybackpy_url_object.save()
)
print(google_newest_archive_source)


# waybackpy_url_object.oldest() type is str, it's oldest archive of google.com
google_oldest_archive_source = waybackpy_url_object.get(
    waybackpy_url_object.oldest()
)
print(google_oldest_archive_source)
```
<sub>Try this out in your browser @ <https://repl.it/@akamhy/WaybackPyGetExample#main.py></sub>


#### Count total archives for an URL using total_archives()
```python
import waybackpy

URL = "https://en.wikipedia.org/wiki/Python (programming language)"

UA = "Mozilla/5.0 (iPad; CPU OS 8_1_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B435 Safari/600.1.4"

archive_count = waybackpy.Url(
    url=URL,
    user_agent=UA
).total_archives()

print(archive_count) # total_archives() returns an int
```
```bash
2440
```
<sub>Try this out in your browser @ <https://repl.it/repls/DigitalUnconsciousNumbers#main.py></sub>

## Tests
* [Here](https://github.com/akamhy/waybackpy/tree/master/tests)


## Dependency
* None, just python standard libraries (re, json, urllib and datetime). Both python 2 and 3 are supported :)


## License
[MIT License](https://github.com/akamhy/waybackpy/blob/master/LICENSE)
