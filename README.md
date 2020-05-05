# waybackpy
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/936204c526e34b808c3eef37c516eff6)](https://www.codacy.com/manual/akamhy/pywayback?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=akamhy/pywayback&amp;utm_campaign=Badge_Grade)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/akamhy/waybackpy/blob/master/LICENSE)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/akamhy/waybackpy/graphs/commit-activity)



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

* [Tests](#tests)

* [Dependency](#dependency)

* [License](#license)

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
<details><summary>Output of the above code</summary>
<p>

###### The source code for <https://example.com/> ! As no encoding was provided, it was auto identified.

```html
<!doctype html>
<html>
<head>
    <title>Example Domain</title>

    <meta charset="utf-8" />
    <meta http-equiv="Content-type" content="text/html; charset=utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <style type="text/css">
    body {
        background-color: #f0f0f2;
        margin: 0;
        padding: 0;
        font-family: -apple-system, system-ui, BlinkMacSystemFont, "Segoe UI", "Open Sans", "Helvetica Neue", Helvetica, Arial, sans-serif;
        
    }
    div {
        width: 600px;
        margin: 5em auto;
        padding: 2em;
        background-color: #fdfdff;
        border-radius: 0.5em;
        box-shadow: 2px 3px 7px 2px rgba(0,0,0,0.02);
    }
    a:link, a:visited {
        color: #38488f;
        text-decoration: none;
    }
    @media (max-width: 700px) {
        div {
            margin: 0 auto;
            width: auto;
        }
    }
    </style>    
</head>

<body>
<div>
    <h1>Example Domain</h1>
    <p>This domain is for use in illustrative examples in documents. You may use this
    domain in literature without prior coordination or asking for permission.</p>
    <p><a href="https://www.iana.org/domains/example">More information...</a></p>
</div>
</body>
</html>
```

</p>
</details>

## Dependency
* None, just python standard libraries. Both python 2 and 3 are supported :)


## License

[MIT License](LICENSE)
