# waybackpy
The waybackpy is python wrapper for [Internet Archive](https://en.wikipedia.org/wiki/Internet_Archive)
's [Wayback Machine](https://en.wikipedia.org/wiki/Wayback_Machine).

## Usage

### Capturing/Saving an url/website. Using save().

waybackpy.save(url, UA=user_agent)

```python
import waybackpy
# Capturing a new archive on wayback machine.
# Default user-agent (UA) is "waybackpy python package", if not specified in the call.
archived_url = waybackpy.save("https://github.com/akamhy/waybackpy", UA = "Any-User-Agent")
print(archived_url)
```
This should print something similar to the following archived url:
```
https://web.archive.org/web/20200504141153/https://github.com/akamhy/waybackpy
```

### Retiving the oldest archive for an url. Using oldest().

waybackpy.oldest(url, UA=user_agent)

```python
import waybackpy
# retriving the oldest archive on wayback machine.
# Default user-agent (UA) is "waybackpy python package", if not specified in the call.
oldest_archive = waybackpy.oldest("https://www.google.com/", UA = "Any-User-Agent")
print(oldest_archive)
```
This returns the oldest available archive for <https://google.com> (Check it out! It's really fascinating! and follow those blue links.)
```
http://web.archive.org/web/19981111184551/http://google.com:80/
```

### Retiving the recent most/newest archive for an url. Using newest().

waybackpy.newest(url, UA=user_agent)

```python
import waybackpy
# retriving the newest archive on wayback machine.
# Default user-agent (UA) is "waybackpy python package", if not specified in the call.
newest_archive = waybackpy.newest("https://www.microsoft.com/en-us", UA = "Any-User-Agent")
print(newest_archive)
```
This returns the newest available archive for <https://www.microsoft.com/en-us>, somthing just like this:
```
http://web.archive.org/web/20200429033402/https://www.microsoft.com/en-us/
```

### Retiving archive close to a specified year, month, day, hour and minute!. Using near().

waybackpy.newest(url, year=2020, month=01, day=01, hour=01, minute=01, UA=user_agent)

```python
import waybackpy
# retriving the the closest archive from a specified year.
# Default user-agent (UA) is "waybackpy python package", if not specified in the call.
# supported argumnets are year,month,day,hour and minute
archive_near_year = waybackpy.near("https://www.facebook.com/", year=2010, UA ="Any-User-Agent")
print(archive_near_year)
```
returns : ```http://web.archive.org/web/20100504071154/http://www.facebook.com/```

