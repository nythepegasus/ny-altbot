import ujson
import random
import discord
import datetime
from discord.ext import commands
from discord import app_commands
from discord.ext.commands import Bot, Cog

reply_switch = {"good bot": "I know I am 😌",
                "bad bot": "Am not smh 😠",
                "no you": "no you",
                "no u": "no u",
                "rip secret tunnel": "f",
                "rip jitbot": "placeholder™️"}

randoms = [
        'You are insecure',
        'lol imagine',
        'No, I don\'t think I will',
        'https://tenor.com/view/yeet-lion-king-simba-rafiki-throw-gif-16194362',
        'Excuse me, what?!',
        'Ah heck no',
        'Have you tried running it over with your car?',
        'https://tenor.com/view/stoobid-steven-he-dumb-you-so-stoobid-gif-21984392',
        'https://tenor.com/view/laugh-laughing-drink-and-laugh-drinking-laugh-rajabets-gif-22201520',
        'https://tenor.com/view/sigh-of-relief-omg-hard-case-oh-my-god-sarcastic-smile-gif-23094385',
        'https://tenor.com/view/no-bugs-bunny-nope-gif-14359850',
        'https://tenor.com/view/youre-welcome-gif-25058970',
        'https://tenor.com/view/worried-kermit-kermit-the-frog-muppets-stressed-gif-17987745'
]

class JitBotRemainsCog(Cog):
    def __init__(self, client):
        self.client = client

    def cog_check(self, ctx):
        return ctx.guild.id != 949183273383395328

    @Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.guild.id != 949183273383395328:
            return
        if message.author == self.client.user or message.content.startswith("buh!"):
            return
        try:
            return await message.reply(reply_switch[message.content.lower()])
        except KeyError:
            pass

        
        
        if "Python" in message.content or "python" in message.content.lower() and any(inc.lower() in message.content.lower() for inc in ["program", "code", "script"]):
            return await message.reply("I think you're cool 😉")
        if "can i get an amen" in message.content.lower():
            return await message.channel.send("Amen!") # <3
        if "secret tunnel" in message.content.lower():
            return await message.channel.send("rip secret tunnel")
        if "national anthem" in message.content.lower():
            return await message.channel.send("All rise for the Rust national anthem\nhttps://www.youtube.com/watch?v=LDU_Txk06tM")

        if random.random() < 0.005:
            return await message.channel.send(random.choice(randoms))


    @app_commands.command(name="status", description="Check the status of JitStreamer server.")
    async def status(self, interaction: discord.Interaction) -> None:
        jitStatus = discord.Embed(title="Server Status", color=0x00ff00)
        async with self.client.session.get('http://jitstreamer.com/census') as response:
            res = await response.text()
            data = ujson.loads(res)
            jitStatus.add_field(name="Discord Bot: 🟢", value=f"How else you seeing this?", inline=False)
            jitStatus.set_footer(text=f"JitStreamer Status v.{data['version']}")
            if response.ok:
                ret = f"Uptime:{data['uptime']}\n"
                ret += f"Registered Users:{data['clients']}\n"
                ret += f"Apps Fetched:{data['fetched']}\n"
                ret += f"Apps Launched:{data['launched']}\n"
                ret += f"Apps Attached:{data['attached']}\n"

                jitStatus.add_field(name="JitStreamer: 🟢", value=ret, inline=False)
            else:
                jitStatus.color = 0xFF0000
                jitStatus.add_field(name="JitStreamer: 🔴", value="Request timed out!!\n")
            await interaction.response.send_message(embed=jitStatus)


async def setup(client: Bot):
    await client.add_cog(JitBotRemainsCog(client))
