<!-- TODO Update bovine documentation -->
# bovine-aptesting

Experimental extension of the [activitypub-testsuite](https://github.com/steve-bate/activitypub-testsuite) for testing [bovine](https://codeberg.org/helge/bovine/).

This repository contains bovine-specific code and configuration. The test framework starts a Python subprocess at the beginning of a test session. The server main is in `server.py`. This sets up an in-memory database and adds a test reset endpoint. Before each test, the test reset action is invoked to reset the bovine database.

> [!NOTE]
> At the time this test suite was created, the bovine code was changing frequently. There's a good chance the test suite will not run with the current version of bovine (without some changes).
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
> The bovine submodule is currently a test-related branch of my `bovine` fork. This branch contains several patches to fix issues and add some test-related endpoint (which are subject to change). This project will eventually be using the primary, authoritative repository.

At this point, the directory structure should look similar to the following one.

```
testing
  ├── activitypub-testsuite
  ├── bovine-aptesting
```

1. Change to the `bovine-aptesting` directory and install it.

```
cd bovine-aptesting
poetry install
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
