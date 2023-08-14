import os

import httpx
import pytest
from activitypub_testsuite.fixtures import *  # noqa
from activitypub_testsuite.interfaces import ServerTestSupport

from bovine_aptesting.support import BovineServerTestSupport

# from activitypub_testsuite.interfaces import ServerTestSupport

# from .support import OnepageServerTestSupport


@pytest.fixture(scope="session")
def server_test_directory():
    return os.path.dirname(__file__)


@pytest.fixture
def server_support(
    local_base_url,
    local_get_json,
    remote_base_url,
    request,
) -> ServerTestSupport:
    return BovineServerTestSupport(
        local_base_url,
        remote_base_url,
        request,
    )


def pytest_configure():
    pkg_dir = os.path.dirname(os.path.realpath(__file__))
    install_fedi_tests(os.path.join(pkg_dir, "tests"))  # noqa: F405


@pytest.fixture
def instance_metadata():
    return {
        "name": "bovine",
    }


# @pytest.fixture
# def server_support(local_base_url, remote_base_url, request) -> ServerTestSupport:
#     return OnepageServerTestSupport(local_base_url, remote_base_url, request)


@pytest.fixture(scope="session")
def server_subprocess_config(
    server_test_directory, local_server_port
) -> ServerSubprocessConfig:  # noqa: F405
    return ServerSubprocessConfig(  # noqa: F405
        args=["python", "server.py", str(local_server_port)],
        cwd=os.path.join(server_test_directory),
        start_matcher=lambda line: "Running on" in line,
        error_matcher=lambda line: "Traceback" in line,
    )


@pytest.fixture(autouse=True)
def reset_local_server_state(local_base_url):
    print("reset local server data")
    response = httpx.get(f"{local_base_url}/test/reset")
    response.raise_for_status()


# @pytest.fixture(autouse=True)
# def reset_server_store(local_base_url, local_server_subprocess):
#     # local_server_subprocess is referenced to ensure proper autouse startup order
#     response = httpx.get(f"{local_base_url}/test/reset", timeout=None, verify=False)
#     response.raise_for_status()

#
# Bovine test server setup
#
