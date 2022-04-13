from discord import RawReactionActionEvent
from discord.ext.commands import Cog, Bot


class ReactionCog(Cog, name="Reaction Roles"):
    def __init__(self, client: Bot):
        self.client = client
        self.reroles = self.client.reroles
        self.description = "This module adds support for reaction roles."

    async def process_reaction(self, payload: RawReactionActionEvent, r_type: str = None) -> None:
        if str(payload.channel_id) in self.reroles.keys():
            print(payload.emoji.name)
            for obj in self.reroles[str(payload.channel_id)]:
                if obj[0] == payload.emoji.name:
                    print(f"{obj[0]}\n{payload.emoji.name}")
                    guild = self.client.get_guild(payload.guild_id)
                    user = await guild.fetch_member(payload.user_id)
                    role = guild.get_role(obj[1])
                    if role is None:
                        print("Invalid role ID provided for reaction role.")
                    elif r_type == "add":
                        await user.add_roles(role)
                    elif r_type == "remove":
                        await user.remove_roles(role)
                    break

    @Cog.listener()
    async def on_raw_reaction_add(self, payload: RawReactionActionEvent) -> None:
        await self.process_reaction(payload, "add")

    @Cog.listener()
    async def on_raw_reaction_remove(self, payload: RawReactionActionEvent) -> None:
        await self.process_reaction(payload, "remove")


async def setup(client: Bot):
    await client.add_cog(ReactionCog(client))
