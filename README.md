# waybackpy
[![Build Status](https://travis-ci.org/akamhy/waybackpy.svg?branch=master)](https://travis-ci.org/akamhy/waybackpy)
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
[![contributions welcome](https://img.shields.io/static/v1.svg?label=Contributions&message=Welcome&color=0059b3&style=flat-square)](https://github.com/akamhy/waybackpy/blob/master/CONTRIBUTING.md)


![Internet Archive](https://upload.wikimedia.org/wikipedia/commons/thumb/8/84/Internet_Archive_logo_and_wordmark.svg/84px-Internet_Archive_logo_and_wordmark.svg.png)
![Wayback Machine](https://upload.wikimedia.org/wikipedia/commons/thumb/0/01/Wayback_Machine_logo_2010.svg/284px-Wayback_Machine_logo_2010.svg.png)

The waybackpy is a python wrapper for [Internet Archive](https://en.wikipedia.org/wiki/Internet_Archive)'s [Wayback Machine](https://en.wikipedia.org/wiki/Wayback_Machine).

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

* [License](https://github.co#license)

<!--te-->

## Installation
Using [pip](https://en.wikipedia.org/wiki/Pip_(package_manager)):

**pip install waybackpy**



## Usage

#### Capturing aka Saving an url Using save()

```diff
+ waybackpy.save(url, UA=user_agent)
```
> url is mandatory. UA is not, but highly recommended.
```python
import waybackpy
# Capturing a new archive on Wayback machine.
# Default user-agent (UA) is "waybackpy python package", if not specified in the call.
archived_url = waybackpy.save("https://github.com/akamhy/waybackpy", UA = "Any-User-Agent")
print(archived_url)
```
This should print something similar to the following archived URL:

<https://web.archive.org/web/20200504141153/https://github.com/akamhy/waybackpy>

#### Receiving the oldest archive for an URL Using oldest()

```diff
+ waybackpy.oldest(url, UA=user_agent)
```
> url is mandatory. UA is not, but highly recommended.


```python
import waybackpy
# retrieving the oldest archive on Wayback machine.
# Default user-agent (UA) is "waybackpy python package", if not specified in the call.
oldest_archive = waybackpy.oldest("https://www.google.com/", UA = "Any-User-Agent")
print(oldest_archive)
```
This returns the oldest available archive for <https://google.com>.

<http://web.archive.org/web/19981111184551/http://google.com:80/>

#### Receiving the newest archive for an URL using newest()

```diff
+ waybackpy.newest(url, UA=user_agent)
```
> url is mandatory. UA is not, but highly recommended.


```python
import waybackpy
# retrieving the newest archive on Wayback machine.
# Default user-agent (UA) is "waybackpy python package", if not specified in the call.
newest_archive = waybackpy.newest("https://www.microsoft.com/en-us", UA = "Any-User-Agent")
print(newest_archive)
```
This returns the newest available archive for <https://www.microsoft.com/en-us>, something just like this:

<http://web.archive.org/web/20200429033402/https://www.microsoft.com/en-us/>

#### Receiving archive close to a specified year, month, day, hour, and minute using near()

```diff
+ waybackpy.near(url, year=2020, month=1, day=1, hour=1, minute=1, UA=user_agent)
```
> url is mandotory. year,month,day,hour and minute are optional arguments. UA is not mandotory, but higly recomended.


```python
import waybackpy
# retriving the the closest archive from a specified year.
# Default user-agent (UA) is "waybackpy python package", if not specified in the call.
# supported argumnets are year,month,day,hour and minute
archive_near_year = waybackpy.near("https://www.facebook.com/", year=2010, UA ="Any-User-Agent")
print(archive_near_year)
```
returns : <http://web.archive.org/web/20100504071154/http://www.facebook.com/>

```waybackpy.near("https://www.facebook.com/", year=2010, month=1, UA ="Any-User-Agent")``` returns: <http://web.archive.org/web/20101111173430/http://www.facebook.com//>

```waybackpy.near("https://www.oracle.com/index.html", year=2019, month=1, day=5, UA ="Any-User-Agent")``` returns: <http://web.archive.org/web/20190105054437/https://www.oracle.com/index.html>
> Please note that if you only specify the year, the current month and day are default arguments for month and day respectively. Do not expect just putting the year parameter would return the archive closer to January but the current month you are using the package. If you are using it in July 2018 and let's say you use ```waybackpy.near("https://www.facebook.com/", year=2011, UA ="Any-User-Agent")``` then you would be returned the nearest archive to July 2011 and not January 2011. You need to specify the month "1" for January.

> Do not pad (don't use zeros in the month, year, day, minute, and hour arguments). e.g. For January, set month = 1 and not month = 01.

#### Get the content of webpage using get()

```diff
+ waybackpy.get(url, encoding="UTF-8", UA=user_agent)
```
> url is mandatory. UA is not, but highly recommended. encoding is detected automatically, don't specify unless necessary.

```python
from waybackpy import get
# retriving the webpage from any url including the archived urls. Don't need to import other libraies :)
# Default user-agent (UA) is "waybackpy python package", if not specified in the call.
# supported argumnets are url, encoding and UA
webpage = get("https://example.com/", UA="User-Agent")
print(webpage)
```
> This should print the source code for <https://example.com/>.

#### Count total archives for an URL using total_archives()

```diff
+ waybackpy.total_archives(url, UA=user_agent)
```
> url is mandatory. UA is not, but highly recommended.

```python
from waybackpy import total_archives
# retriving the webpage from any url including the archived urls. Don't need to import other libraies :)
# Default user-agent (UA) is "waybackpy python package", if not specified in the call.
# supported argumnets are url and UA
count = total_archives("https://en.wikipedia.org/wiki/Python (programming language)", UA="User-Agent")
print(count)
```
> This should print an integer (int), which is the number of total archives on archive.org

## Tests
* [Here](https://github.com/akamhy/waybackpy/tree/master/tests)

## Dependency
* None, just python standard libraries (json, urllib and datetime). Both python 2 and 3 are supported :)


## License

[MIT License](https://github.com/akamhy/waybackpy/blob/master/LICENSE)
