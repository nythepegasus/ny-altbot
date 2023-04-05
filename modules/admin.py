import json
import asyncio
import discord
from datetime import timedelta
from discord import app_commands
from typing import Optional, Literal
from discord.ext import commands
from discord.ext.commands import Bot, Cog, command, ExtensionNotLoaded, ExtensionAlreadyLoaded, ExtensionNotFound


class AdminCog(Cog, name="Admin"):
    def __init__(self, client: Bot):
        self.client = client
        self.description = "This module is only for the developer"

    async def cog_before_invoke(self, ctx):
        try:
            await ctx.message.delete()
        except:
            return

    async def cog_check(self, ctx):
        return int(self.client.owner_id) == ctx.author.id

    async def cog_command_error(self, ctx, error):
        print(ctx)
        print(error)

    @command(name="load", hidden=True, help="Loads a cog.")
    async def load_cog(self, ctx, *, cog: str):
        try:
            await self.client.load_extension(f"modules.{cog}")
        except (ExtensionAlreadyLoaded, ExtensionNotFound) as e:
            await ctx.author.send(f"**`ERROR:`**\n {type(e).__name__} - {e}")
        else:
            await ctx.send(f"`{cog}` has been loaded!", delete_after=5)

    @command(name="unload", hidden=True, help="Unloads a cog.")
    async def unload_mod(self, ctx, *, cog: str):
        if cog == "modules.admin":
            return await ctx.send("Cowardly refusing to unload admin cog.", delete_after=5)
        try:
            await self.client.unload_extension(f"modules.{cog}")
            return await ctx.send(f"`{cog}` has been unloaded!", delete_after=5)
        except (ExtensionNotLoaded, ExtensionNotFound) as e:
            await ctx.author.send(f"**`ERROR:`**\n {type(e).__name__} - {e}")

    @command(name="reload", hidden=True, help="Reloads a cog.")
    async def unload_cog(self, ctx, *, cog: str):
        try:
            await self.client.reload_extension(f"modules.{cog}")
            return await ctx.send(f"`{cog}` has been reloaded!", delete_after=5)
        except (ExtensionNotLoaded, ExtensionNotFound) as e:
            await ctx.author.send(f"**`ERROR:`**\n {type(e).__name__} - {e}")

    @command()
    @commands.guild_only()
    async def sync(self, ctx: commands.Context, guilds: commands.Greedy[discord.Object], spec: Optional[Literal["~", "*", "^"]] = None) -> None:
        print(f"{guilds = }")
        if not guilds:
            if spec == "~":
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "*":
                ctx.bot.tree.copy_global_to(guild=ctx.guild)
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "^":
                ctx.bot.tree.clear_commands(guild=ctx.guild)
                await ctx.bot.tree.sync(guild=ctx.guild)
                synced = []
            else:
                synced = await ctx.bot.tree.sync()

            return await ctx.send(
                f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}",
                delete_after=5
            )
            

        ret = 0
        for guild in guilds:
            try:
                await ctx.bot.tree.sync(guild=guild)
            except discord.HTTPException:
                pass
            else:
                ret += 1

        await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.", delete_after=5)

    @command(name="update", hidden=True, help="Update the bot.")
    async def update_bot(self, ctx):
        """We should git pull, and reload all the modules"""
        proc = await asyncio.create_subprocess_exec(
            "git", "pull", stdout=asyncio.subprocess.PIPE
        )
        data = await proc.stdout.readline()
        line = data.decode('ascii').rstrip()
        await proc.wait()
        print(line)

        for cog in self.client.conf_data["modules"]:
            await self.client.reload_extension(cog)

        await ctx.send("Updated the bot!", delete_after=5)

    @command(name="add_cog", hidden=True, help="Add cog to bot.")
    async def add_mod(self, ctx, *, cog: str):
        conf = json.load(open("conf.json"))
        try:
            await self.client.load_extension(f"modules.{cog}")
        except (ExtensionNotFound, ExtensionAlreadyLoaded) as e:
            if isinstance(e, ExtensionNotFound):
                return await ctx.send(f"Couldn't find `{cog}` to add to startup.", delete_after=5)
            elif isinstance(e, ExtensionAlreadyLoaded):
                pass

        if f"modules.{cog}" in conf["modules"]:
            return await ctx.send(f"`{cog}` is already in startup.", delete_after=5)
        conf["modules"].append(f"modules.{cog}")
        json.dump(conf, open("conf.json", "w"), indent=4)
        return await ctx.send(f"`{cog}` has been added to bot startup!", delete_after=5)

    @app_commands.command(name="yeet", description="Timeout a user")
    @app_commands.describe(user="The user to recommend this tag to.")
    @app_commands.describe(duration="The duration to time them out for")
    @app_commands.describe(reason="Reason for timing them out")
    async def yeet(self, interaction: discord.Interaction, user: discord.User, duration: str, reason: str = None):
        units = {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800}
        try:
            unit = units[duration[-1]]
            value = int(duration[:-1])
            timer = value * unit
        except (KeyError, ValueError):
            return await interaction.response.send_message(f"Invalid duration format. Use 's' for seconds, 'm' for minutes, 'h' for hours, 'd' for days, and 'w' for weeks.", ephemeral=True)
        await user.timeout(timedelta(seconds=timer), reason=reason)
        return await interaction.response.send(f"Timed out user {user.name} for {timer} seconds.", ephemeral=True)

    @yeet.autocomplete("duration")
    async def yeet_ac(self, interaction: discord.Interaction, current: str):
        date_formats = ["1h", "1d", "1w", "30m", "15m"]
        ret = [date_str for date_str in date_formats if date_str.startswith(string.lower())]
        if len(ret) == 0:
            return date_formats


async def setup(client: Bot):
    await client.add_cog(AdminCog(client))
