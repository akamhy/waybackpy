# ┏┓┏┓┏┓━━━━━━━━━━┏━━┓━━━━━━━━━━┏┓━━┏━━━┓━━━━━
# ┃┃┃┃┃┃━━━━━━━━━━┃┏┓┃━━━━━━━━━━┃┃━━┃┏━┓┃━━━━━
# ┃┃┃┃┃┃┏━━┓━┏┓━┏┓┃┗┛┗┓┏━━┓━┏━━┓┃┃┏┓┃┗━┛┃┏┓━┏┓
# ┃┗┛┗┛┃┗━┓┃━┃┃━┃┃┃┏━┓┃┗━┓┃━┃┏━┛┃┗┛┛┃┏━━┛┃┃━┃┃
# ┗┓┏┓┏┛┃┗┛┗┓┃┗━┛┃┃┗━┛┃┃┗┛┗┓┃┗━┓┃┏┓┓┃┃━━━┃┗━┛┃
# ━┗┛┗┛━┗━━━┛┗━┓┏┛┗━━━┛┗━━━┛┗━━┛┗┛┗┛┗┛━━━┗━┓┏┛
# ━━━━━━━━━━━┏━┛┃━━━━━━━━━━━━━━━━━━━━━━━━┏━┛┃━
# ━━━━━━━━━━━┗━━┛━━━━━━━━━━━━━━━━━━━━━━━━┗━━┛━

"""
Waybackpy is a Python package & command-line program that interfaces with the Internet Archive's Wayback Machine API.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Archive webpage and retrieve archived URLs easily.

Usage:
    >>> import waybackpy

    >>> url = "https://en.wikipedia.org/wiki/Multivariable_calculus"
    >>> user_agent = "Mozilla/5.0 (Windows NT 5.1; rv:40.0) Gecko/20100101 Firefox/40.0"

    >>> wayback = waybackpy.Url(url, user_agent)

    >>> archive = wayback.save()
    >>> str(archive)
    'https://web.archive.org/web/20210104173410/https://en.wikipedia.org/wiki/Multivariable_calculus'

    >>> archive.timestamp
    datetime.datetime(2021, 1, 4, 17, 35, 12, 691741)

    >>> oldest_archive = wayback.oldest()
    >>> str(oldest_archive)
    'https://web.archive.org/web/20050422130129/http://en.wikipedia.org:80/wiki/Multivariable_calculus'

    >>> archive_close_to_2010_feb = wayback.near(year=2010, month=2)
    >>> str(archive_close_to_2010_feb)
    'https://web.archive.org/web/20100215001541/http://en.wikipedia.org:80/wiki/Multivariable_calculus'

    >>> str(wayback.newest())
    'https://web.archive.org/web/20210104173410/https://en.wikipedia.org/wiki/Multivariable_calculus'

Full documentation @ <https://github.com/akamhy/waybackpy/wiki>.
:copyright: (c) 2020-2021 AKash Mahanty Et al.
:license: MIT
"""

from .wrapper import Url, Cdx
from .__version__ import (
    __title__,
    __description__,
    __url__,
    __version__,
    __author__,
    __author_email__,
    __license__,
    __copyright__,
)
