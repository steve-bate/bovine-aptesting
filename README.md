<!-- TODO Update bovine documentation -->
# bovine-aptesting

Experimental extension of the [activitypub-testsuite](https://github.com/steve-bate/activitypub-testsuite) for testing [bovine.pub](https://codeberg.org/helge/bovine/).

This repository contains bovine.pub-specific code and configuration. The test framework starts a Node.js subprocess at the beginning of a test session. Before each test, a custom test reset API is called to reset the bovine.pub database.

## Install

### Requirements

* MacOS or Linux
* Python 3.11+
* Node.js 16+

The project is currently configured to expect the `activitypub-testsuite` repository in a sibling directory. In the future, this may be modified to include `activitypub-testsuite` as a git submodule in the `bovine-aptesting` testing repository.

### Set Up

1. Create a directory to hold the repositories, `testing`, for example, but the name doesn't matter.

2. Clone the `activitypub-testsuite` into that directory and install it.

```bash
git clone https://github.com/steve-bate/activitypub-testsuite.git
cd activitypub-testsuite/
poetry install
cd -
```

3. Clone the `bovine-aptesting` repository into the `testing` directory (a sibling of the previous repository). *Note the special submodule-related argument to clone.*

```bash
git clone --recurse-submodules https://github.com/steve-bate/bovine-aptesting
```

> [!NOTE]
> The bovine.pub submodule is currently a test-related branch of my `bovine.pub` fork. This branch contains several patches to fix issues and add some test-related endpoint (which are subject to change). This project will eventually be using the primary, authoritative repository.

At this point, the directory structure should look similar to the following one.

```
testing
  ├── activitypub-testsuite
  ├── bovine-aptesting
```

4. Change to the `bovine-aptesting` directory and install it. This will do the Python (Poetry) install and run `npm init` in the `bovine.pub` submodule (the code being tested).

```
cd bovine-aptesting
sh install.sh
```

## Usage

Run the tests from `bovine-aptesting` directory. The tests will run in a Python virtual environment created by Poetry. You will need to run them using

```bash
poetry run pytest
```
or
```bash
poetry shell  # creates a shell configured with the virtual environment
pytest
```

## License

[MIT License](LICENSE.txt)
