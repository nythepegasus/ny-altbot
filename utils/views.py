import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Cog, Bot, command


class RoleDropdown(discord.ui.Select):
    def __init__(self, options: [discord.SelectOption], placeholder: str, min_values: int, max_values: int, custom_id: str):
        super().__init__(placeholder=placeholder, min_values=min_values, max_values=max_values, options=options, custom_id=custom_id)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.edit_message()
        guild: discord.Guild = interaction.guild

        roles = [guild.get_role(int(r.value)) for r in self.options]
        role = guild.get_role(int(self.values[0]))

        if self.max_values == 1:
            await interaction.followup.send(f"You chose: {role.name}.", ephemeral=True)

            await interaction.user.remove_roles(*roles)
            return await interaction.user.add_roles(role)

        remove = bool([v for v in self.values if v == "0"])

        roles = [guild.get_role(int(role)) for role in self.values if role != "0"]

        if remove:
            await interaction.user.remove_roles(*roles)
            return await interaction.followup.send("Removed all roles!", ephemeral=True)
        else:
            await interaction.user.add_roles(*roles)
            return await interaction.followup.send("You chose:\n" + '\n'.join([role.name for role in roles]), ephemeral=True)


class RoleDropdownView(discord.ui.View):
    def __init__(self, select: RoleDropdown):
        super().__init__(timeout=None)

        self.add_item(select)

