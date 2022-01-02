<div align="center">

<img src="https://raw.githubusercontent.com/akamhy/waybackpy/master/assets/waybackpy_logo.svg"><br>

<h2>Python package & CLI tool that interfaces with the Wayback Machine API</h2>

</div>

-----------------------------------------------------------------------------------------------------------------------------------------------

### Installation

Using [pip](https://en.wikipedia.org/wiki/Pip_(package_manager)):

```bash
pip install waybackpy
```

Install directly from GitHub:

```bash
pip install git+https://github.com/akamhy/waybackpy.git
```

### Supported APIs
 Wayback Machine has 3 client side APIs.

  - Save API
  - Availability API
  - CDX API

All three of these can be accessed by waybackpy.


### Usage

#### As a Python package
```python
>>> import waybackpy

>>> url = "https://en.wikipedia.org/wiki/Multivariable_calculus"
>>> user_agent = "Mozilla/5.0 (Windows NT 5.1; rv:40.0) Gecko/20100101 Firefox/40.0"

>>> wayback = waybackpy.Url(url, user_agent)

>>> archive = wayback.save()
>>> archive.archive_url
'https://web.archive.org/web/20210104173410/https://en.wikipedia.org/wiki/Multivariable_calculus'

>>> archive.timestamp
datetime.datetime(2021, 1, 4, 17, 35, 12, 691741)

>>> oldest_archive = wayback.oldest()
>>> oldest_archive.archive_url
'https://web.archive.org/web/20050422130129/http://en.wikipedia.org:80/wiki/Multivariable_calculus'

>>> archive_close_to_2010_feb = wayback.near(year=2010, month=2)
>>> archive_close_to_2010_feb.archive_url
'https://web.archive.org/web/20100215001541/http://en.wikipedia.org:80/wiki/Multivariable_calculus'

>>> wayback.newest().archive_url
'https://web.archive.org/web/20210104173410/https://en.wikipedia.org/wiki/Multivariable_calculus'
```
> Full Python package documentation can be found at <https://github.com/akamhy/waybackpy/wiki/Python-package-docs>.



#### As a CLI tool
```bash
$ waybackpy --save --url "https://en.wikipedia.org/wiki/Social_media" --user_agent "my-unique-user-agent"
https://web.archive.org/web/20200719062108/https://en.wikipedia.org/wiki/Social_media

$ waybackpy --oldest --url "https://en.wikipedia.org/wiki/Humanoid" --user_agent "my-unique-user-agent"
https://web.archive.org/web/20040415020811/http://en.wikipedia.org:80/wiki/Humanoid

$ waybackpy --newest --url "https://en.wikipedia.org/wiki/Remote_sensing" --user_agent "my-unique-user-agent"
https://web.archive.org/web/20201221130522/https://en.wikipedia.org/wiki/Remote_sensing

$ waybackpy --known_urls --url akamhy.github.io --user_agent "my-unique-user-agent" --file
https://akamhy.github.io
https://akamhy.github.io/assets/js/scale.fix.js
https://akamhy.github.io/favicon.ico
https://akamhy.github.io/robots.txt
https://akamhy.github.io/waybackpy/

'akamhy.github.io-urls-iftor2.txt' saved in current working directory
```
> Full CLI documentation can be found at <https://github.com/akamhy/waybackpy/wiki/CLI-docs>.

## License
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/akamhy/waybackpy/blob/master/LICENSE)

Released under the MIT License. See
[license](https://github.com/akamhy/waybackpy/blob/master/LICENSE) for details.


-----------------------------------------------------------------------------------------------------------------------------------------------
