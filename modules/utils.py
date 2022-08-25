import discord
from discord import app_commands
from discord.ext.commands import Bot, Cog


class UtilCog(Cog, name="Utility"):
    def __init__(self, client: Bot):
        self.client = client

    @app_commands.command(name="applestatus", description="Get Apple's current system statuses.")
    async def apple_status(self, interaction: discord.Interaction):
        pass

    @app_commands.command(name="dev-applestatus", description="Get Apple's current dev system statuses.")
    async def dev_apple_status(self, interaction: discord.Interaction):
        pass


async def setup(client: Bot):
    await client.add_cog(UtilCog(client))
