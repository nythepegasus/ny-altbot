import discord
import traceback
from .schema import Tag


class TagModal(discord.ui.Modal, title="New Tag"):
    tag_name = discord.ui.TextInput(
        label="Tag Name",
        placeholder="Tag name here.."
    )
    tag_content = discord.ui.TextInput(
        label="Tag Description",
        style=discord.TextStyle.long
    )
    tag_section = discord.ui.TextInput(
        label="Tag Section (Optional)",
        required=False
    )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        db_tag = Tag.objects(name=self.tag_name.value).first()
        if db_tag is not None:
            ret_str = F"Edited tag {self.tag_name.value}"
        else:
            ret_str = f"New tag created '{self.tag_name.value}'"
        await interaction.response.send_message(ret_str, ephemeral=True)
        db_tag.update(set__tag=self.tag_content.value, set__section=self.tag_section.value)

    async def on_error(self, error: Exception, interaction: discord.Interaction) -> None:
        await interaction.response.send_message(f"Oops something went wrong!", ephemeral=True)
        traceback.print_tb(error.__traceback__)
