from datetime import datetime
import discord
from discord.ext import commands
from discord.ext.commands.errors import MissingPermissions



class Kick(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("-----\nkick loaded")

    @commands.command(name="kick", description="For kick a member!")
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member=None, *, reason=None):
        if member is not None:
            if reason is not None:
                reason = reason
            else:
                reason = "Without any reason!"
            await member.kick(reason=reason)
            embed = discord.Embed(
                title="Member kicked!",
                description=f"Member {member.mention} was kicked from server by {ctx.author.mention}\nReason: {reason}",
                colour=0xFF9301,
            )

            await ctx.send(embed=embed)
        else:
            await ctx.reply("Please mention a member!")


    @kick.error
    async def KickError(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.reply("You don't have permission to kick members!")
        else:
            raise error


def setup(client):
    client.add_cog(Kick(client))