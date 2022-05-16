import discord
import traceback


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
        name = self.tag_name.value
        tag = self.tag_content.value
        section = self.tag_section.value
        db_tag = await interaction.client.db.fetch(f"SELECT * FROM tags WHERE name = '{name}'")
        if len(db_tag) is not 0:
            ret_str = F"Edited tag {self.tag_name.value}"
        else:
            ret_str = f"New tag created '{self.tag_name.value}'"
        await interaction.client.db.execute(f"INSERT INTO tags "
                                            f"VALUES('{name}', '{tag}', '{section}') ON CONFLICT (name) "
                                            f"DO UPDATE SET tag = '{tag}', section = '{section}'")
        await interaction.response.send_message(ret_str, ephemeral=True)

    async def on_error(self, error: Exception, interaction: discord.Interaction) -> None:
        await interaction.response.send_message(f"Oops something went wrong!", ephemeral=True)
        traceback.print_tb(error.__traceback__)
