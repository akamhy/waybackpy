# waybackpy

![Internet Archive](https://upload.wikimedia.org/wikipedia/commons/thumb/8/84/Internet_Archive_logo_and_wordmark.svg/84px-Internet_Archive_logo_and_wordmark.svg.png)
![Wayback Machine](https://upload.wikimedia.org/wikipedia/commons/thumb/0/01/Wayback_Machine_logo_2010.svg/284px-Wayback_Machine_logo_2010.svg.png)


The waybackpy is a python wrapper for [Internet Archive](https://en.wikipedia.org/wiki/Internet_Archive)
's [Wayback Machine](https://en.wikipedia.org/wiki/Wayback_Machine).

## Installation
Using [pip](https://en.wikipedia.org/wiki/Pip_(package_manager)):

**pip install waybackpy**



## Usage

#### Capturing/Saving an url/website. Using save().

```diff
+ waybackpy.save(url, UA=user_agent)
```

```python
import waybackpy
# Capturing a new archive on wayback machine.
# Default user-agent (UA) is "waybackpy python package", if not specified in the call.
archived_url = waybackpy.save("https://github.com/akamhy/waybackpy", UA = "Any-User-Agent")
print(archived_url)
```
This should print something similar to the following archived URL:

<https://web.archive.org/web/20200504141153/https://github.com/akamhy/waybackpy>

#### Receiving the oldest archive for an URL. Using oldest().

```diff
+ waybackpy.oldest(url, UA=user_agent)
```


```python
import waybackpy
# retrieving the oldest archive on Wayback machine.
# Default user-agent (UA) is "waybackpy python package", if not specified in the call.
oldest_archive = waybackpy.oldest("https://www.google.com/", UA = "Any-User-Agent")
print(oldest_archive)
```
This returns the oldest available archive for <https://google.com>.

<http://web.archive.org/web/19981111184551/http://google.com:80/>

#### Receiving the recent most/newest archive for an URL. Using newest().

```diff
+ waybackpy.newest(url, UA=user_agent)
```

```python
import waybackpy
# retrieving the newest archive on Wayback machine.
# Default user-agent (UA) is "waybackpy python package", if not specified in the call.
newest_archive = waybackpy.newest("https://www.microsoft.com/en-us", UA = "Any-User-Agent")
print(newest_archive)
```
This returns the newest available archive for <https://www.microsoft.com/en-us>, something just like this:

<http://web.archive.org/web/20200429033402/https://www.microsoft.com/en-us/>

#### Receiving archive close to a specified year, month, day, hour, and minute! Using near().

```diff
+ waybackpy.near(url, year=2020, month=1, day=1, hour=1, minute=1, UA=user_agent)
```

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

> Do not pad (use zeros in month, year, day, minute and hour arguments).

#### Get the content of webpage using get().

```diff
+ waybackpy.get(url, encoding="UTF-8", UA=user_agent)
```

## License

[MIT License](LICENSE)
