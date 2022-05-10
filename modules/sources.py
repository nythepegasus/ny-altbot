import json
import discord
from discord import app_commands
from discord.ext.commands import Bot, Cog
from aiohttp.client_exceptions import InvalidURL


class SourcesCog(Cog, name="Sources"):
    def __init__(self, client: Bot):
        self.client = client

    @app_commands.command(name="add-source", description="Add a link to an AltStore source.")
    @app_commands.describe(source_name="Name of the AltSource.")
    @app_commands.describe(source_url="URL of the AltSource.")
    @app_commands.checks.has_any_role("Moderators", "Helpers")
    async def add_source(self, interaction: discord.Interaction, source_name: str, source_url: str) -> None:
        await interaction.response.send_message(
            f"[{source_name}](https://delta-skins.github.io/sourceinstall.html?altstore://url?={source_url})"
        )

    @app_commands.command(name="track-source", description="Add an AltSource to track with AltBot")
    @app_commands.describe(source_url="URL of AltSource to track.")
    @app_commands.checks.has_role("Moderators")
    async def track_source(self, interaction: discord.Interaction, source_url: str):
        try:
            async with self.client.session.get(source_url) as response:
                data = json.loads(await response.text())
                await self.client.db.execute(f"INSERT INTO sources "
                                             f"VALUES('{data['identifier']}', '{data['name']}', '{source_url}')")
                await interaction.response.send_message(f"Added '{data['name']}' as a source.", ephemeral=True)
        except (InvalidURL, json.decoder.JSONDecodeError):
            await interaction.response.send_message(f"'{source_url}' is not an AltSource, or is malformed in some way.",
                                                    ephemeral=True)

    @app_commands.command(name="list-sources", description="List all tracked AltSources")
    async def list_sources(self, interaction: discord.Interaction):
        sources = [s['name'] for s in await self.client.db.fetch("SELECT name FROM sources")]
        await interaction.response.send_message("Current sources:\n"+'\n'.join(sources), ephemeral=True)

    @app_commands.command(name="add-update-channel", description="Add an update channel to track AltSource apps.")
    @app_commands.describe(channel="The channel to receive app update notifications.")
    @app_commands.checks.has_role("Moderators")
    async def add_update_channel(self, interaction: discord.Interaction, channel: app_commands.AppCommandChannel):
        self.client.update_channels.append(self.client.get_channel(channel.id))
        await self.client.db.execute(f"INSERT INTO update_channels VALUES({channel.id})")
        await interaction.response.send_message(f"Inserted '{channel.name}' as an update channel.", ephemeral=True)

    @app_commands.command(name="remove-update-channel", description="Delete an update channel.")
    @app_commands.describe(channel="The channel to remove from app update notifications.")
    @app_commands.checks.has_role("Moderators")
    async def rem_update_channel(self, interaction: discord.Interaction, channel: str):
        channel = await self.client.fetch_channel(int(channel))
        self.client.update_channels.remove(channel)
        await self.client.db.execute(f"DELETE FROM update_channels WHERE channel_id = {channel.id}")
        await interaction.response.send_message(f"Removed '{channel.name}' as an update channel.", ephemeral=True)

    @rem_update_channel.autocomplete("channel")
    async def del_channel_ac(self, interaction: discord.Interaction, _: str) -> list[app_commands.Choice[str]]:
        channels = await self.client.db.fetch("SELECT * FROM update_channels")
        channels = [await self.client.fetch_channel(c["channel_id"]) for c in channels]
        return [app_commands.Choice(name=c.name, value=str(c.id)) for c in channels]

    @app_commands.command(name="add-ping-role", description="Add a role to be pinged on updates.")
    @app_commands.checks.has_role("Moderators")
    async def add_ping_role(self, interaction: discord.Interaction, role: discord.Role, app_id: str):
        await self.client.db.execute(f"INSERT INTO ping_roles VALUES({interaction.guild_id}, {role.id}, '{app_id}')")
        await interaction.response.send_message(f"Added role {role.name} to be pinged for {app_id}.", ephemeral=True)

    @add_ping_role.autocomplete("app_id")
    async def ping_type_ac(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
        types = sorted([a["id"] for a in await self.client.db.fetch(f"SELECT id FROM apps")])
        return [app_commands.Choice(name=t.replace("com.rileytestut.", "").replace(".", " "), value=t)
                for t in types if current.lower() in t.lower()]


async def setup(client: Bot):
    await client.add_cog(SourcesCog(client))
