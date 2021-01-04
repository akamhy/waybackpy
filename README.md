<div align="center">
  <img src="https://raw.githubusercontent.com/akamhy/waybackpy/master/assets/waybackpy_logo.svg"><br>
</div>

---------------------------------------------------------------------------------------------------
<center> <h1>Python package & CLI tool that interfaces with the Wayback Machine API</h1> </center>

[![pypi](https://img.shields.io/pypi/v/waybackpy.svg)](https://pypi.org/project/waybackpy/)
[![Build Status](https://github.com/akamhy/waybackpy/workflows/CI/badge.svg)](https://github.com/akamhy/waybackpy/actions?query=workflow%3ACI)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/255459cede9341e39436ec8866d3fb65)](https://www.codacy.com/manual/akamhy/waybackpy?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=akamhy/waybackpy&amp;utm_campaign=Badge_Grade)
[![codecov](https://codecov.io/gh/akamhy/waybackpy/branch/master/graph/badge.svg)](https://codecov.io/gh/akamhy/waybackpy)
[![Maintainability](https://api.codeclimate.com/v1/badges/942f13d8177a56c1c906/maintainability)](https://codeclimate.com/github/akamhy/waybackpy/maintainability)
[![contributions welcome](https://img.shields.io/static/v1.svg?label=Contributions&message=Welcome&color=0059b3&style=flat-square)](https://github.com/akamhy/waybackpy/blob/master/CONTRIBUTING.md)
[![Downloads](https://pepy.tech/badge/waybackpy/month)](https://pepy.tech/project/waybackpy)
[![GitHub last commit](https://img.shields.io/github/last-commit/akamhy/waybackpy?color=blue&style=flat-square)](https://github.com/akamhy/waybackpy/commits/master)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/waybackpy?style=flat-square)



## Table of contents

<!--ts-->

* [Installation](#installation)

* [Documentation and Wiki](https://github.com/akamhy/waybackpy/wiki)

* [Tests](#tests)

* [Packaging](#packaging)

* [License](#license)

<!--te-->

### Installation

Using [pip](https://en.wikipedia.org/wiki/Pip_(package_manager)):

```bash
pip install waybackpy
```

or direct from this repository using git.

```bash
pip install git+https://github.com/akamhy/waybackpy.git
```


### Tests

To run tests locally:

1) Install or update the testing/coverage tools 

```bash
pip install codecov pytest pytest-cov -U
```

2) Inside the repository run the following commands

```bash
pytest --cov=waybackpy tests/
```

3) To report coverage run

```bash
bash <(curl -s https://codecov.io/bash) -t SECRET_CODECOV_TOKEN
```

You can find the tests [here](https://github.com/akamhy/waybackpy/tree/master/tests).


### Packaging

1. Increment version.

2. Build package ``python setup.py sdist bdist_wheel``.

3. Sign & upload the package ``twine upload -s dist/*``.
