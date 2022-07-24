import re
import discord
import datetime
import wavelink
from discord import app_commands
from discord.ext.commands import Bot, Cog

URL_RE = re.compile("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")

class Music(Cog):
    def __init__(self, client: Bot):
        self.client = client

        client.loop.create_task(self.connect_nodes())

    async def connect_nodes(self):
        await self.client.wait_until_ready()

        await wavelink.NodePool.create_node(bot=self.client,
                                            host="45.33.29.114",
                                            port=2333,
                                            password="TwiNkie45?!")

    @Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node):
        print(f"Node: <{node.identifier}> is ready!")

    @Cog.listener()
    async def on_wavelink_track_end(self, vc, track, reason):
        print(f"{track} - {reason}")
        if not vc.queue.is_empty:
            new = await vc.queue.get_wait()
            await vc.play(new)
        else:
            await vc.stop()

    @app_commands.command(name="play", description="Play song through the bot.")
    async def play(self, interaction: discord.Interaction, query: str):
        if interaction.user.voice is None:
            return await interaction.response.send_message("You aren't in a voice channel!", ephemeral=True)
        if not interaction.guild.voice_client:
            vc: wavelink.Player = await interaction.user.voice.channel.connect(cls=wavelink.Player)
        else:
            vc: wavelink.Player = interaction.guild.voice_client

        if URL_RE.match(query):
            track: wavelink.YouTubeTrack = wavelink.NodePool.get_node().get_tracks(wavelink.YouTubeTrack, query)
        else:
            track: wavelink.YouTubeTrack = await wavelink.YouTubeTrack.search(query, return_first=True)

        if vc.queue.is_empty and not vc.is_playing():
            await vc.play(track)
            await interaction.response.send_message(f"**Now playing!** `{track.title}`", ephemeral=True)
        else:
            await vc.queue.put_wait(track)
            await interaction.response.send_message(f"Added `{track.title}` to the queue...", ephemeral=True)

    @app_commands.command(name="queue", description="See the current queue of songs.")
    async def queue(self, interaction: discord.Interaction, page: int = 1):
        """
        Get queue, and slice each page of the queue
        """
        if not interaction.guild.voice_client:
            vc: wavelink.Player = await interaction.user.voice.channel.connect(cls=wavelink.Player)
        else:
            vc: wavelink.Player = interaction.guild.voice_client

        cur_queue = list(vc.queue._queue)
        embed = discord.Embed(title="Current Queue")
        embed.add_field(name="Position in Queue", value=vc.queue.history.count+1, inline=True)
        embed.add_field(name="Length of Queue", value=vc.queue.count, inline=True)
        duration = str(datetime.timedelta(seconds=sum([song.length for song in cur_queue])))
        embed.add_field(name="Duration of Queue", value=duration, inline=True)
        songs = ""
        for p, song in enumerate(cur_queue[((page-1)*10):(page*10)]):
            songs += f"`{((page-1)*10+p+1):02}.` [{song.title[0:50]}]({song.info['uri']})\n"
        embed.add_field(name="**Next Up**", value=songs or "No more songs!", inline=False)
        songs_left = ((page-1)*10)+len(cur_queue[((page-1)*10):(page*10)])
        embed.set_footer(text=f"Songs {(page-1)*10+1} to {songs_left}")

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="skip", description="Skip song.")
    async def skip(self, interaction: discord.Interaction):
        if not interaction.guild.voice_client:
            vc: wavelink.Player = await interaction.user.voice.channel.connect(cls=wavelink.Player)
        else:
            vc: wavelink.Player = interaction.guild.voice_client

        if not vc.is_playing():
            return await interaction.response.send_message("Not currently playing anything!", ephemeral=True)
        else:
            await vc.stop()
            return await interaction.response.send_message(f"Skipped song, playing `{vc.queue[0] or vc.queue}`")

async def setup(client: Bot):
    await client.add_cog(Music(client))

