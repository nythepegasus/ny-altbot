import discord
from discord.ext.commands import Cog, Bot
from discord import RawReactionActionEvent, app_commands


class iPhoneDropdown(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="iPhone 5S", description=""),
            discord.SelectOption(label="iPhone 6/Plus", description=""),
            discord.SelectOption(label="iPhone 7/Plus", description=""),
            discord.SelectOption(label="iPhone X/8/Plus", description=""),
            discord.SelectOption(label="iPhone SE (2016)", description=""),
            discord.SelectOption(label="iPhone XR/XS/Max", description=""),
            discord.SelectOption(label="iPhone 11/Pro", description=""),
            discord.SelectOption(label="iPhone SE (2020)", description=""),
            discord.SelectOption(label="iPhone 12/Mini/Pro/Max", description=""),
            discord.SelectOption(label="iPhone 13/Mini", description=""),
            discord.SelectOption(label="iPhone SE (2022)", description="")
        ]

        super().__init__(placeholder="Choose your iPhone model", min_values=1, max_values=1, options=options, custom_id="dropdown:iphone")

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Your iPhone model is {self.values[0]}.", ephemeral=True)


class iOSDropdown(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="<= iOS 12", description=""),
            discord.SelectOption(label="iOS 13.0 - 13.3.1", description=""),
            discord.SelectOption(label="iOS 13.3.1 - 13.7", description=""),
            discord.SelectOption(label="iOS 14.0 - 14.3", description=""),
            discord.SelectOption(label="iOS 14.3 - 14.8.1", description=""),
            discord.SelectOption(label="iOS 15.0 - 15.1.1", description=""),
            discord.SelectOption(label="iOS 15.2+", description=""),
            discord.SelectOption(label="iOS 16+", description="")
        ]
        super().__init__(placeholder="Choose your iOS version", min_values=1, max_values=1, options=options, custom_id="dropdown:ios")

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Your iOS version is {self.values[0]}.", ephemeral=True)


class RoleDropdownView(discord.ui.View):
    def __init__(self, select: discord.ui.Select):
        super().__init__(timeout=None)

        self.add_item(select())


class ReactionCog(Cog, name="Reaction Roles"):
    def __init__(self, client: Bot):
        self.client = client
        self.description = "This module adds support for reaction roles."
        self.client.add_view(RoleDropdownView(iOSDropdown))
        self.client.add_view(RoleDropdownView(iPhoneDropdown))

    @app_commands.command(name="prepare-roles", description="Send dropdowns to channel.")
    async def prepare_reroles(self, interaction: discord.Interaction):
        await interaction.response.send_message("Sent messages", ephemeral=True)
        await interaction.channel.send("Pick your iPhone model:", view=RoleDropdownView(iPhoneDropdown))
        await interaction.channel.send("Pick your iOS version:", view=RoleDropdownView(iOSDropdown))

    async def process_reaction(self, payload: RawReactionActionEvent, r_type: str = None) -> None:
        if payload.user_id == self.client.user.id:
            return
        rerole = await self.client.db.fetchrow(f"SELECT * FROM react_roles WHERE emoji = '{payload.emoji.name}' "
                                               f"AND guild_id = {payload.guild_id}")
        if rerole is not None:
            guild = self.client.get_guild(rerole["guild_id"])
            role = guild.get_role(rerole["role_id"])
            user = await guild.fetch_member(payload.user_id)
            if r_type == "remove":
                return await user.remove_roles(role)
            if rerole["exclusive"]:
                channel = guild.get_channel(rerole["channel_id"])
                all_roles = await self.client.db.fetch("SELECT * FROM react_roles WHERE exclusive = "
                                                       f"'{rerole['exclusive']}' AND guild_id = {payload.guild_id}")
                try:
                    rem = [x for x in all_roles if x["role_id"] in [r.id for r in user.roles]][0]
                    message = await channel.fetch_message(rem["message_id"])
                    await message.remove_reaction(rem["emoji"], user)
                    rem_role = guild.get_role(rem["role_id"])
                    await user.remove_roles(rem_role)
                except IndexError:
                    pass
            return await user.add_roles(role)

    @Cog.listener()
    async def on_raw_reaction_add(self, payload: RawReactionActionEvent) -> None:
        await self.process_reaction(payload, "add")

    @Cog.listener()
    async def on_raw_reaction_remove(self, payload: RawReactionActionEvent) -> None:
        await self.process_reaction(payload, "remove")

    @app_commands.command(name="add-rerole", description="Create a reaction role")
    @app_commands.describe(message_id="The message id to add reaction role to.")
    @app_commands.describe(channel="The channel that the message is in.")
    @app_commands.describe(emoji="The emoji to add as the reaction role to the message.")
    @app_commands.describe(role="The role to relate to the emoji")
    @app_commands.describe(exclusive="Which group the role should be exclusive to. (Optional)")
    @app_commands.checks.has_role("Mods")
    async def add_rerole(self, interaction: discord.Interaction, message_id: str,
                         channel: app_commands.AppCommandChannel, emoji: str, role: discord.Role,
                         exclusive: str = ""):
        channel = await channel.fetch()
        msg = await channel.fetch_message(int(message_id))
        await msg.add_reaction(emoji)

        query = f"INSERT INTO react_roles VALUES({channel.guild.id}, {channel.id}, {message_id}, {role.id}, '{emoji}'"
        ret_msg = f"Inserted {emoji} as role '{role.name}'"
        if exclusive != "":
            query += f", '{exclusive}'"
            ret_msg += f" with exclusivity '{exclusive}'"
        query += ")"
        ret_msg += "."
        await self.client.db.execute(query)

        await interaction.response.send_message(ret_msg, ephemeral=True)

    @app_commands.command(name="remove-rerole", description="Delete reaction role. (NOT RECOMMENDED)")
    @app_commands.describe(role="The role to remove as a reaction role.")
    @app_commands.checks.has_role("Mods")
    async def remove_rerole(self, interaction: discord.Interaction, role: str):
        t_role = await self.client.db.fetchrow(f"SELECT * FROM react_roles WHERE guild_id = {interaction.guild_id} "
                                               f"AND role_id = {role}")
        await self.client.db.execute(f"DELETE FROM react_roles WHERE guild_id = {interaction.guild_id} "
                                     f"AND role_id = {role}")
        role_name = interaction.guild.get_role(int(role))
        ret_str = f"Deleted reaction role with emoji '{t_role['emoji']}' and name '{role_name}'"
        ret_str += "\n\n***NOTE***: The reaction role has been removed from the database, but people with said role " \
                   "will still have the role, and their reactions will still be on the original message. You will " \
                   "have to do manual clean up if you want to get rid of the role completely. This is mostly " \
                   "for testing, and cleaning up the database."

        await interaction.response.send_message(ret_str, ephemeral=True)

    @remove_rerole.autocomplete("role")
    async def delete_role_ac(self, interaction: discord.Interaction, _: str) -> list[app_commands.Choice[str]]:
        roles = await self.client.db.fetch(f"SELECT * FROM react_roles WHERE guild_id = {interaction.guild_id}"
                                           f" LIMIT 25")
        all_roles = [interaction.guild.get_role(r["role_id"]) for r in roles]
        return [app_commands.Choice(name=r.name, value=str(r.id)) for r in all_roles]

    @add_rerole.autocomplete("exclusive")
    async def excl_ac(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
        excl = await self.client.db.fetch("SELECT DISTINCT exclusive FROM react_roles WHERE exclusive LIKE "
                                          f"'{current}%' AND guild_id = {interaction.guild_id} LIMIT 25")
        return [app_commands.Choice(name=e["exclusive"], value=e["exclusive"]) for e in excl]


async def setup(client: Bot):
    await client.add_cog(ReactionCog(client))
