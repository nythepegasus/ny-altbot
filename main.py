import sys
import json
import aiohttp
import asyncio
import discord
import traceback
import mongoengine
from discord import Embed
from packaging import version
from utils.schema import Application
from discord.ext import commands, tasks


class MyClient(commands.Bot):
    def __init__(self, conf_data: dict, *args, **kwargs):
        super().__init__(*args, command_prefix=conf_data["prefix"], intents=discord.Intents().all(),
                         application_id=706563324560801793, **kwargs)
        self.session = None
        self.owner_id = conf_data["owner_id"]
        self.mgocnf = conf_data["mongodb"]
        self.modules = conf_data["modules"]
        self.sources = conf_data["sources"]
        self.reroles = conf_data["reaction_roles"]
        self.__TOKEN = conf_data["TOKEN"]
        mongoengine.connect(host=f"mongodb://{self.mgocnf['ipport']}/{self.mgocnf['db']}")
        print("Connected to MongoDB!")
        self.remove_command("help")

    async def on_ready(self) -> None:
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    @tasks.loop(minutes=1)
    async def update_apps(self) -> None:
        await self.wait_until_ready()
        for url in self.sources:
            async with self.session.get(url) as response:
                html = await response.text()
                for app in json.loads(html)["apps"]:
                    old_app = Application.objects(bundle_id=app["bundleIdentifier"]).first()
                    if old_app is None:
                        Application(bundle_id=app["bundleIdentifier"],
                                    name=app["name"],
                                    version=app["version"]).save()
                        continue
                    else:
                        print(app["bundleIdentifier"])
                        print(f"{app['version']} > {old_app.version}")
                        print(version.parse(app["version"]) > version.parse(old_app.version))
                        if version.parse(app["version"]) > version.parse(old_app.version):
                            old_app.update(set__version=app["version"])
                            if "a" in app["version"]:
                                # Alpha update!
                                pass
                            elif "b" in app["version"]:
                                # Beta update!
                                pass
                            else:
                                # Normal update!
                                pass
                            # send to update channels if app is newer

    async def setup_hook(self) -> None:
        # self.update_apps.start()
        for ext in self.modules:
            try:
                await self.load_extension(ext)
                print(ext)
            except Exception as e:
                print(f'Failed to load extension {ext}.', file=sys.stderr)
                print(f"{type(e).__name__} - {e}")
                traceback.print_exc()
        await self.tree.sync(guild=discord.Object(537887803774730270))
        self.session = aiohttp.ClientSession()

    async def close(self):
        await super().close()
        await self.session.close()

    def run(self):
        super().run(self.__TOKEN)


MyClient(json.load(open("confs/conf.json"))).run()
