import os

server_dir = os.path.dirname(os.path.realpath(__file__))
os.environ["BOVINE_CONTEXT_CACHE"] = os.path.join(
    server_dir, "..", "bovine_data", "context_cache"
)

# Environment must be set up before imports
# ruff: noqa: E402

import sys

from bovine_herd import bovine_herd
from bovine_store import register
from bovine_store.models import (
    BovineActorKeyPair,
    CollectionItem,
    StoredJsonObject,
    VisibleTo,
)
from quart import Quart


class BovineServer:
    def __init__(self, server_port):
        self.server_port = server_port
        self.registered = False

    def run(self):
        app = Quart(__name__)

        os.environ["BOVINE_DB_URL"] = "sqlite://:memory:"

        bovine_herd(app)

        @app.before_serving
        async def register_local_actor():
            if self.registered:
                raise Exception("Already registered local_actor_1")
            print("Creating test user: local_actor_1")
            name = "local_actor_1"

            def ep(suffix):
                if suffix == "actor":
                    suffix = name
                return f"http://localhost:{self.server_port}/endpoints/{suffix}"

            await register(name, None, ep)

        @app.get("/test/reset")
        async def test_reset():
            await CollectionItem.all().delete()
            await StoredJsonObject.all().delete()
            await VisibleTo.all().delete()
            return "OK"

        @app.get("/test/private_key")
        async def get_private_key():
            key_pair = await BovineActorKeyPair.get_or_none(name="serverKey")
            return key_pair.private_key

        app.run(port=self.server_port)


if __name__ == "__main__":
    server = BovineServer(int(sys.argv[1]) if len(sys.argv) > 1 else 50000)
    server.run()
