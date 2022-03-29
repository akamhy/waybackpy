# Welcome to waybackpy contributing guide


## Getting started

Read our [Code of Conduct](./CODE_OF_CONDUCT.md).

## Creating an issue

It's a good idea to open an issue and discuss suspected bugs and new feature ideas with the maintainers. Somebody might be working on your bug/idea and it would be best to discuss it to avoid wasting your time. It is a recommendation. You may avoid creating an issue and directly open pull requests.

## Fork this repository

Fork this repository. See '[Fork a repo](https://docs.github.com/en/get-started/quickstart/fork-a-repo)' for help forking this repository on GitHub.

## Make changes to the forked copy

Make the required changes to your forked copy of waybackpy, please don't forget to add or update comments and docstrings.

## Add tests for your changes

You have made the required changes to the codebase, now go ahead and add tests for newly written methods/functions and update the tests of code that you changed.

## Testing and Linting

You must run the tests and linter on your changes before opening a pull request.

### pytest

Runs all test from tests directory. pytest is a mature full-featured Python testing tool.
```bash
pytest
```

### mypy

Mypy is a static type checker for Python. Type checkers help ensure that you're using variables and functions in your code correctly.
```bash
mypy -p waybackpy -p tests
```

### black

After testing with pytest and type checking with mypy run black on the code base. The codestyle used by the project is 'black'.

```bash
black .
```

## Create a pull request

Read [Creating a pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request).

Try to make sure that all automated tests are passing, and if some of them do not pass then don't worry. Tests are meant to catch bugs and a failed test is better than introducing bugs to the master branch.
