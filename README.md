<div align="center">
 <img src="https://raw.githubusercontent.com/akamhy/waybackpy/master/assets/waybackpy_logo.svg"><br>

<h2>Python package & CLI tool that interfaces with the Wayback Machine API</h2>

</div>


[![pypi](https://img.shields.io/pypi/v/waybackpy.svg)](https://pypi.org/project/waybackpy/)
[![Build Status](https://github.com/akamhy/waybackpy/workflows/CI/badge.svg)](https://github.com/akamhy/waybackpy/actions?query=workflow%3ACI)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/255459cede9341e39436ec8866d3fb65)](https://www.codacy.com/manual/akamhy/waybackpy?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=akamhy/waybackpy&amp;utm_campaign=Badge_Grade)
[![codecov](https://codecov.io/gh/akamhy/waybackpy/branch/master/graph/badge.svg)](https://codecov.io/gh/akamhy/waybackpy)
[![Maintainability](https://api.codeclimate.com/v1/badges/942f13d8177a56c1c906/maintainability)](https://codeclimate.com/github/akamhy/waybackpy/maintainability)
[![contributions welcome](https://img.shields.io/static/v1.svg?label=Contributions&message=Welcome&color=0059b3&style=flat-square)](https://github.com/akamhy/waybackpy/blob/master/CONTRIBUTING.md)
[![Downloads](https://pepy.tech/badge/waybackpy/month)](https://pepy.tech/project/waybackpy)
[![GitHub last commit](https://img.shields.io/github/last-commit/akamhy/waybackpy?color=blue&style=flat-square)](https://github.com/akamhy/waybackpy/commits/master)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/waybackpy?style=flat-square)


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

### Usage

#### As a python package
```python
>>> import waybackpy

>>> url = "https://en.wikipedia.org/wiki/Multivariable_calculus"
>>> user_agent = "Mozilla/5.0 (Windows NT 5.1; rv:40.0) Gecko/20100101 Firefox/40.0"

>>> wayback = waybackpy.Url(url, user_agent)

>>> archive = wayback.save()
>> str(archive)
'https://web.archive.org/web/20210104173410/https://en.wikipedia.org/wiki/Multivariable_calculus'

>> archive.timestamp
datetime.datetime(2021, 1, 4, 17, 35, 12, 691741)

>> oldest_archive = wayback.oldest()
>> str(oldest_archive)
'https://web.archive.org/web/20050422130129/http://en.wikipedia.org:80/wiki/Multivariable_calculus'

>> archive_close_to_2010_feb = wayback.near(year=2010, month=2)
>> str(archive_close_to_2010_feb)
'https://web.archive.org/web/20100215001541/http://en.wikipedia.org:80/wiki/Multivariable_calculus'

>> str(wayback.newest())
'https://web.archive.org/web/20210104173410/https://en.wikipedia.org/wiki/Multivariable_calculus'
```


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

$ waybackpy --url akamhy.github.io --user_agent "my-user-agent" --known_urls
https://akamhy.github.io
https://akamhy.github.io/assets/js/scale.fix.js
https://akamhy.github.io/favicon.ico
https://akamhy.github.io/robots.txt
https://akamhy.github.io/waybackpy/

'akamhy.github.io-10-urls-m2a24y.txt' saved in current working directory
```

