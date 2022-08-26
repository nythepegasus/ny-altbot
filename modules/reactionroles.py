import discord
from discord.ext.commands import Cog, Bot, command

# TODO: Generate values and such from DB, for now everything is hardcoded


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


class iPhoneDropdown(RoleDropdown):
    def __init__(self):
        options = [
            discord.SelectOption(label="iPhone 5S", description="", value="973604854259908608"),
            discord.SelectOption(label="iPhone 6/Plus", description="", value="973604873499205632"),
            discord.SelectOption(label="iPhone 7/Plus", description="", value="973604885515862096"),
            discord.SelectOption(label="iPhone X/8/Plus", description="", value="973604889664053268"),
            discord.SelectOption(label="iPhone SE (2016)", description="", value="973604895909351464"),
            discord.SelectOption(label="iPhone XR/XS/Max", description="", value="973604901429080074"),
            discord.SelectOption(label="iPhone 11/Pro", description="", value="973604910841077801"),
            discord.SelectOption(label="iPhone SE (2020)", description="", value="973604938754170900"),
            discord.SelectOption(label="iPhone 12/Mini/Pro/Max", description="", value="973604942503895050"),
            discord.SelectOption(label="iPhone 13/Mini", description="", value="973604948480770100"),
            discord.SelectOption(label="iPhone SE (2022)", description="", value="973604945603473418")
        ]

        super().__init__(placeholder="Choose your iPhone model", min_values=1, max_values=1, options=options, custom_id="dropdown:iphone")


class iOSDropdown(RoleDropdown):
    def __init__(self):
        options = [
            discord.SelectOption(label="<= iOS 12", description="", value="719312337470750810"),
            discord.SelectOption(label="iOS 13.0 - 13.3.1", description="", value="973604190066729010"),
            discord.SelectOption(label="iOS 13.4 - 13.7", description="", value="847304060544745492"),
            discord.SelectOption(label="iOS 14.0 - 14.3", description="", value="973603795726635029"),
            discord.SelectOption(label="iOS 14.3 - 14.8.1", description="", value="973603902224207913"),
            discord.SelectOption(label="iOS 15.0 - 15.1.1", description="", value="956247474081767435"),
            discord.SelectOption(label="iOS 15.2+", description="", value="973603653652992122"),
            discord.SelectOption(label="iOS 16+", description="", value="1012525211553374269")
        ]
        super().__init__(placeholder="Choose your iOS version", min_values=1, max_values=1, options=options, custom_id="dropdown:ios")


class JailbrokenDropdown(RoleDropdown):
    def __init__(self):
        options = [
            discord.SelectOption(label="Stock iOS", emoji=u"🪖", description="Nah, I always stay on the latest stock firmware", value="847474574412218409"),
            discord.SelectOption(label="Jailbroken", emoji=u"🛠", description="Yup, I love myself some good JB tweaks", value="719369094297812993")
        ]
        super().__init__(placeholder="Are you jailbroken?", min_values=1, max_values=1, options=options, custom_id="dropdown:jb")


class SkillDropdown(RoleDropdown):
    def __init__(self):
        options = [
            discord.SelectOption(label="iOS Beginner", emoji=u"🆕", description="I'm more of a beginner at sideloading", value="847507324842147860"),
            discord.SelectOption(label="Casual User", emoji=u"🦾", description="I'm a power user but don't get into dev stuff", value="847517763966205974"),
            discord.SelectOption(label="iOS Veteran", emoji=u"👨‍💻", description="I do at least some dev / tinkering with iOS", value="847507222934061087")
        ]
        super().__init__(placeholder="Choose your skill", min_values=1, max_values=1, options=options, custom_id="dropdown:skill")


class ComputerDropdown(RoleDropdown):
    def __init__(self):
        options = [
            discord.SelectOption(label="<= macOS 10.15", emoji=u"🦴", description="", value="847303756176424971"),
            discord.SelectOption(label="macOS 11", emoji=u"🍏", description="", value="973603015498010624"),
            discord.SelectOption(label="macOS 12", emoji=u"🍎", description="", value="956248314800656485"),
            discord.SelectOption(label="macOS 13", emoji=u"🍎", description="", value="1012525153864929320"),
            discord.SelectOption(label="<= Windows 8", emoji=u"\u231B", description="", value="847472981130084382"),
            discord.SelectOption(label="Windows 10", emoji=u"🪟", description="", value="973603196964589658"),
            discord.SelectOption(label="Windows 11", emoji=u"🖼", description="", value="956247720631357601")
        ]
        super().__init__(placeholder="Choose your MAIN computer's OS", min_values=1, max_values=1, options=options, custom_id="dropdown:computer")


class DevicesDropdown(RoleDropdown):
    def __init__(self):
        options = [
            discord.SelectOption(label="iPad", emoji=u"📝", description="", value="847726262583951380"),
            discord.SelectOption(label="TV", emoji=u"📺", description="", value="847604362313990164"),
            discord.SelectOption(label="Mac", emoji=u"💻", description="", value="1012525470908153901"),
            discord.SelectOption(label="Remove Roles", description="This removes all listed roles above, so that you can rechoose which roles you actually want.", value="0")
        ]
        super().__init__(placeholder="Choose devices you want to see support for", min_values=1, max_values=4, options=options, custom_id="dropdown:devices")

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.edit_message()

        remove = bool([v for v in self.values if v == "0"])

        guild: discord.Guild = interaction.guild
        roles = [guild.get_role(int(role)) for role in self.values]

        if remove:
            roles = [guild.get_role(int(role.value)) for role in self.options if role.value != "0"]
            await interaction.user.remove_roles(*roles)
            return await interaction.followup.send("Removed all roles!", ephemeral=True)
        else:
            await interaction.user.add_roles(*roles)
            return await interaction.followup.send("You chose:\n" + '\n'.join([role.name for role in roles]), ephemeral=True)


class PingDropdown(RoleDropdown):
    def __init__(self):
        options = [
            discord.SelectOption(label="AltStore Notifications", emoji=discord.PartialEmoji.from_str("<:AltStore:849473203599704064>"), description="Get notifications whenever AltStore updates!", value="944733407966015531"),
            discord.SelectOption(label="Delta Notifications", emoji=discord.PartialEmoji.from_str("<:Delta:849473203742048266>"), description="Get notifications whenever Delta updates!", value="944733560156348436"),
            discord.SelectOption(label="Potential Collaborator", emoji="👨‍🔧", description="Yeah, I could maybe contribute sometime", value="847506847752519720"),
            discord.SelectOption(label="Tester", description="Get pinged whenever something relating to AltStore/Delta needs testing", value="847161591653072927"),
            discord.SelectOption(label="Skin Tester", description="Get pinged whenever new Delta skins need testing", value="1012525070507331615"),
            discord.SelectOption(label="Remove Ping Roles", description="This removes all ping roles, so that you can rechoose which roles you actually want.", value="0")
        ]
        super().__init__(placeholder="Choose based on when you want to be pinged", min_values=1, max_values=6, options=options, custom_id="dropdown:ping")

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.edit_message()

        remove = bool([v for v in self.values if v == "0"])

        guild: discord.Guild = interaction.guild
        roles = [guild.get_role(int(role)) for role in self.values]

        if remove:
            roles = [guild.get_role(int(role.value)) for role in self.options if role.value != "0"]
            await interaction.followup.send("Removed all ping roles!", ephemeral=True)
            await interaction.user.remove_roles(*roles)
        else:
            await interaction.followup.send("You chose:\n" + '\n'.join([role.name for role in roles]), ephemeral=True)
            await interaction.user.add_roles(*roles)


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
        self.client.add_view(RoleDropdownView(JailbrokenDropdown))
        self.client.add_view(RoleDropdownView(SkillDropdown))
        self.client.add_view(RoleDropdownView(ComputerDropdown))
        self.client.add_view(RoleDropdownView(DevicesDropdown))
        self.client.add_view(RoleDropdownView(PingDropdown))

    async def cog_before_invoke(self, ctx):
        await ctx.message.delete()

    async def cog_check(self, ctx):
        return await self.client.is_owner(ctx.author)

    async def cog_command_error(self, ctx, error):
        print(ctx)
        print(error)

    @command(name="prep-roles")
    async def prepare_reroles(self, ctx):
        await ctx.channel.send("Pick your iPhone model:", view=RoleDropdownView(iPhoneDropdown))
        await ctx.channel.send("Pick your iOS version:", view=RoleDropdownView(iOSDropdown))
        await ctx.channel.send("Are you jailbroken:", view=RoleDropdownView(JailbrokenDropdown))
        await ctx.channel.send("What would you consider your computer skill level:", view=RoleDropdownView(SkillDropdown))
        await ctx.channel.send("Which computer OS do you use on your **MAIN** computer for AltServer:", view=RoleDropdownView(ComputerDropdown))
        await ctx.channel.send("Which devices would you like to see AltStore/Delta on next:", view=RoleDropdownView(DevicesDropdown))
        await ctx.channel.send("Choose the following that apply: ", view=RoleDropdownView(PingDropdown))


async def setup(client: Bot):
    await client.add_cog(ReactionCog(client))
