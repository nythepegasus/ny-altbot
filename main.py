import sys
import json
import random
import aiohttp
import asyncpg
import discord
import traceback
import pushover as po
from datetime import datetime
from packaging import version
from discord import Embed, Interaction
from discord.app_commands import AppCommandError
from discord.app_commands.errors import MissingRole, MissingAnyRole
from discord.ext import commands, tasks
from discord.ext.commands.errors import CheckFailure, CommandNotFound


class MyClient(commands.Bot):
    def __init__(self, conf_data: dict, *args, **kwargs):
        super().__init__(*args, command_prefix=conf_data["prefix"], intents=discord.Intents().all(),
                         application_id=conf_data["application_id"], **kwargs)
        self.session = None
        self.db = None
        self.__TOKEN = conf_data.pop("TOKEN")
        self.conf_data = conf_data
        self.owner_id = self.conf_data["owner_id"]
        self.pclient = po.Client(self.conf_data["pushover"]["user_key"], self.conf_data["pushover"]["api_key"])
        self.update_channels = None
        self.remove_command("help")

    async def on_ready(self) -> None:
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    @tasks.loop(minutes=5)
    async def update_apps(self) -> None:
        await self.wait_until_ready()
        sources = [s['url'] for s in await self.db.fetch("SELECT url FROM sources")]
        for url in sources:
            async with self.session.get(url) as response:
                data = json.loads(await response.text())
                for app in data["apps"]:
                    old_app = await self.db.fetchrow(f"SELECT * FROM apps WHERE id = '{app['bundleIdentifier']}'")
                    if old_app is None:
                        await self.db.execute(f"INSERT INTO apps VALUES('{app['bundleIdentifier']}', '{app['name']}', "
                                              f"'{app['version']}', '{data['identifier']}')")
                        continue
                    else:
                        if version.parse(app["version"]) > version.parse(old_app['version']):
                            await self.db.execute(f"UPDATE apps SET version='{app['version']}', name='{app['name']}'"
                                                  f"WHERE id = '{app['bundleIdentifier']}'")
                            emb = Embed(title=f"New {app['name']} update!", color=int(app['tintColor'], 16),
                                        timestamp=datetime.now())
                            emb.add_field(name="Version:", value=f"{old_app['version']} -> {app['version']}", inline=False)
                            emb.add_field(name="Changelog:", value=app['versionDescription'], inline=False)
                            emb.set_thumbnail(url=app['iconURL'])
                            emb.set_footer(text="AltBot v. 1.0")
                            for channel in self.update_channels:
                                ping_roles = await self.db.fetch(f"SELECT role_id FROM ping_roles "
                                                                 f"WHERE guild_id = {channel.guild.id} AND "
                                                                 f"appbundle_id = '{app['bundleIdentifier']}'")
                                guild = self.get_guild(channel.guild.id)
                                ret_msg = " ".join([guild.get_role(r["role_id"]).mention for r in ping_roles])
                                await channel.send(content=ret_msg, embed=emb)

    @tasks.loop(minutes=10)
    async def change_status(self) -> None:
        await self.wait_until_ready()
        status = random.choice(["DS", "N64", "GBA", "GBC", "SNES", "NES"])
        presence = discord.Game(f"{status} games on Delta with {len(self.users)} others!")
        await self.change_presence(activity=presence)

    async def setup_hook(self) -> None:
        self.change_status.start()

        self.db = await asyncpg.connect(**self.conf_data["postgres"])
        print("Connected to postgres!")

        update_channels = await self.db.fetch("SELECT * FROM update_channels")
        self.update_channels = [await self.fetch_channel(channel["channel_id"]) for channel in update_channels]

        self.update_apps.start()
        for ext in self.conf_data["modules"]:
            try:
                await self.load_extension(ext)
                print(ext)
            except Exception as e:
                print(f'Failed to load extension {ext}.', file=sys.stderr)
                print(f"{type(e).__name__} - {e}")
                traceback.print_exc()
        self.session = aiohttp.ClientSession()

    async def close(self):
        if self.session is not None:
            await self.session.close()
        await super().close()

    def run(self):
        super().run(self.__TOKEN)


client = MyClient(json.load(open("conf.json")))


@client.listen()
async def on_command_error(ctx, error):
    await ctx.message.delete()
    if isinstance(error, CheckFailure):
        print(f"Ignoring Check Failure from user: {ctx.author.name}")
    elif isinstance(error, CommandNotFound):
        print(f"Ignoring command not found, no normal user should be using text commands: {ctx.author.name}\n {error}")
    else:
        raise error


@client.tree.error
async def on_app_command_error(interaction: Interaction, error: AppCommandError):
    if isinstance(error, (MissingRole, MissingAnyRole)):
        await interaction.response.send_message(error, ephemeral=True)
        return
    else:
        print(error)
        raise error


client.run()
