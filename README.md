<div align="center">

<img src="https://raw.githubusercontent.com/akamhy/waybackpy/master/assets/waybackpy_logo.svg"><br>

<h2>Python package & CLI tool that interfaces with the Wayback Machine API</h2>

</div>

<p align="center">
<a href="https://pypi.org/project/waybackpy/"><img alt="pypi" src="https://img.shields.io/pypi/v/waybackpy.svg"></a>
<a href="https://github.com/akamhy/waybackpy/actions?query=workflow%3ACI"><img alt="Build Status" src="https://github.com/akamhy/waybackpy/workflows/CI/badge.svg"></a>
<a href="https://www.codacy.com/manual/akamhy/waybackpy?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=akamhy/waybackpy&amp;utm_campaign=Badge_Grade"><img alt="Codacy Badge" src="https://api.codacy.com/project/badge/Grade/255459cede9341e39436ec8866d3fb65"></a>
<a href="https://codecov.io/gh/akamhy/waybackpy"><img alt="codecov" src="https://codecov.io/gh/akamhy/waybackpy/branch/master/graph/badge.svg"></a>
<a href="https://github.com/akamhy/waybackpy/blob/master/CONTRIBUTING.md"><img alt="Contributions Welcome" src="https://img.shields.io/static/v1.svg?label=Contributions&message=Welcome&color=0059b3&style=flat-square"></a>
<a href="https://pepy.tech/project/waybackpy?versions=2*&versions=1*&versions=3*"><img alt="Downloads" src="https://pepy.tech/badge/waybackpy/month"></a>
<a href="https://github.com/akamhy/waybackpy/commits/master"><img alt="GitHub lastest commit" src="https://img.shields.io/github/last-commit/akamhy/waybackpy?color=blue&style=flat-square"></a>
<a href="#"><img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/waybackpy?style=flat-square"></a>
</p>

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

### Supported Features

  - Archive webpage
  - Retrieve all archives of a webpage/domain
  - Retrieve archive close to a date or timestamp
  - Retrieve all archives which have a particular prefix
  - Get source code of the archive easily
  - CDX API support


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

$ waybackpy --total --url "https://en.wikipedia.org/wiki/Linux_kernel" --user_agent "my-unique-user-agent"
1904

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
