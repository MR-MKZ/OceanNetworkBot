import discord
from discord.ext import commands
from discord.ext.commands.errors import MissingPermissions



class Ban_Unban(commands.Cog):
    def __init__(self, client):
        self.client = client
    

    @commands.Cog.listener()
    async def on_ready(self):
        print("-----\nban loaded")



    @commands.command(name="ban", description="For ban members")
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member=None, *, reason=None):
        if reason is None:
            reason = "For no reason!"

        if member is not None:

            await member.ban(reason=reason)
            embed = discord.Embed(
                title="Member banned!",
                description=f"Member {member.mention} has been banned by {ctx.author.mention}\nReason: {reason}",
                colour=0x6A90FD,
                timestamp=ctx.message.created_at
            )

            await ctx.send(embed=embed)

        else:

            await ctx.reply("Please mention a member!")
    
    @commands.command(name="unban", description="For unban banned members")
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member=None):
        
        if member is not None:
            banned_users = await ctx.guild.bans()
            member_name, member_discriminator = member.split('#')

            for ban_entry in banned_users:
                user = ban_entry.user


                if (user.name, user.discriminator) == (member_name, member_discriminator):
                    await ctx.guild.unban(user)
                    embed = discord.Embed(
                        title="User Unbanned!",
                        description=f"User {user.mention} was unbanned by {ctx.author.mention}",
                        colour=0x4DC6FF
                    )
                    await ctx.send(embed=embed)
                    return
            else:
                    await ctx.reply(f"User `{member}` was not banned!")
        else:
            await ctx.reply("Please enter a member name for example `Ocean network#3223`")
    

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.reply("You don't have permission to ban members!")


    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.reply("You don't have permission to unban members!")
        else:
            raise error



def setup(client):
    client.add_cog(Ban_Unban(client))