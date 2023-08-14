from typing import Any

import httpx
import pytest
from activitypub_testsuite.http.client import HttpxBaseActor, HttpxServerTestSupport
from activitypub_testsuite.http.signatures import HTTPSignatureAuth
from activitypub_testsuite.interfaces import Actor


class BovineLocalActor(HttpxBaseActor):
    def __init__(self, server: HttpxServerTestSupport, profile: dict, auth: Any = None):
        super().__init__(server, profile, auth)

    def get_actor_uri(self, *_):
        return self.profile["id"]


class BovineServerTestSupport(HttpxServerTestSupport):
    def __init__(self, local_base_url, remote_base_url, request):
        super().__init__(local_base_url, remote_base_url, request)

    def get_local_actor(self, actor_name: str = None) -> Actor:
        if actor_name is not None:
            pytest.skip("Single actor instance")
        # Need to create an authenticdated remote actor to get the local actor profile
        response = httpx.get(f"{self.local_base_url}/test/actor_info")
        response.raise_for_status()
        actor_info = response.json()
        remote_actor = self.request.getfixturevalue("remote_actor")
        profile = remote_actor.get_json(actor_info["uri"])
        auth = HTTPSignatureAuth(profile["publicKey"]["id"], actor_info["private_key"])
        return BovineLocalActor(self, profile, auth=auth)
