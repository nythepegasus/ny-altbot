import io
import os
import discord
from PIL import Image
from pyppeteer import launch
from discord import app_commands
from discord.ext.commands import Bot, Cog, command


class UtilCog(Cog, name="Utility"):
    def __init__(self, client: Bot):
        self.client = client

    @app_commands.command(name="applestatus", description="Get Apple's current system statuses.")
    async def apple_status(self, interaction: discord.Interaction):
        pass

    @app_commands.command(name="dev-applestatus", description="Get Apple's current dev system statuses.")
    async def dev_apple_status(self, interaction: discord.Interaction):
        pass

    @command()
    async def sync(self, ctx):
        c = await self.client.tree.sync()
        await ctx.send(f"Synced {len(c)} global commands.")

    @command()
    async def sync_dev(self, ctx):
        c = await self.client.tree.sync(guild=discord.Object(537887803774730270))
        await interaction.response.send_message(f"Synced {len(c)} dev commands.")

async def setup(client: Bot):
    await client.add_cog(UtilCog(client))
