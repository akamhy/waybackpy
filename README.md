# waybackpy
The waybackpy is python wrapper for [Internet Archive](https://en.wikipedia.org/wiki/Internet_Archive)
's [Wayback Machine](https://en.wikipedia.org/wiki/Wayback_Machine).

## Usage

### Capturing/Saving a url/website. Using save().

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

### Retiving the oldest archive for a url. Using oldest().

waybackpy.oldest(url, UA=user_agent)

```python
import waybackpy
# retriving the oldest archive on wayback machine.
# Default user-agent (UA) is "waybackpy python package", if not specified in the call.
oldest_archive = waybackpy.oldest("https://www.google.com/", UA = "Any-User-Agent")
print(oldest_archive)
```
This returns the oldest available archive for google.com (Check it out! It's really fascinating! and follow those blue links.)
```
http://web.archive.org/web/19981111184551/http://google.com:80/
```
