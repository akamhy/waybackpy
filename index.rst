waybackpy
=========

|Build Status| |Downloads| |Release| |Codacy Badge| |License: MIT|
|Maintainability| |CodeFactor| |made-with-python| |pypi| |PyPI - Python
Version| |Maintenance| |codecov| |image1| |contributions welcome|

.. |Build Status| image:: https://img.shields.io/travis/akamhy/waybackpy.svg?label=Travis%20CI&logo=travis&style=flat-square
   :target: https://travis-ci.org/akamhy/waybackpy
.. |Downloads| image:: https://img.shields.io/pypi/dm/waybackpy.svg
   :target: https://pypistats.org/packages/waybackpy
.. |Release| image:: https://img.shields.io/github/v/release/akamhy/waybackpy.svg
   :target: https://github.com/akamhy/waybackpy/releases
.. |Codacy Badge| image:: https://api.codacy.com/project/badge/Grade/255459cede9341e39436ec8866d3fb65
   :target: https://www.codacy.com/manual/akamhy/waybackpy?utm_source=github.com&utm_medium=referral&utm_content=akamhy/waybackpy&utm_campaign=Badge_Grade
.. |License: MIT| image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://github.com/akamhy/waybackpy/blob/master/LICENSE
.. |Maintainability| image:: https://api.codeclimate.com/v1/badges/942f13d8177a56c1c906/maintainability
   :target: https://codeclimate.com/github/akamhy/waybackpy/maintainability
.. |CodeFactor| image:: https://www.codefactor.io/repository/github/akamhy/waybackpy/badge
   :target: https://www.codefactor.io/repository/github/akamhy/waybackpy
.. |made-with-python| image:: https://img.shields.io/badge/Made%20with-Python-1f425f.svg
   :target: https://www.python.org/
.. |pypi| image:: https://img.shields.io/pypi/v/waybackpy.svg
.. |PyPI - Python Version| image:: https://img.shields.io/pypi/pyversions/waybackpy?style=flat-square
.. |Maintenance| image:: https://img.shields.io/badge/Maintained%3F-yes-green.svg
   :target: https://github.com/akamhy/waybackpy/graphs/commit-activity
.. |codecov| image:: https://codecov.io/gh/akamhy/waybackpy/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/akamhy/waybackpy
.. |image1| image:: https://img.shields.io/github/repo-size/akamhy/waybackpy.svg?label=Repo%20size&style=flat-square
.. |contributions welcome| image:: https://img.shields.io/static/v1.svg?label=Contributions&message=Welcome&color=0059b3&style=flat-square


|Internet Archive| |Wayback Machine|

Waybackpy is a Python library that interfaces with the `Internet
Archive`_\ ’s `Wayback Machine`_ API. Archive pages and retrieve
archived pages easily.

.. _Internet Archive: https://en.wikipedia.org/wiki/Internet_Archive
.. _Wayback Machine: https://en.wikipedia.org/wiki/Wayback_Machine

.. |Internet Archive| image:: https://upload.wikimedia.org/wikipedia/commons/thumb/8/84/Internet_Archive_logo_and_wordmark.svg/84px-Internet_Archive_logo_and_wordmark.svg.png
.. |Wayback Machine| image:: https://upload.wikimedia.org/wikipedia/commons/thumb/0/01/Wayback_Machine_logo_2010.svg/284px-Wayback_Machine_logo_2010.svg.png

Table of contents
=================

.. raw:: html

   <!--ts-->

-  `Installation`_

-  `Usage`_

   -  `Saving an url using save()`_
   -  `Receiving the oldest archive for an URL Using oldest()`_
   -  `Receiving the recent most/newest archive for an URL using
      newest()`_
   -  `Receiving archive close to a specified year, month, day, hour,
      and minute using near()`_
   -  `Get the content of webpage using get()`_
   -  `Count total archives for an URL using total_archives()`_

-  `Tests`_

-  `Dependency`_

-  `License`_

.. raw:: html

   <!--te-->

.. _Installation: #installation
.. _Usage: #usage
.. _Saving an url using save(): #capturing-aka-saving-an-url-using-save
.. _Receiving the oldest archive for an URL Using oldest(): #receiving-the-oldest-archive-for-an-url-using-oldest
.. _Receiving the recent most/newest archive for an URL using newest(): #receiving-the-newest-archive-for-an-url-using-newest
.. _Receiving archive close to a specified year, month, day, hour, and minute using near(): #receiving-archive-close-to-a-specified-year-month-day-hour-and-minute-using-near
.. _Get the content of webpage using get(): #get-the-content-of-webpage-using-get
.. _Count total archives for an URL using total_archives(): #count-total-archives-for-an-url-using-total_archives
.. _Tests: #tests
.. _Dependency: #dependency
.. _License: #license
