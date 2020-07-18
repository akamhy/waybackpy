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
Waybackpy is a Python library that interfaces with the Internet Archive's Wayback Machine API.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Archive pages and retrieve archived pages easily.

Usage:
   >>> import waybackpy
   >>> target_url = waybackpy.Url('https://www.python.org', 'Your-apps-cool-user-agent')
   >>> new_archive = target_url.save()
   >>> print(new_archive)
   https://web.archive.org/web/20200502170312/https://www.python.org/

Full documentation @ <https://akamhy.github.io/waybackpy/>.
:copyright: (c) 2020 by akamhy.
:license: MIT
"""

from .wrapper import Url
from .__version__ import __title__, __description__, __url__, __version__
from .__version__ import __author__, __author_email__, __license__, __copyright__
