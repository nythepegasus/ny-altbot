import asyncio
import string
import re
from typing import List
import discord
from discord import app_commands
from discord.ext import commands
from utils.schema import Tag
from utils.modals import TagModal


class TagCog(commands.Cog, name="Tags"):
    def __init__(self, client):
        self.client = client
        self.description = "This module adds various commands for tags."
        self.tag_cache = []
        self.tag_cache_update = False

    @commands.Cog.listener("on_ready")
    async def on_ready(self) -> None:
        await self.update_cache()

    async def update_cache(self) -> None:
        self.tag_cache = [tag for tag in Tag.objects()]

    @app_commands.command(name="add-tag", description="Add a new tag")
    @app_commands.checks.has_any_role("Moderators", "Helpers", "Testers")
    @app_commands.guilds(discord.Object(id=537887803774730270))
    async def add_tag(self, interaction: discord.Interaction) -> None:
        self.tag_cache_update = True
        await interaction.response.send_modal(TagModal())

    @app_commands.command(name="edit-tag", description="Edit an existing tag")
    @app_commands.checks.has_any_role("Moderators", "Helpers", "Testers")
    @app_commands.guilds(discord.Object(id=537887803774730270))
    async def edit_tag(self, interaction: discord.Interaction, tag_name: str):
        self.tag_cache_update = True
        tag = Tag.objects(name=tag_name).first()
        if tag is None:
            raise Exception("Tag not found")
        modal = TagModal()
        modal.tag_name.label = "DON'T TOUCH IF YOU'RE EDITING TAG"
        modal.tag_name.default = tag.name
        modal.tag_content.default = tag.tag
        modal.tag_section.default = tag.section
        await interaction.response.send_modal(modal)

    @app_commands.command(name="tag", description="Send a tag")
    @app_commands.guilds(discord.Object(id=537887803774730270))
    async def tag(self, interaction: discord.Interaction, tag_name: str, user: discord.User = None):
        print(tag_name)
        if tag_name not in [tag.tag for tag in self.tag_cache]:
            await interaction.response.send_message("Tag doesn't exist.", ephemeral=True)
            return
        ret_str = f"*Tag suggestion for {user.mention}*:\n" if user is not None else ""
        ret_str += tag_name
        await interaction.response.send_message(ret_str)

    @tag.autocomplete("tag_name")
    async def tag_ac(self, _: discord.Interaction, current: str) -> List[app_commands.Choice[str]]:
        if self.tag_cache_update:
            await self.update_cache()
            self.tag_cache_update = False
        tags = [tag for tag in self.tag_cache if tag.name.startswith(current)][0:24]
        return [
            app_commands.Choice(name=tag.name, value=tag.tag)
            for tag in tags if current.lower() in tag.name.lower()
        ]

    @app_commands.command(name="rem-tag", description="Remove a tag")
    @app_commands.checks.has_any_role("Moderators", "Helpers")
    @app_commands.guilds(discord.Object(id=537887803774730270))
    async def rem_tag(self, interaction: discord.Interaction, tag_name: str):
        if tag_name not in [tag.name for tag in self.tag_cache]:
            await interaction.response.send_message(f"Tag {tag_name} doesn't exist.", ephemeral=True)
            return
        Tag.objects(name=tag_name).delete()
        await interaction.response.send_message(f"Tag {tag_name} has been deleted.", ephemeral=True)
        await self.update_cache()

    @edit_tag.autocomplete("tag_name")
    @rem_tag.autocomplete("tag_name")
    async def tag_rm_ac(self, _: discord.Interaction, current: str) -> List[app_commands.Choice[str]]:
        if self.tag_cache_update:
            await self.update_cache()
            self.tag_cache_update = False
        tags = [tag for tag in self.tag_cache if tag.name.startswith(current)][0:24]
        return [
            app_commands.Choice(name=tag.name, value=tag.name)
            for tag in tags if current.lower() in tag.name.lower()
        ]

    @add_tag.error
    @rem_tag.error
    @edit_tag.error
    async def tag_error(self, interaction: discord.Interaction, error):
        await interaction.followup.send(error, ephemeral=True)
        print(type(error))
        print(error)


async def setup(client: commands.Bot):
    await client.add_cog(TagCog(client), guilds=[discord.Object(id=537887803774730270)])
