import discord
from discord import app_commands
from discord.ext.commands import Bot, Cog


class UtilCog(Cog, name="Utility"):
    def __init__(self, client: Bot):
        self.client = client


async def setup(client: Bot):
    await client.add_cog(UtilCog(client))
