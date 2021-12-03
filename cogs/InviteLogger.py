import discord
import DiscordUtils
from bot_config.config import GOODBYE_MESSAGE
from discord.ext import commands



class InviteLogger(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.tracker = DiscordUtils.InviteTracker(client)
    

    @commands.Cog.listener()
    async def on_ready(self):
        print("-----\nInviteLogger loaded")
        await self.tracker.cache_invites()

    @commands.Cog.listener()
    async def on_invite_create(self, invite):
        await self.tracker.update_invite_cache(invite)

    @commands.Cog.listener()
    async def on_invite_delete(self, invite):
        await self.tracker.remove_invite_cache(invite)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        await self.tracker.update_guild_cache(guild)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        await self.tracker.remove_guild_cache(guild)

    @commands.Cog.listener()
    async def on_member_join(self, member):

        global inviter
        inviter = await self.tracker.fetch_inviter(member)
        data = await self.client.invites.find_by_custom(
            {"guild_id": member.guild.id, "inviter_id": inviter.id}
        )
        if data is None:
            data = {
                "guild_id": member.guild.id,
                "inviter_id": inviter.id,
                "count": 0,
                "invited_users": []
            }

        data["count"] += 1
        data["invited_users"].append(member.id)
        await self.client.invites.upsert_custom(
            {"guild_id": member.guild.id, "inviter_id": inviter.id}, data
        )

        channel = discord.utils.get(member.guild.text_channels, name="bot-commands")

        embed = discord.Embed(
            title=f"Welcome {member.display_name}!",
            description=f"Hello, I hope you have a good time on our server, if you need help, visit the site or contact some staff\nسلام، امیدوارم اوقات خوبی را در سرور ما داشته باشید، اگر به کمک نیاز دارید به سایت مراجعه کنید و یا با برخی از کارکنان تماس بگیرید\n\nInvited by: {inviter.mention}\nInvites: {data['count']}",
            timestamp=member.joined_at
        )
        embed.set_thumbnail(url=f"{member.avatar_url}")
        embed.set_footer(text=member.guild, icon_url=member.guild.icon_url)
        await channel.send(embed=embed)
    

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        inviter = await self.tracker.fetch_inviter(member)
        channel = discord.utils.get(member.guild.text_channels, name="bot-commands")
        data = await self.client.invites.find_by_custom(
            {"guild_id": member.guild.id, "inviter_id": inviter.id}
        )
        try:
            data["count"] -= 1
            data["invited_users"].remove(member.id)
            await self.client.invites.upsert_custom(
                {"guild_id": member.guild.id, "inviter_id": inviter.id}, data
            )
        except:
            pass
        embed = discord.Embed(
            title=f"good bye {member.display_name}",
            description=GOODBYE_MESSAGE
        )
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=member.guild, icon_url=member.guild.icon_url)
        await channel.send(embed=embed)
    

    @commands.command(name="invites", description="For see invited members from you")
    @commands.guild_only()
    async def invites(self, ctx):
        inviterr = ctx.message.author
        data = await self.client.invites.find_by_custom(
            {"guild_id": ctx.guild.id, "inviter_id": inviterr.id}
        )

        embed = discord.Embed(
            title=f"Invites status",
            colour=0xFFC901
        )
        try:
            count = data["count"]
            users = data["invited_users"]
            embed.add_field(name="Invited Users", value='\n'.join(f"<@!{i}>" for i in users), inline=True)
            embed.add_field(name="Invited Count", value=count, inline=True)
            embed.set_thumbnail(url=ctx.message.author.avatar_url)
            embed.set_footer(text=f"Requested by {ctx.message.author.display_name}")
            await ctx.reply(embed=embed)
        except:
            await ctx.reply("You didn't invite any users!")




def setup(client):
    client.add_cog(InviteLogger(client))
