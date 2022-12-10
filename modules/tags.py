import discord
from discord import app_commands
from discord.ext import commands
from utils.modals import TagModal


class TagCog(commands.Cog, name="Tags"):
    def __init__(self, client):
        self.client = client
        self.description = "This module adds various commands for tags."

    @app_commands.command(name="tag", description="Send a tag")
    @app_commands.describe(tag_name="Name of the tag.")
    @app_commands.describe(user="The user to recommend this tag to.")
    @app_commands.checks.has_any_role("Mods", "Moderator", "Helpers", "Helper", "Testers")
    async def tag(self, interaction: discord.Interaction, tag_name: str, user: discord.User = None):
        tag = await self.client.db.fetchrow(f"SELECT * FROM tags WHERE name = '{tag_name}'")
        if tag is None:
            return await interaction.response.send_message(f"Tag '{tag_name}' doesn't exist.", ephemeral=True)
        ret_str = f"*Tag suggestion for {user.mention}*:\n" if user is not None else ""
        ret_str += tag["tag"]
        await interaction.response.send_message(ret_str)

    @app_commands.command(name="add-tag", description="Add a new tag")
    @app_commands.checks.has_any_role("Mods", "Helpers", "Testers")
    async def add_tag(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_modal(TagModal())

    @app_commands.command(name="edit-tag", description="Edit an existing tag")
    @app_commands.describe(tag_name="Name of the tag.")
    @app_commands.checks.has_any_role("Mods", "Moderator", "Helpers", "Helper")
    async def edit_tag(self, interaction: discord.Interaction, tag_name: str):
        tag = await self.client.db.fetchrow(f"SELECT * FROM tags WHERE name LIKE '{tag_name}%'")
        if tag is None:
            return await interaction.response.send_message(f"Tag '{tag_name}' doesn't exist.", ephemeral=True)
        modal = TagModal()
        modal.tag_name.label = "DON'T TOUCH IF YOU'RE EDITING TAG"
        modal.tag_name.default = tag["name"]
        modal.tag_content.default = tag["tag"]
        modal.tag_section.default = tag["section"]
        await interaction.response.send_modal(modal)

    @app_commands.command(name="remove-tag", description="Remove a tag")
    @app_commands.describe(tag_name="Name of the tag.")
    @app_commands.checks.has_any_role("Mods", "Moderator", "Helpers", "Helper")
    async def rem_tag(self, interaction: discord.Interaction, tag_name: str):
        tags = await self.client.db.fetchrow(f"SELECT * FROM tags WHERE name = '{tag_name}'")
        if len(tags) == 0:
            await interaction.response.send_message(f"Tag {tag_name} doesn't exist.", ephemeral=True)
            return
        await self.client.db.execute(f"DELETE FROM tags WHERE name = '{tag_name}'")
        await interaction.response.send_message(f"Tag {tag_name} has been deleted.", ephemeral=True)

    @tag.autocomplete("tag_name")
    @edit_tag.autocomplete("tag_name")
    @rem_tag.autocomplete("tag_name")
    async def tag_ac(self, _: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
        tags = await self.client.db.fetch(f"SELECT * FROM tags WHERE name LIKE '{current}%' LIMIT 25")
        return [app_commands.Choice(name=tag["name"], value=tag["name"]) for tag in tags]


async def setup(client: commands.Bot):
    await client.add_cog(TagCog(client))
