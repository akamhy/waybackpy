# waybackpy
The waybackpy is python wrapper for [Internet Archive](https://en.wikipedia.org/wiki/Internet_Archive)
's [Wayback Machine](https://en.wikipedia.org/wiki/Wayback_Machine).

## Usage

### Capturing/Saving a url/website. Using save() function.

waybackpy.save(url, UA=user_agent)

```python
import waybackpy
# Capturing a new archive on wayback machine.
# Default user-agent (UA) is "waybackpy python package", if not specified in the call.
archived_url = waybackpy.save("https://github.com/akamhy/waybackpy", UA = "Any-User-Agent")
print(archived_url)
```
```
https://web.archive.org/web/20200504141153/https://github.com/akamhy/waybackpy
```
