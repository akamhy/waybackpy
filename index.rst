waybackpy
=========

|Build Status| |Downloads| |Release| |Codacy Badge| |License: MIT|
|Maintainability| |CodeFactor| |made-with-python| |pypi| |PyPI - Python
Version| |Maintenance| |codecov| |image12| |contributions welcome|

|Internet Archive| |Wayback Machine|

Waybackpy is a Python library that interfaces with the `Internet
Archive <https://en.wikipedia.org/wiki/Internet_Archive>`__'s `Wayback
Machine <https://en.wikipedia.org/wiki/Wayback_Machine>`__ API. Archive
pages and retrieve archived pages easily.

Table of contents
=================

.. raw:: html

   <!--ts-->

-  `Installation <#installation>`__

-  `Usage <#usage>`__
-  `Saving an url using
   save() <#capturing-aka-saving-an-url-using-save>`__
-  `Receiving the oldest archive for an URL Using
   oldest() <#receiving-the-oldest-archive-for-an-url-using-oldest>`__
-  `Receiving the recent most/newest archive for an URL using
   newest() <#receiving-the-newest-archive-for-an-url-using-newest>`__
-  `Receiving archive close to a specified year, month, day, hour, and
   minute using
   near() <#receiving-archive-close-to-a-specified-year-month-day-hour-and-minute-using-near>`__
-  `Get the content of webpage using
   get() <#get-the-content-of-webpage-using-get>`__
-  `Count total archives for an URL using
   total\_archives() <#count-total-archives-for-an-url-using-total_archives>`__

-  `Tests <#tests>`__

-  `Dependency <#dependency>`__

-  `License <#license>`__

.. raw:: html

   <!--te-->

Installation
------------

Using `pip <https://en.wikipedia.org/wiki/Pip_(package_manager)>`__:

.. code:: bash

    pip install waybackpy

Usage
-----

Capturing aka Saving an url using save()
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    import waybackpy

    new_archive_url = waybackpy.Url(

        url = "https://en.wikipedia.org/wiki/Multivariable_calculus",
        user_agent = "Mozilla/5.0 (Windows NT 5.1; rv:40.0) Gecko/20100101 Firefox/40.0"
        
    ).save()

    print(new_archive_url)

.. code:: bash

    https://web.archive.org/web/20200504141153/https://github.com/akamhy/waybackpy

Try this out in your browser @
https://repl.it/repls/CompassionateRemoteOrigin#main.py\ 

Receiving the oldest archive for an URL using oldest()
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    import waybackpy

    oldest_archive_url = waybackpy.Url(

        "https://www.google.com/",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:40.0) Gecko/20100101 Firefox/40.0"
        
    ).oldest()

    print(oldest_archive_url)

.. code:: bash

    http://web.archive.org/web/19981111184551/http://google.com:80/

Try this out in your browser @
https://repl.it/repls/MixedSuperDimensions#main.py\ 

Receiving the newest archive for an URL using newest()
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    import waybackpy

    newest_archive_url = waybackpy.Url(

        "https://www.facebook.com/",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:39.0) Gecko/20100101 Firefox/39.0"
        
    ).newest()

    print(newest_archive_url)

.. code:: bash

    https://web.archive.org/web/20200714013225/https://www.facebook.com/

Try this out in your browser @
https://repl.it/repls/OblongMiniInteger#main.py\ 

Receiving archive close to a specified year, month, day, hour, and minute using near()
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    from waybackpy import Url

    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:38.0) Gecko/20100101 Firefox/38.0"
    github_url = "https://github.com/"


    github_wayback_obj = Url(github_url, user_agent)

    # Do not pad (don't use zeros in the month, year, day, minute, and hour arguments). e.g. For January, set month = 1 and not month = 01.

.. code:: python

    github_archive_near_2010 = github_wayback_obj.near(year=2010)
    print(github_archive_near_2010)

.. code:: bash

    https://web.archive.org/web/20100719134402/http://github.com/

.. code:: python

    github_archive_near_2011_may = github_wayback_obj.near(year=2011, month=5)
    print(github_archive_near_2011_may)

.. code:: bash

    https://web.archive.org/web/20110519185447/https://github.com/

.. code:: python

    github_archive_near_2015_january_26 = github_wayback_obj.near(
        year=2015, month=1, day=26
    )
    print(github_archive_near_2015_january_26)

.. code:: bash

    https://web.archive.org/web/20150127031159/https://github.com

.. code:: python

    github_archive_near_2018_4_july_9_2_am = github_wayback_obj.near(
        year=2018, month=7, day=4, hour = 9, minute = 2
    )
    print(github_archive_near_2018_4_july_9_2_am)

.. code:: bash

    https://web.archive.org/web/20180704090245/https://github.com/

The library doesn't supports seconds yet. You are encourged to create a
PR ;)

Try this out in your browser @
https://repl.it/repls/SparseDeadlySearchservice#main.py\ 

Get the content of webpage using get()
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    import waybackpy

    google_url = "https://www.google.com/"

    User_Agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36"

    waybackpy_url_object = waybackpy.Url(google_url, User_Agent)


    # If no argument is passed in get(), it gets the source of the Url used to create the object.
    current_google_url_source = waybackpy_url_object.get()
    print(current_google_url_source)


    # The following chunk of code will force a new archive of google.com and get the source of the archived page.
    # waybackpy_url_object.save() type is string.
    google_newest_archive_source = waybackpy_url_object.get(
        waybackpy_url_object.save()
    )
    print(google_newest_archive_source)


    # waybackpy_url_object.oldest() type is str, it's oldest archive of google.com
    google_oldest_archive_source = waybackpy_url_object.get(
        waybackpy_url_object.oldest()
    )
    print(google_oldest_archive_source)

Try this out in your browser @
https://repl.it/repls/PinkHoneydewNonagon#main.py\ 

Count total archives for an URL using total\_archives()
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    import waybackpy

    URL = "https://en.wikipedia.org/wiki/Python (programming language)"

    UA = "Mozilla/5.0 (iPad; CPU OS 8_1_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B435 Safari/600.1.4"

    archive_count = waybackpy.Url(
        url=URL,
        user_agent=UA
    ).total_archives()

    print(archive_count) # total_archives() returns an int

.. code:: bash

    2440

Try this out in your browser @
https://repl.it/repls/DigitalUnconsciousNumbers#main.py\ 

Tests
-----

-  `Here <https://github.com/akamhy/waybackpy/tree/master/tests>`__

Dependency
----------

-  None, just python standard libraries (re, json, urllib and datetime).
   Both python 2 and 3 are supported :)

License
-------

`MIT
License <https://github.com/akamhy/waybackpy/blob/master/LICENSE>`__

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
.. |image12| image:: https://img.shields.io/github/repo-size/akamhy/waybackpy.svg?label=Repo%20size&style=flat-square
.. |contributions welcome| image:: https://img.shields.io/static/v1.svg?label=Contributions&message=Welcome&color=0059b3&style=flat-square
.. |Internet Archive| image:: https://upload.wikimedia.org/wikipedia/commons/thumb/8/84/Internet_Archive_logo_and_wordmark.svg/84px-Internet_Archive_logo_and_wordmark.svg.png
.. |Wayback Machine| image:: https://upload.wikimedia.org/wikipedia/commons/thumb/0/01/Wayback_Machine_logo_2010.svg/284px-Wayback_Machine_logo_2010.svg.png
