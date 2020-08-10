from discord.utils import get


class ReactionsListener:
    def __init__(self, ranks, client):
        self.ranks = ranks
        self.client = client

    def load(self):
        self.client.event(self.on_raw_reaction_add)
        self.client.event(self.on_raw_reaction_remove)

    async def on_raw_reaction_add(self, event):
        for name_check in self.ranks:
            rank_check = self.ranks[name_check]
            if (
                rank_check["message_id"] == event.message_id
                and rank_check["emoji"] == event.emoji.name
            ):
                guild = self.get_guild(event)
                role = get(guild.roles, id=rank_check["role_id"])
                await self.get_member(guild, event).add_roles(role)
                break

    async def on_raw_reaction_remove(self, event):
        for name_check in self.ranks:
            rank_check = self.ranks[name_check]

            if (
                rank_check["message_id"] == event.message_id
                and rank_check["emoji"] == event.emoji.name
            ):
                guild = self.get_guild(event)
                role = get(guild.roles, id=rank_check["role_id"])
                await self.get_member(guild, event).remove_roles(role)
                break

    def get_guild(self, event):
        return self.client.get_guild(event.guild_id)

    def get_member(self, guild, event):
        return guild.get_member(event.user_id)
