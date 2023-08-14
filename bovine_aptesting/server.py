import os

server_dir = os.path.dirname(os.path.realpath(__file__))
os.environ["BOVINE_CONTEXT_CACHE"] = os.path.join(
    server_dir, "..", "bovine_data", "context_cache"
)

# Environment must be set up before imports
# ruff: noqa: E402


from bovine_herd import bovine_herd
from bovine_store import register
from bovine_store.models import (
    BovineActorEndpoint,
    BovineActorKeyPair,
    CollectionItem,
    StoredJsonObject,
    VisibleTo,
)
from quart import Quart


class BovineServer:
    def __init__(self, server_port: int, use_disk: bool):
        self.server_port = server_port
        self.registered = False
        self.use_disk = use_disk

    def run(self):
        app = Quart(__name__)

        if not self.use_disk:
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

            # await register(name, None, ep)
            await register(name, f"http://localhost:{self.server_port}/endpoints/")

        @app.get("/test/reset")
        async def test_reset():
            await CollectionItem.all().delete()
            await StoredJsonObject.all().delete()
            await VisibleTo.all().delete()
            return "OK"

        @app.get("/test/actor_info")
        async def get_actor_info():
            key_pair = await BovineActorKeyPair.get_or_none(name="serverKey")
            actor_ep = await BovineActorEndpoint.get_or_none(stream_name="ACTOR")
            return {
                "uri": actor_ep.name,
                "private_key": key_pair.private_key,
            }

        app.run(port=self.server_port)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=50000)
    parser.add_argument("--use-disk", action="store_true")
    args = parser.parse_args()
    server = BovineServer(args.port, args.use_disk)
    server.run()
