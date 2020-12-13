--------------

Python package & CLI tool that interfaces with the Wayback Machine API.
-----------------------------------------------------------------------

|pypi| |License: MIT| |Build Status| |codecov| |contributions welcome|
|Codacy Badge| |Downloads| |Release| |Maintainability|
|made-with-python| |Maintenance| |GitHub last commit| |PyPI - Python
Version|

Table of contents
=================

.. raw:: html

   <!--ts-->

-  `Installation <#installation>`__

-  `Usage <#usage>`__
-  `As a Python package <#as-a-python-package>`__

   -  `Saving a webpage <#capturing-aka-saving-an-url-using-save>`__
   -  `Retrieving
      archive <#retrieving-the-archive-for-an-url-using-archive_url>`__
   -  `Retrieving the oldest
      archive <#retrieving-the-oldest-archive-for-an-url-using-oldest>`__
   -  `Retrieving the recent most/newest
      archive <#retrieving-the-newest-archive-for-an-url-using-newest>`__
   -  `Retrieving the JSON response of availability
      API <#retrieving-the-json-reponse-for-the-avaliblity-api-request>`__
   -  `Retrieving archive close to a specified year, month, day, hour,
      and
      minute <#retrieving-archive-close-to-a-specified-year-month-day-hour-and-minute-using-near>`__
   -  `Get the content of
      webpage <#get-the-content-of-webpage-using-get>`__
   -  `Count total archives for an
      URL <#count-total-archives-for-an-url-using-total_archives>`__
   -  `List of URLs that Wayback Machine knows and has archived for a
      domain
      name <#list-of-urls-that-wayback-machine-knows-and-has-archived-for-a-domain-name>`__

-  `With the Command-line
   interface <#with-the-command-line-interface>`__

   -  `Saving webpage <#save>`__
   -  `Archive URL <#get-archive-url>`__
   -  `Oldest archive URL <#oldest-archive>`__
   -  `Newest archive URL <#newest-archive>`__
   -  `JSON response of API <#get-json-data-of-avaialblity-api>`__
   -  `Total archives <#total-number-of-archives>`__
   -  `Archive near specified time <#archive-near-time>`__
   -  `Get the source code <#get-the-source-code>`__
   -  `Fetch all the URLs that the Wayback Machine knows for a
      domain <#fetch-all-the-urls-that-the-wayback-machine-knows-for-a-domain>`__

-  `Tests <#tests>`__

-  `Dependency <#dependency>`__

-  `Packaging <#packaging>`__

-  `License <#license>`__

.. raw:: html

   <!--te-->

Installation
------------

Using `pip <https://en.wikipedia.org/wiki/Pip_(package_manager)>`__:

.. code:: bash

    pip install waybackpy

or direct from this repository using git.

.. code:: bash

    pip install git+https://github.com/akamhy/waybackpy.git

Usage
-----

As a Python package
~~~~~~~~~~~~~~~~~~~

Capturing aka Saving an url using save()
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    import waybackpy

    url = "https://en.wikipedia.org/wiki/Multivariable_calculus"
    user_agent = "Mozilla/5.0 (Windows NT 5.1; rv:40.0) Gecko/20100101 Firefox/40.0"

    waybackpy_url_obj = waybackpy.Url(url, user_agent)
    archive = waybackpy_url_obj.save()
    print(archive)

.. code:: bash

    https://web.archive.org/web/20201016171808/https://en.wikipedia.org/wiki/Multivariable_calculus

Try this out in your browser @
https://repl.it/@akamhy/WaybackPySaveExample\ 

Retrieving the archive for an URL using archive\_url
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    import waybackpy

    url = "https://www.google.com/"
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:40.0) Gecko/20100101 Firefox/40.0"

    waybackpy_url_obj = waybackpy.Url(url, user_agent)
    archive_url = waybackpy_url_obj.archive_url
    print(archive_url)

.. code:: bash

    https://web.archive.org/web/20201016153320/https://www.google.com/

Try this out in your browser @
https://repl.it/@akamhy/WaybackPyArchiveUrl\ 

Retrieving the oldest archive for an URL using oldest()
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    import waybackpy

    url = "https://www.google.com/"
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:40.0) Gecko/20100101 Firefox/40.0"

    waybackpy_url_obj = waybackpy.Url(url, user_agent)
    oldest_archive_url = waybackpy_url_obj.oldest()
    print(oldest_archive_url)

.. code:: bash

    http://web.archive.org/web/19981111184551/http://google.com:80/

Try this out in your browser @
https://repl.it/@akamhy/WaybackPyOldestExample\ 

Retrieving the newest archive for an URL using newest()
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    import waybackpy

    url = "https://www.facebook.com/"
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:39.0) Gecko/20100101 Firefox/39.0"

    waybackpy_url_obj = waybackpy.Url(url, user_agent)
    newest_archive_url = waybackpy_url_obj.newest()
    print(newest_archive_url)

.. code:: bash

    https://web.archive.org/web/20201016150543/https://www.facebook.com/

Try this out in your browser @
https://repl.it/@akamhy/WaybackPyNewestExample\ 

Retrieving the JSON reponse for the avaliblity API request
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    import waybackpy

    url = "https://www.facebook.com/"
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:39.0) Gecko/20100101 Firefox/39.0"

    waybackpy_url_obj = waybackpy.Url(url, user_agent)
    json_dict = waybackpy_url_obj.JSON
    print(json_dict)

.. code:: javascript

    {'url': 'https://www.facebook.com/', 'archived_snapshots': {'closest': {'available': True, 'url': 'http://web.archive.org/web/20201016150543/https://www.facebook.com/', 'timestamp': '20201016150543', 'status': '200'}}}

Try this out in your browser @ https://repl.it/@akamhy/WaybackPyJSON\ 

Retrieving archive close to a specified year, month, day, hour, and minute using near()
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    from waybackpy import Url

    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:38.0) Gecko/20100101 Firefox/38.0"
    url = "https://github.com/"

    waybackpy_url_obj = Url(url, user_agent)

    # Do not pad (don't use zeros in the month, year, day, minute, and hour arguments). e.g. For January, set month = 1 and not month = 01.

.. code:: python

    github_archive_near_2010 = waybackpy_url_obj.near(year=2010)
    print(github_archive_near_2010)

.. code:: bash

    https://web.archive.org/web/20101018053604/http://github.com:80/

.. code:: python

    github_archive_near_2011_may = waybackpy_url_obj.near(year=2011, month=5)
    print(github_archive_near_2011_may)

.. code:: bash

    https://web.archive.org/web/20110518233639/https://github.com/

.. code:: python

    github_archive_near_2015_january_26 = waybackpy_url_obj.near(year=2015, month=1, day=26)
    print(github_archive_near_2015_january_26)

.. code:: bash

    https://web.archive.org/web/20150125102636/https://github.com/

.. code:: python

    github_archive_near_2018_4_july_9_2_am = waybackpy_url_obj.near(year=2018, month=7, day=4, hour=9, minute=2)
    print(github_archive_near_2018_4_july_9_2_am)

.. code:: bash

    https://web.archive.org/web/20180704090245/https://github.com/

The package doesn't support second argument yet. You are encourged to
create a PR ;)

Try this out in your browser @
https://repl.it/@akamhy/WaybackPyNearExample\ 

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
    google_newest_archive_source = waybackpy_url_object.get(waybackpy_url_object.save())
    print(google_newest_archive_source)


    # waybackpy_url_object.oldest() type is str, it's oldest archive of google.com
    google_oldest_archive_source = waybackpy_url_object.get(waybackpy_url_object.oldest())
    print(google_oldest_archive_source)

Try this out in your browser @
https://repl.it/@akamhy/WaybackPyGetExample#main.py\ 

Count total archives for an URL using total\_archives()
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    import waybackpy

    URL = "https://en.wikipedia.org/wiki/Python (programming language)"
    UA = "Mozilla/5.0 (iPad; CPU OS 8_1_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B435 Safari/600.1.4"

    waybackpy_url_object = waybackpy.Url(url=URL, user_agent=UA)

    archive_count = waybackpy_url_object.total_archives()

    print(archive_count) # total_archives() returns an int

.. code:: bash

    2516

Try this out in your browser @
https://repl.it/@akamhy/WaybackPyTotalArchivesExample\ 

List of URLs that Wayback Machine knows and has archived for a domain name
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1) If alive=True is set, waybackpy will check all URLs to identify the
   alive URLs. Don't use with popular websites like google or it would
   take too long.
2) To include URLs from subdomain set sundomain=True

.. code:: python

    import waybackpy

    URL = "akamhy.github.io"
    UA = "Mozilla/5.0 (iPad; CPU OS 8_1_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B435 Safari/600.1.4"

    waybackpy_url_object = waybackpy.Url(url=URL, user_agent=UA)
    known_urls = waybackpy_url_object.known_urls(alive=True, subdomain=False) # alive and subdomain are optional.
    print(known_urls) # known_urls() returns list of URLs

.. code:: bash

    ['http://akamhy.github.io',
    'https://akamhy.github.io/waybackpy/',
    'https://akamhy.github.io/waybackpy/assets/css/style.css?v=a418a4e4641a1dbaad8f3bfbf293fad21a75ff11',
    'https://akamhy.github.io/waybackpy/assets/css/style.css?v=f881705d00bf47b5bf0c58808efe29eecba2226c']

Try this out in your browser @
https://repl.it/@akamhy/WaybackPyKnownURLsToWayBackMachineExample#main.py\ 

With the Command-line interface
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Save
^^^^

.. code:: bash

    $ waybackpy --url "https://en.wikipedia.org/wiki/Social_media" --user_agent "my-unique-user-agent" --save
    https://web.archive.org/web/20200719062108/https://en.wikipedia.org/wiki/Social_media

Try this out in your browser @
https://repl.it/@akamhy/WaybackPyBashSave\ 

Get archive URL
^^^^^^^^^^^^^^^

.. code:: bash

    $ waybackpy --url "https://en.wikipedia.org/wiki/SpaceX" --user_agent "my-unique-user-agent" --archive_url
    https://web.archive.org/web/20201007132458/https://en.wikipedia.org/wiki/SpaceX

Try this out in your browser @
https://repl.it/@akamhy/WaybackPyBashArchiveUrl\ 

Oldest archive
^^^^^^^^^^^^^^

.. code:: bash

    $ waybackpy --url "https://en.wikipedia.org/wiki/SpaceX" --user_agent "my-unique-user-agent" --oldest
    https://web.archive.org/web/20040803000845/http://en.wikipedia.org:80/wiki/SpaceX

Try this out in your browser @
https://repl.it/@akamhy/WaybackPyBashOldest\ 

Newest archive
^^^^^^^^^^^^^^

.. code:: bash

    $ waybackpy --url "https://en.wikipedia.org/wiki/YouTube" --user_agent "my-unique-user-agent" --newest
    https://web.archive.org/web/20200606044708/https://en.wikipedia.org/wiki/YouTube

Try this out in your browser @
https://repl.it/@akamhy/WaybackPyBashNewest\ 

Get JSON data of avaialblity API
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: bash

    waybackpy --url "https://en.wikipedia.org/wiki/SpaceX" --user_agent "my-unique-user-agent" --json

.. code:: javascript

    {'archived_snapshots': {'closest': {'timestamp': '20201007132458', 'status': '200', 'available': True, 'url': 'http://web.archive.org/web/20201007132458/https://en.wikipedia.org/wiki/SpaceX'}}, 'url': 'https://en.wikipedia.org/wiki/SpaceX'}

Try this out in your browser @
https://repl.it/@akamhy/WaybackPyBashJSON\ 

Total number of archives
^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: bash

    $ waybackpy --url "https://en.wikipedia.org/wiki/Linux_kernel" --user_agent "my-unique-user-agent" --total
    853

Try this out in your browser @
https://repl.it/@akamhy/WaybackPyBashTotal\ 

Archive near time
^^^^^^^^^^^^^^^^^

.. code:: bash

    $ waybackpy --url facebook.com --user_agent "my-unique-user-agent" --near --year 2012 --month 5 --day 12
    https://web.archive.org/web/20120512142515/https://www.facebook.com/

Try this out in your browser @
https://repl.it/@akamhy/WaybackPyBashNear\ 

Get the source code
^^^^^^^^^^^^^^^^^^^

.. code:: bash

    waybackpy --url google.com --user_agent "my-unique-user-agent" --get url # Prints the source code of the url
    waybackpy --url google.com --user_agent "my-unique-user-agent" --get oldest # Prints the source code of the oldest archive
    waybackpy --url google.com --user_agent "my-unique-user-agent" --get newest # Prints the source code of the newest archive
    waybackpy --url google.com --user_agent "my-unique-user-agent" --get save # Save a new archive on wayback machine then print the source code of this archive.

Try this out in your browser @
https://repl.it/@akamhy/WaybackPyBashGet\ 

Fetch all the URLs that the Wayback Machine knows for a domain
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1) You can add the '--alive' flag to only fetch alive links.
2) You can add the '--subdomain' flag to add subdomains.
3) '--alive' and '--subdomain' flags can be used simultaneously.
4) All links will be saved in a file, and the file will be created in
   the current working directory.

.. code:: bash

    pip install waybackpy

    # Ignore the above installation line.

    waybackpy --url akamhy.github.io --user_agent "my-user-agent" --known_urls
    # Prints all known URLs under akamhy.github.io


    waybackpy --url akamhy.github.io --user_agent "my-user-agent" --known_urls --alive
    # Prints all known URLs under akamhy.github.io which are still working and not dead links.


    waybackpy --url akamhy.github.io --user_agent "my-user-agent" --known_urls --subdomain
    # Prints all known URLs under akamhy.github.io inclusing subdomain


    waybackpy --url akamhy.github.io --user_agent "my-user-agent" --known_urls --subdomain --alive
    # Prints all known URLs under akamhy.github.io including subdomain which are not dead links and still alive.

Try this out in your browser @
https://repl.it/@akamhy/WaybackpyKnownUrlsFromWaybackMachine#main.sh\ 

Tests
-----

To run tests locally:

1) Install or update the testing/coverage tools

.. code:: bash

    pip install codecov pytest pytest-cov -U

2) Inside the repository run the following commands

.. code:: bash

    pytest --cov=waybackpy tests/

3) To report coverage run

.. code:: bash

    bash <(curl -s https://codecov.io/bash) -t SECRET_CODECOV_TOKEN

You can find the tests
`here <https://github.com/akamhy/waybackpy/tree/master/tests>`__.

Packaging
---------

1. Increment version.

2. Build package ``python setup.py sdist bdist_wheel``.

3. Sign & upload the package ``twine upload -s dist/*``.

License
-------

Released under the MIT License. See
`license <https://github.com/akamhy/waybackpy/blob/master/LICENSE>`__
for details.

.. |pypi| image:: https://img.shields.io/pypi/v/waybackpy.svg
   :target: https://pypi.org/project/waybackpy/
.. |License: MIT| image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://github.com/akamhy/waybackpy/blob/master/LICENSE
.. |Build Status| image:: https://github.com/akamhy/waybackpy/workflows/CI/badge.svg
   :target: https://github.com/akamhy/waybackpy/actions
.. |codecov| image:: https://codecov.io/gh/akamhy/waybackpy/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/akamhy/waybackpy
.. |contributions welcome| image:: https://img.shields.io/static/v1.svg?label=Contributions&message=Welcome&color=0059b3&style=flat-square
   :target: https://github.com/akamhy/waybackpy/blob/master/CONTRIBUTING.md
.. |Codacy Badge| image:: https://api.codacy.com/project/badge/Grade/255459cede9341e39436ec8866d3fb65
   :target: https://www.codacy.com/manual/akamhy/waybackpy?utm_source=github.com&utm_medium=referral&utm_content=akamhy/waybackpy&utm_campaign=Badge_Grade
.. |Downloads| image:: https://pepy.tech/badge/waybackpy/month
   :target: https://pepy.tech/project/waybackpy
.. |Release| image:: https://img.shields.io/github/v/release/akamhy/waybackpy.svg
   :target: https://github.com/akamhy/waybackpy/releases
.. |Maintainability| image:: https://api.codeclimate.com/v1/badges/942f13d8177a56c1c906/maintainability
   :target: https://codeclimate.com/github/akamhy/waybackpy/maintainability
.. |made-with-python| image:: https://img.shields.io/badge/Made%20with-Python-1f425f.svg
   :target: https://www.python.org/
.. |Maintenance| image:: https://img.shields.io/badge/Maintained%3F-yes-green.svg
   :target: https://github.com/akamhy/waybackpy/graphs/commit-activity
.. |GitHub last commit| image:: https://img.shields.io/github/last-commit/akamhy/waybackpy?color=blue&style=flat-square
   :target: https://github.com/akamhy/waybackpy/commits/master
.. |PyPI - Python Version| image:: https://img.shields.io/pypi/pyversions/waybackpy?style=flat-square
