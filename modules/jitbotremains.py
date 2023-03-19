import ujson
import random
import discord
import datetime
from discord.ext import commands
from discord import app_commands
from discord.ext.commands import Bot, Cog
from utils.modals import AnnoyMeModal

reply_switch = {"good bot": "I know I am 😌",
                "bad bot": "Am not smh 😠",
                "no you": "no you",
                "no u": "no u",
                "rip secret tunnel": "f",
                "rip jitbot": "placeholder™️"}

rules = {
    "r1": "__**No Piracy!**__\nThis includes asking where to download ROMs and telling people where to find them (besides your console of course).",
    "r2": "__**Keep swearing minimal**__\nLet's keep our community clean, please. While some swearing may be situationally appropriate, blatant dirty language will not be tolerated.",
    "r3": "__**Be considerate of others**__\nWe are all just learning here, and come from all experiences. Please be respectful of others' ideas and questions.",
    "r4": "__**Absolutely no discrimination**__\nDiscrimination against a person due to race, gender, religion or orientation will be served with an immediate and permanent ban. We will not allow hate in our community.",
    "r5": "__**Python**__\nAbsolutely programming in Python, as it is pure magic and idiomatic beauty. Garbage programmers care about garbage collectors.",
    "r6": "__**Keep it G rated**__\nPlease do not post content that you would be embarrassed showing your mother. This includes porn, gore and stuff that you would get banned at work for having.",
    "r7": "__**No spam**__\nThis includes sending the same message over and over, pinging mass amounts of people or crossposting. This may result in a mute and then a ban.",
    "r8": "__**No excessive pinging**__\nPinging staff that you are not actively having a conversation with may result in a mute and kick. You do not have the right to be helped at all times.",
    "r34": "😳😳😳\n😳😳😳",
    "r69": "haha funny number\nhaha funny number"
}

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
        if message.guild is not None and message.guild.id != 949183273383395328:
            return
        if message.author == self.client.user or message.content.startswith("buh!"):
            return
        try:
            return await message.reply(reply_switch[message.content.lower()])
        except KeyError:
            pass

        try:
            rule = rules[message.content.lower()].split("\n")
            ruleEmbed = discord.Embed(title=rule[0], description=rule[1], color=0x0000FF)
            await message.channel.send(embed=ruleEmbed)
            return await message.delete()
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
                ret = f"Uptime: {datetime.timedelta(seconds=data['uptime'])}\n"
                ret += f"Registered Users: {data['clients']}\n"
                ret += f"Apps Fetched: {data['fetched']}\n"
                ret += f"Apps Launched: {data['launched']}\n"
                ret += f"Apps Attached: {data['attached']}\n"

                jitStatus.add_field(name="JitStreamer: 🟢", value=ret, inline=False)
            else:
                jitStatus.color = 0xFF0000
                jitStatus.add_field(name="JitStreamer: 🔴", value="Request timed out!!\n")
            await interaction.response.send_message(embed=jitStatus)

    @app_commands.command(name="annoyme", description="Send me (Nythepegasus) a message from you!")
    async def annoyme(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_modal(AnnoyMeModal())



async def setup(client: Bot):
    await client.add_cog(JitBotRemainsCog(client))
