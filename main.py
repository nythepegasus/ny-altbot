import os
import sys
import json
import random
import dotenv
import aiohttp
import asyncpg
import discord
import asyncssh
import traceback
import pushover as po
from datetime import datetime
from packaging import version
from discord import Embed, Interaction
from discord.app_commands import AppCommandError
from discord.app_commands.errors import MissingRole, MissingAnyRole
from discord.ext import commands, tasks
from discord.ext.commands.errors import CheckFailure, CommandNotFound
from utils.views import RoleDropdown, RoleDropdownView

os.chdir(os.path.dirname(os.path.abspath(__file__)))

class MyClient(commands.Bot):
    def __init__(self, conf_data: dict, *args, **kwargs):
        super().__init__(*args, command_prefix=conf_data["DISCORD_PREFIX"], intents=discord.Intents().all(),
                         application_id=conf_data["DISCORD_APPID"], **kwargs)
        self.session = None
        self.db = None
        self.__TOKEN = conf_data.pop("DISCORD_TOKEN")
        self.conf = conf_data
        self.owner_id = self.conf["DISCORD_OID"]
        self.pclient = po.Client(self.conf["PUSHOVER_UK"], self.conf["PUSHOVER_AK"])
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
            async with self.session(timeout=aiohttp.ClientTimeout(total=5)) as session:
                async with session.get(url) as response:
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

    @tasks.loop(seconds=5)
    async def check_anisette(self) -> None:
        await self.wait_until_ready()
        async with self.session(timeout=aiohttp.ClientTimeout(total=5)) as session:
            try:
                async with session.get("http://ani.sidestore.io:6969/", timeout=aiohttp.ClientTimeout(total=5)) as response:
                    try:
                        data = json.loads(await response.text())
                        self._lsa = datetime.now()
                        # print(f"Successful anisette at {self._lsa}")
                        return
                    except json.decoder.JSONDecodeError:
                        print(f"JSONDecodeError: Something funky is going on, here is `response.text()`: '{await response.text()}'\n"
                              f"Last successful anisette: {self._lsa}")
                        return await self.reset_anisette()

            except aiohttp.client_exceptions.ClientConnectorError as e:
                print(f'ClientConnectorErrorError: {e}\n'
                      f'Last successful anisette: {self._lsa}')
            except Exception as e:
                print(f'Exception unhandled: {e}\n'
                      f'Last successful anisette: {self._lsa}')
            return await self.reset_anisette()

    async def setup_hook(self) -> None:
        self.session = aiohttp.ClientSession
        try:
            self.ssh_conn = await asyncssh.connect(self.conf["SSH_HOST"],
                                                   username=self.conf["SSH_USER"],
                                                   client_keys = [asyncssh.read_private_key("~/.ssh/auto_ed25519")])
            print("Connected to SSH!")
        except Exception as e:
            print(f"Couldn't connect to SSH: {e}")
        self._lsa = None
        self.check_anisette.start()
        self.change_status.start()

        self.db = await asyncpg.connect(user=self.conf["POSTGRES_USER"],
                                        password=self.conf["POSTGRES_PASSWORD"],
                                        database=self.conf["POSTGRES_DB"],
                                        host=self.conf["POSTGRES_HOST"])
        print("Connected to postgres!")

        menus = await self.db.fetch("SELECT * FROM role_menus")
        for menu in menus:
            roles = await self.db.fetch("SELECT * FROM role_menu_info WHERE mid = $1 ORDER BY rid ASC", menu["id"])
            r = roles[0]
            choices = [discord.SelectOption(label=role["rname"], description=role["rdesc"], value=role["rid"], emoji=role["remoji"]) for role in roles]
            if r["mmchoice"] > 1:
                choices.append(discord.SelectOption(label="Remove Roles",
                                                    description="This removes all listed roles above, so that you can rechoose which roles you actually want.", 
                                                    value="0"))
            view = RoleDropdownView(RoleDropdown(options=choices, placeholder=r["mplaceholder"], min_values=1,
                                                 max_values=r["mmchoice"], custom_id=str(r["mid"])))
            self.add_view(view)

        update_channels = await self.db.fetch("SELECT * FROM update_channels")
        self.update_channels = [await self.fetch_channel(channel["channel_id"]) for channel in update_channels]

        self.update_apps.start()
        for ext in ["modules." + e for e in self.conf["DISCORD_MODULES"].split(",")]:
            try:
                await self.load_extension(ext)
                print(f"Loaded extension {ext}")
            except Exception as e:
                print(f'Failed to load extension {ext}.', file=sys.stderr)
                print(f"{type(e).__name__} - {e}")
                traceback.print_exc()

    async def reset_anisette(self):
        try:
            create_tmux = await self.ssh_conn.run("tmux new-session -d -s anisette '/home/ny/prod/omnisette/omnisette-server-linux --http-port 6969'")
            result_one = await self.ssh_conn.run("tmux send-keys -t 'anisette:0' C-c './omnisette-server-linux --http-port 6969' Enter")
            result_two = await self.ssh_conn.run("tmux send-keys -t 'anisette:0' './omnisette-server-linux --http-port 6969' Enter")

            if create_tmux.exit_status == 0:
                print("Yay created tmux :)")
            else:
                print("It's probably already there..")

            if result_one.exit_status == 0:
                print(result_one.stdout, end='')
            else:
                print("Anisette tmux command 1 with ctrl-C failed, oh well.")

            if result_two.exit_status == 0:
                print(result_two.stdout, end='')
            else:
                print("Uh oh, this is bad news bears!")
        except Exception as ex:
            print(ex)

    async def close(self):
        if self.session is not None:
            await self.session.close(self.session)
        if self.ssh_conn is not None:
            self.ssh_conn.close()
        await super().close()

    def run(self):
        super().run(self.__TOKEN)


client = MyClient({**os.environ, **dotenv.dotenv_values()})


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
