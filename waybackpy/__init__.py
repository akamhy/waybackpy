# -*- coding: utf-8 -*-

# ┏┓┏┓┏┓━━━━━━━━━━┏━━┓━━━━━━━━━━┏┓━━┏━━━┓━━━━━
# ┃┃┃┃┃┃━━━━━━━━━━┃┏┓┃━━━━━━━━━━┃┃━━┃┏━┓┃━━━━━
# ┃┃┃┃┃┃┏━━┓━┏┓━┏┓┃┗┛┗┓┏━━┓━┏━━┓┃┃┏┓┃┗━┛┃┏┓━┏┓
# ┃┗┛┗┛┃┗━┓┃━┃┃━┃┃┃┏━┓┃┗━┓┃━┃┏━┛┃┗┛┛┃┏━━┛┃┃━┃┃
# ┗┓┏┓┏┛┃┗┛┗┓┃┗━┛┃┃┗━┛┃┃┗┛┗┓┃┗━┓┃┏┓┓┃┃━━━┃┗━┛┃
# ━┗┛┗┛━┗━━━┛┗━┓┏┛┗━━━┛┗━━━┛┗━━┛┗┛┗┛┗┛━━━┗━┓┏┛
# ━━━━━━━━━━━┏━┛┃━━━━━━━━━━━━━━━━━━━━━━━━┏━┛┃━
# ━━━━━━━━━━━┗━━┛━━━━━━━━━━━━━━━━━━━━━━━━┗━━┛━

"""
A python wrapper for Internet Archive's Wayback Machine API.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Archive pages and retrieve archived pages easily.
Usage:
   >>> import waybackpy
   >>> new_archive = waybackpy.save('https://www.python.org')
   >>> print(new_archive)
   https://web.archive.org/web/20200502170312/https://www.python.org/

Full documentation @ <https://akamhy.github.io/waybackpy/>.
:copyright: (c) 2020 by akamhy.
:license: MIT
"""

from .wrapper import save, near, oldest, newest, get, clean_url, url_check, total_archives
from .__version__ import __title__, __description__, __url__, __version__
from .__version__ import __author__, __author_email__, __license__, __copyright__
