import discord
import traceback
import pushover as po


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
        tag = self.tag_content.value.replace("'", "''")
        section = self.tag_section.value
        db_tag = await interaction.client.db.fetch(f"SELECT * FROM tags WHERE name = '{name}'")
        if len(db_tag) != 0:
            ret_str = F"Edited tag {self.tag_name.value}"
        else:
            ret_str = f"New tag created '{self.tag_name.value}'"
        await interaction.client.db.execute(f"INSERT INTO tags "
                                            f"VALUES('{name}', '{tag}', '{section}') ON CONFLICT (name) "
                                            f"DO UPDATE SET tag = '{tag}', section = '{section}'")
        await interaction.response.send_message(ret_str, ephemeral=True)

    async def on_error(self, error: Exception, interaction: discord.Interaction) -> None:
        await interaction.response.send_message(f"Oops something went wrong!\n{error.__traceback__}", ephemeral=True)
        traceback.print_tb(error.__traceback__)


class AnnoyMeModal(discord.ui.Modal, title="What do you want to say?"):
    annoy_name = discord.ui.TextInput(
        label="What's your subject?",
        placeholder="I think you should..."
    )
    annoy_content = discord.ui.TextInput(
        label="Preferably longform complaint",
        style=discord.TextStyle.long,
        required=False
    )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        name = self.annoy_name.value
        content = self.annoy_content.value.replace("'", "''")
        db_name = await interaction.client.db.fetch(f"SELECT * FROM annoys WHERE name = '{name}'")
        all_annoys = await interaction.client.db.fetch(f"SELECT * FROM annoys")
        if len(db_name) != 0:
            ret_str = f"Edited annoyance `{name}`"
        else:
            ret_str = f"Sent annoyance `{name}`"
        await interaction.client.db.execute(f"INSERT INTO annoys "
                                            f"VALUES('{name}', '{content}')")
        await interaction.response.send_message(ret_str, ephemeral=True)

        interaction.client.pclient.send(po.Message(message=f"{content}\n - {interaction.user.display_name}#{interaction.user.discriminator}", title=name, priority=0))
        interaction.client.pclient.send(po.Glance(text=f"{content}\n - {interaction.user.display_name}#{interaction.user.discriminator}", title=name, count=len(all_annoys) + 1))

    async def on_error(self, error: Exception, interaction: discord.Interaction) -> None:
        await interaction.response.send_message(f"Oops something went wrong!\n{error.__traceback__}", ephemeral=True)
        traceback.print_tb(error.__traceback__)

