import json
import discord
from discord import app_commands
from discord.ext.commands import Bot, Cog


class FunCog(Cog, description="Fun commands."):
    def __init__(self, client: Bot):
        self.client = client
        self.session = self.client.session

    @app_commands.command(name="cat", description="")
    @app_commands.guilds(discord.Object(id=537887803774730270))
    async def cat(self, interaction: discord.Interaction) -> None:
        pass


async def setup(client: Bot):
    await client.add_cog(FunCog(client))
