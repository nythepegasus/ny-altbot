import discord
from discord.ext.commands import Bot, Cog, command

class AdminCog(Cog, name="Admin"):
    def __init__(self, client):
        self.client = client
        self.description = "This module is only for the developer"

    async def cog_before_invoke(self, ctx):
        await ctx.message.delete()

    async def cog_check(self, ctx):
        return await self.client.is_owner(ctx.author)

    async def cog_command_error(self, ctx, error):
        print(ctx)
        print(error)

    @command(name="load_cog", hidden=True, help="Loads a cog.")
    async def load_cog(self, ctx, *, cog: str):
        try:
            await self.client.load_extension(cog)
        except Exception as e:
            await ctx.author.send(f"**`ERROR:`**\n {type(e).__name__} - {e}")
        else:
            await ctx.send(f"`{cog}` has been loaded!", delete_after=5)

    @command(name="unload_cog", hidden=True, help="Unloads a cog.")
    async def unload_mod(self, ctx, *, cog: str):
        if cog == "modules.admin":
            return await ctx.send("Cowardly refusing to unload admin cog.", delete_after=5)
        try:
            await self.client.unload_extension(cog)
            return await ctx.send(f"Unloaded cog: `{cog}`", delete_after=5)
        except Exception as e:
            await ctx.author.send(f"**`ERROR:`**\n {type(e).__name__} - {e}")

    @command(name="reload_cog", hidden=True, help="Reloads` a cog.")
    async def unload_cog(self, ctx, *, cog: str):
        try:
            await self.client.unload_extension(cog)
            await self.client.load_extension(cog)
            return await ctx.send(f"`{cog}` has been reloaded.", delete_after=5)
        except Exception as e:
            await ctx.author.send(f"**`ERROR:`**\n {type(e).__name__} - {e}")

async def setup(client: Bot):
    await client.add_cog(AdminCog(client))

