import discord
from discord.ext.commands import Cog, Bot, command


class RoleDropdown(discord.ui.Select):
    def __init__(self, placeholder: str, options: list[discord.SelectOption], min_values: int, max_values: int, custom_id: str):
        super().__init__(placeholder=placeholder, min_values=min_values, max_values=max_values, options=options, custom_id=custom_id)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.edit_message()
        guild: discord.Guild = interaction.guild

        roles = [guild.get_role(int(r.value)) for r in self.options]
        role = guild.get_role(int(self.values[0]))

        await interaction.followup.send(f"You chose: {role.name}.", ephemeral=True)

        await interaction.user.remove_roles(*roles)
        await interaction.user.add_roles(role)


class JitRoleDropdown(RoleDropdown):
    def __init__(self):
        options = [
            discord.SelectOption(label="SideStore Tester", description="Test out new features from the devs! Hands on changes/feedback *with* the devs!", emoji="🚀", value="1051087638389588050"),
            discord.SelectOption(label="SideStore Releases", description="Get pinged every time SideStore is updated, or there's news from the team.", emoji="🎉", value="1051087502229897216"),
            discord.SelectOption(label="SideStore Feedback", description="Get pinged every time a SideStore dev wants specific information, but not necessarily test.", emoji="📋", value="1051087707201347624")
        ]

        super().__init__(placeholder="Choose your ping status: ", min_values=1, max_values=1, options=options, custom_id="dropdown:jit_ping")



class RoleDropdownView(discord.ui.View):
    def __init__(self, select: discord.ui.Select):
        super().__init__(timeout=None)

        self.add_item(select())



class JitRoleCog(Cog, name="JitStreamer Reaction Roles"):
    def __init__(self, client: Bot):
        self.client = client
        self.description = "This module adds support for reaction roles."
        self.client.add_view(RoleDropdownView(JitRoleDropdown))

    async def cog_before_invoke(self, ctx):
        await ctx.message.delete()

    async def cog_check(self, ctx):
        return await self.client.is_owner(ctx.author)

    async def cog_command_error(self, ctx, error):
        print(ctx)
        print(error)

    @command(name="prep-jit-roles")
    async def prepare_reroles(self, ctx):
        jitEmbed = discord.Embed(color=0xa038ef, title="Self Roles", description="Come get your self-roles here so we can feel better about pinging you! :D")
        await ctx.channel.send(embed=jitEmbed, view=RoleDropdownView(JitRoleDropdown))


async def setup(client: Bot):
    await client.add_cog(JitRoleCog(client))
