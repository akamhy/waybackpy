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

#### Capturing aka Saving an url Using save()
```python
import waybackpy
# Capturing a new archive on Wayback machine.
target_url = waybackpy.Url("https://github.com/akamhy/waybackpy", user_agent="My-cool-user-agent")
archived_url = target_url.save()
print(archived_url)
```
This should print an URL similar to the following archived URL:

> <https://web.archive.org/web/20200504141153/https://github.com/akamhy/waybackpy>


#### Receiving the oldest archive for an URL Using oldest()
```python
import waybackpy
# retrieving the oldest archive on Wayback machine.
target_url = waybackpy.Url("https://www.google.com/", "My-cool-user-agent")
oldest_archive = target_url.oldest()
print(oldest_archive)
```
This should print the oldest available archive for <https://google.com>.

> <http://web.archive.org/web/19981111184551/http://google.com:80/>


#### Receiving the newest archive for an URL using newest()
```python
import waybackpy
# retrieving the newest/latest archive on Wayback machine.
target_url = waybackpy.Url(url="https://www.google.com/", user_agent="My-cool-user-agent")
newest_archive = target_url.newest()
print(newest_archive)
```
This print the newest available archive for <https://www.microsoft.com/en-us>, something just like this:

> <http://web.archive.org/web/20200429033402/https://www.microsoft.com/en-us/>


#### Receiving archive close to a specified year, month, day, hour, and minute using near()
```python
import waybackpy
# retriving the the closest archive from a specified year.
# supported argumnets are year,month,day,hour and minute
target_url = waybackpy.Url(https://www.facebook.com/", "Any-User-Agent")
archive_near_year = target_url.near(year=2010)
print(archive_near_year)
```
returns : <http://web.archive.org/web/20100504071154/http://www.facebook.com/>

> Please note that if you only specify the year, the current month and day are default arguments for month and day respectively. Just putting the year parameter would not return the archive closer to January but the current month you are using the package. You need to specify the month "1" for January , 2 for february and so on.

> Do not pad (don't use zeros in the month, year, day, minute, and hour arguments). e.g. For January, set month = 1 and not month = 01.


#### Get the content of webpage using get()
```python
import waybackpy
# retriving the webpage from any url including the archived urls. Don't need to import other libraies :)
# supported argumnets encoding and user_agent
target = waybackpy.Url("google.com", "any-user_agent")
oldest_url = target.oldest()
webpage = target.get(oldest_url) # We are getting the source of oldest archive of google.com.
print(webpage)
```
> This should print the source code for oldest archive of google.com. If no URL is passed in get() then it should retrive the source code of google.com and not any archive.

#### Count total archives for an URL using total_archives()
```python
from waybackpy import Url
# retriving the content of a webpage from any url including but not limited to the archived urls.
count = Url("https://en.wikipedia.org/wiki/Python (programming language)", "User-Agent").total_archives()
print(count)
```
> This should print an integer (int), which is the number of total archives on archive.org


## Tests
* [Here](https://github.com/akamhy/waybackpy/tree/master/tests)


## Dependency
* None, just python standard libraries (re, json, urllib and datetime). Both python 2 and 3 are supported :)


## License
[MIT License](https://github.com/akamhy/waybackpy/blob/master/LICENSE)
