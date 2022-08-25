from discord.ext.commands import Bot, Cog


class FunCog(Cog, description="Fun commands."):
    def __init__(self, client: Bot):
        self.client = client
        self.session = self.client.session


async def setup(client: Bot):
    await client.add_cog(FunCog(client))
