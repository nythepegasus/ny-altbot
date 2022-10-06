import asyncio
import discord
from discord import app_commands
from discord.ext.commands import Bot, Cog


class UtilCog(Cog, name="Utility"):
    def __init__(self, client: Bot):
        self.client = client

    @Cog.listener()
    async def on_thread_create(self, thread):
        if not isinstance(await self.client.fetch_channel(thread.parent_id), discord.ForumChannel):
            return

        cyr = discord.utils.get(thread.guild.text_channels, name="choose-your-roles")
        await asyncio.sleep(1)
        await thread.starter_message.pin()
        help_emb = discord.Embed(title="Help us help you!", description=f"We are going to try to help you " \
        "to the best of our abilities, but before we can do so, make sure to give us information " \
        "such as the devices you are using if you haven't taken the <#{cyr.id}> survey!\n\nAlso " \
        "please have patience, I know having an issue can be very frustrating, but all helpers " \
        "here are community volunteers, so please treat them respectfully!")
        await thread.starter_message.reply(embed=help_emb)


async def setup(client: Bot):
    await client.add_cog(UtilCog(client))
