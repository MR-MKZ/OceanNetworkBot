import discord
from discord.ext import commands
from discord.ext.commands.errors import MissingPermissions



class UserInfo(commands.Cog):
    def __init__(self, client):
        self.client = client

    
    @commands.Cog.listener()
    async def on_ready(self):
        print("-----\nUserInfo loaded")
    


    @commands.command(name="userinfo", description="For see informations of a member", aliases=["member_info", "meminfo", "uinfo"])
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def userinfo(self, ctx, member: discord.Member=None):

        if member is None:
            member = ctx.author
        else:
            member = member

        embed = discord.Embed(
            colour=member.color, timestamp=ctx.message.created_at
        )

        roles = [role for role in member.roles]

        embed.set_author(name=f"User Info - {member}")
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f"Request by {ctx.author}", icon_url=ctx.author.avatar_url)

        embed.add_field(name="ID: ", value=member.id)
        embed.add_field(name="Guild name:", value=member.display_name)
        embed.add_field(name="Account created at:", value=member.created_at.strftime("%a %#d %B %Y, %I:%M %p"))
        embed.add_field(name="Joined at server:", value=member.joined_at.strftime("%a %#d %B %Y, %I:%M %p"))
        embed.add_field(name=f"Roles: ({len(roles)})", value=" ".join([role.mention for role in roles]))
        embed.add_field(name="Top role:", value=member.top_role.mention)

        embed.add_field(name="Bot?", value=member.bot)

        await ctx.send(embed=embed)
    

    @userinfo.error
    async def userinfo_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.reply("You don't have permission to see userinfo")
        else:
            raise error





def setup(client):
    client.add_cog(UserInfo(client))