import discord
from discord.ext import commands
import asyncio
import json

from discord.ext.commands.errors import MissingPermissions


class Mute(commands.Cog):
    def __init__(self, client):
        self.client = client
    


    @commands.Cog.listener()
    async def on_ready(self):
        print("-----\nmute loaded")
    
    @commands.command(no_pm=True, name="mute", description="For mute a member")
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, member: discord.Member=None, time=None, *, reason=None):
        server = ctx.message.guild
        role_name = "Muted"
        for role in server.roles:
            if role_name == role.name:
                role_id = role
                break
        if not member:
            await ctx.send("You must mention a member to mute!")
            return
        elif not time:
            await ctx.send("You must mention a time!")
            return
        else:
            if not reason:
                reason="No reason given"
            time_conversion = {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800, "M": 2419200, "y": 29030400}
            mute_time = int(time[:-1]) * time_conversion[time[-1]]
        guild = ctx.guild
        Muted = discord.utils.get(guild.roles, name="Muted")
        if not Muted:
            Muted = await guild.create_role(name="Muted")
            for channel in guild.channels:
                await channel.set_permissions(Muted, speak=False, send_messages=False, read_message_history=True, read_messages=False)
        else:
            await member.add_roles(Muted, reason=reason)
            muted_embed = discord.Embed(title="Muted a user", description=f"{member.mention} Was muted by {ctx.author.mention} for {reason} to {time}", colour=0xFF0000)
            await ctx.send(embed=muted_embed)
            await asyncio.sleep(int(mute_time))

            if role_id in member.roles:
                await member.remove_roles(Muted)
                unmute_embed = discord.Embed(title='Mute over!', description=f'{ctx.author.mention} muted to {member.mention} for {reason} is over after {time}', colour=0x2AFF00)
                await ctx.send(embed=unmute_embed)
            else:
                pass
    

    @commands.command(name="unmute", description="For unmute a member")
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx, member: discord.Member=None):
        server = ctx.message.guild
        role_name = "Muted"
        for role in server.roles:
            if role_name == role.name:
                role_id = role
                break
        if not member is None:
            guild = ctx.guild
            Muted = discord.utils.get(guild.roles, name="Muted")

            if role_id not in member.roles:
                await ctx.send(f"{member.mention} was not muted!")
            else:
                await member.remove_roles(Muted)
                unmute_embed = discord.Embed(
                    title=f"{member.display_name} was unmuted!",
                    description=f"{ctx.author.mention} was unmuted {member.mention}!",
                    colour=0x0DEAB8
                )
                await ctx.send(embed=unmute_embed)
        else:
            await ctx.send("Please mention a member!")
    

    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.reply("You don't have permission to mute members")
        else:
            raise error


    @unmute.error
    async def unmute_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.reply("You don't have permission to unmute members")
        else:
            raise error



def setup(client):
    client.add_cog(Mute(client))
