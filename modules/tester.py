import json
import discord
from discord import app_commands
from discord.ext.commands import Bot, Cog


class TesterCog(Cog):
    def __init__(self, client: Bot):
        self.client = client

    async def cog_before_invoke(self, ctx) -> None:
        print("Hello!")

    @app_commands.command(name="test", description="[DEBUG ONLY] I cannot assure this command will always function as expected.")
    @app_commands.guilds(discord.Object(id=537887803774730270))
    async def test(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message("Printing guild roles..", ephemeral=True)
        roles = await interaction.guild.fetch_roles()
        print(", ".join([role.name for role in roles]))
        raise TypeError("Woops")

    @app_commands.command(name="tester", description="Testing error handler")
    @app_commands.checks.has_role("Mods")
    @app_commands.guilds(discord.Object(id=537887803774730270))
    async def tester(self, interaction: discord.Interaction):
        await interaction.response.send_message("Testing errors..")

    @test.error
    @tester.error
    async def test_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingRole):
            await interaction.response.send_message(error, ephemeral=True)
            return
        if interaction.response.is_done():
            await interaction.followup.send(error, ephemeral=True)
        print(type(error))
        print(error)


async def setup(client: Bot):
    await client.add_cog(TesterCog(client))
