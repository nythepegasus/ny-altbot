import discord
from discord import Interaction, SelectOption, TextChannel, Role
from discord import app_commands as ac
from discord.ext.commands import Cog, Bot
from utils.views import RoleDropdown, RoleDropdownView


class ReactionCog(Cog, name="Reaction Roles"):
    def __init__(self, client: Bot):
        self.client = client
        self.db = client.db
        self.description = "This module adds support for reaction roles."

    @ac.command(name="add-role-menu", description="Add a custom menu to the bot")
    @ac.describe(name="The custom name to use for the menu")
    @ac.describe(max_choice="The maximum amount of roles users can select")
    @ac.describe(placeholder="The placeholder inside the menu")
    @ac.checks.has_any_role("Mods", "Moderator", "Helpers", "Helper")
    async def add_role_menu(self, interaction: Interaction, name: str, max_choice: int = 1, placeholder: str = None):
        query = "INSERT INTO role_menus (name, placeholder, guild, max_choice) VALUES ($1, $2, $3, $4)"
        await self.db.execute(query, name, placeholder, interaction.guild.id, max_choice)
        await interaction.response.send_message(f"Registered {name} into list of menus!", ephemeral=True)

    @ac.command(name="del-role-menu", description="Delete a custom menu from the bot")
    @ac.describe(menu="The menu to delete")
    @ac.checks.has_any_role("Mods", "Moderator", "Helpers", "Helper")
    async def del_role_menu(self, interaction: Interaction, menu: int):
        menu_name = await self.db.fetchval("SELECT name FROM role_menus WHERE id = $1", menu)
        await self.db.execute("DELETE FROM role_menus WHERE id = $1", menu)
        await interaction.response.send_message(f"Deleted {menu_name} from list of menus!", ephemeral=True)

    @ac.command(name="edit-role-menu", description="Edit a custom menu from the bot")
    @ac.describe(menu="The menu to edit")
    @ac.describe(max_choice="The maximum amount of roles users can select")
    @ac.describe(placeholder="The placeholder inside the menu")
    @ac.describe(name="What you would like to rename the menu to")
    @ac.checks.has_any_role("Mods", "Moderator", "Helpers", "Helper")
    async def edit_role_menu(self, interaction: Interaction, menu: int, max_choice: int = 1, placeholder: str = None, name: str = None):
        menu_name = await self.db.fetchval("SELECT name FROM role_menus WHERE id = $1", menu)
        query = "UPDATE role_menus "
        query += "SET name = $1, " if name is not None else "SET "
        query += " placeholder = $2, guild = $3, max_choice = $4 "
        query += "WHERE id = $5"
        await self.db.execute(query, name, placeholder, interaction.guild.id, max_choice, menu)
        await self.update_menu_messages(menu)
        await interaction.response.send_message(f"Updated {menu_name}!", ephemeral=True)

    @ac.command(name="add-role-to-menu", description="Add a role to a role menu registered to the bot")
    @ac.describe(role="The role to add to the menu")
    @ac.describe(menu="The menu to add the role to")
    @ac.describe(emoji="The emoji to represent this role")
    @ac.describe(description="The description of the role inside of the menu")
    @ac.checks.has_any_role("Mods", "Moderator", "Helpers", "Helper")
    async def add_role_to_menu(self, interaction: Interaction, role: Role, menu: int, description: str = None, emoji: str = None):
        query = "INSERT INTO roles (id, name, guild, menu, description, emoji) VALUES ($1, $2, $3, $4, $5, $6)" \
                "ON CONFLICT (id) DO UPDATE SET menu = $4"
        await self.db.execute(query, role.id, role.name, role.guild.id, menu, description, emoji)
        menu_name = await self.db.fetchval("SELECT name FROM role_menus WHERE id = $1", menu)
        await interaction.response.send_message(f"Registered {role.name} into {menu_name}!", ephemeral=True)
        await self.update_menu_messages(menu)

    @ac.command(name="del-role-from-menu", description="Delete a role from a menu registered to the bot")
    @ac.describe(role="The role to remove from the menu")
    @ac.describe(menu="The menu to remove the role from")
    @ac.checks.has_any_role("Mods", "Moderator", "Helpers", "Helper")
    async def del_role_fr_menu(self, interaction: Interaction, role: str, menu: int):
        role = self.client.get_guild(interaction.guild.id).get_role(int(role))
        await self.db.execute("UPDATE roles SET menu = NULL WHERE id = $1", role.id)
        menu_name = await self.db.fetchval("SELECT name FROM role_menus WHERE id = $1", menu)
        await interaction.response.send_message(f"Deleted {role.name} from {menu_name}!", ephemeral=True)
        await self.update_menu_messages(menu)

    @ac.command(name="edit-role-for-menu", description="Edit a role that is already registered to a menu.")
    @ac.checks.has_any_role("Mods", "Moderator", "Helpers", "Helper")
    async def edit_role_for_menu(self, interaction: Interaction, role: str, description: str = None, emoji: str = None):
        role = self.client.get_guild(interaction.guild.id).get_role(int(role))
        await self.db.execute("UPDATE roles SET description = $1, emoji = $2 WHERE id = $3", description, emoji, role.id)
        await interaction.response.send_message(f"Updated {role.name}!", ephemeral=True)
        await self.update_menu_messages(menu)

    @ac.command(name="send-role-menu", description="Send a role menu to a channel")
    @ac.describe(menu="The role menu to send")
    @ac.describe(channel="The channel to send the menu to")
    @ac.describe(message="A message to attach to the sent message")
    @ac.checks.has_any_role("Mods", "Moderator", "Helpers", "Helper")
    async def send_menu(self, interaction: Interaction, menu: int, channel: TextChannel, message: str = None):
        roles = await self.db.fetch("SELECT * FROM role_menu_info WHERE mid = $1", menu)
        r = roles[0]
        choices = [SelectOption(label=role["rname"], description=role["rdesc"], value=role["rid"], emoji=role["remoji"]) for role in roles]
        if r["mmchoice"] > 1:
            choices.append(SelectOption(label="Remove Roles",
                                                description="This removes all listed roles above, so that you can rechoose which roles you actually want.", 
                                                value="0"))
        view = RoleDropdownView(RoleDropdown(options=choices, placeholder=r["mplaceholder"], min_values=1,
                                             max_values=r["mmchoice"], custom_id=str(r["mid"])))

        msg = await channel.send(view=view)
        await self.db.execute("INSERT INTO menu_messages (id, channel, menu) VALUES ($1, $2, $3)", msg.id, channel.id, r["mid"])

        await interaction.response.send_message(f"Sent {r['mname']} to {channel.name}!", ephemeral=True)

    @del_role_fr_menu.autocomplete("role")
    @edit_role_for_menu.autocomplete("role")
    async def role_ac(self, interaction: Interaction, current: str) -> list[ac.Choice[int]]:
        query = "SELECT * FROM roles WHERE name ILIKE $1 AND guild = $2 LIMIT 25"
        roles = await self.db.fetch(query, f"{current}%", interaction.guild.id)
        return [ac.Choice(name=role["name"], value=str(role["id"])) for role in roles]

    @add_role_to_menu.autocomplete("menu")
    @edit_role_menu.autocomplete("menu")
    @del_role_menu.autocomplete("menu")
    @del_role_fr_menu.autocomplete("menu")
    @send_menu.autocomplete("menu")
    async def menu_ac(self, interaction: Interaction, current: str) -> list[ac.Choice[int]]:
        query = "SELECT * FROM role_menus WHERE name ILIKE $1 AND guild = $2 LIMIT 25"
        menus = await self.db.fetch(query, f"{current}%", interaction.guild.id)
        return [ac.Choice(name=menu["name"], value=menu["id"]) for menu in menus]

    async def update_menu_messages(self, menu):
        roles = await self.db.fetch("SELECT * FROM role_menu_info WHERE mid = $1", menu)
        r = roles[0]
        choices = [SelectOption(label=role["rname"], description=role["rdesc"], value=role["rid"], emoji=role["remoji"]) for role in roles]
        if r["mmchoice"] > 1:
            choices.append(SelectOption(label="Remove Roles",
                                                description="This removes all listed roles above, so that you can rechoose which roles you actually want.", 
                                                value="0"))
        view = RoleDropdownView(RoleDropdown(options=choices, placeholder=r["mplaceholder"], min_values=1,
                                             max_values=r["mmchoice"], custom_id=str(r["mid"])))
        self.client.add_view(view)

        msgs = await self.db.fetch("SELECT * FROM menu_messages WHERE menu = $1", menu)
        for msg in msgs:
            channel = self.client.get_guild(r["mguild"]).get_channel(int(msg["channel"]))
            try:
                m = await channel.fetch_message(msg["id"])
                await m.edit(view=view)
            except:
                print("RIP message!")

    @Cog.listener()
    async def on_raw_message_delete(self, message):
        if message.guild_id:
            await self.db.execute("DELETE FROM menu_messages WHERE id = $1", message.message_id)

    @Cog.listener()
    async def on_guild_role_delete(self, role):
        await self.db.execute("DELETE FROM roles WHERE id = $1", role.id)

    @Cog.listener()
    async def on_guild_role_update(self, before, after):
        await self.db.execute("UPDATE roles SET id = $1, name = $2 WHERE id = $3", after.id, after.name, before.id)


async def setup(client: Bot):
    await client.add_cog(ReactionCog(client))
