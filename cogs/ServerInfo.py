import discord
from discord.ext import commands
from discord.ext.commands.errors import MissingPermissions


class ServerInfo(commands.Cog):
    def __init__(self, client):
        self.client = client
    

    @commands.Cog.listener()
    async def on_ready(self):
        print("-----\nServerInfo loaded")
    

    @commands.command(aliases=["guild_info"], name="serverinfo", description="For see server informations")
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def serverinfo(self, ctx):
        role_count = len(ctx.guild.roles)
        list_of_bots = [bot.mention for bot in ctx.guild.members if bot.bot]

        server_info_embed = discord.Embed(timestamp=ctx.message.created_at, colour=ctx.author.color)
        server_info_embed.add_field(name="Name", value=ctx.guild.name, inline=False)
        server_info_embed.add_field(name="Member Count", value=ctx.guild.member_count, inline=False)
        server_info_embed.add_field(name="Verification Level", value=str(ctx.guild.verification_level), inline=False)
        server_info_embed.add_field(name="Highest Role", value=ctx.guild.roles[-1], inline=False)
        server_info_embed.add_field(name="Number of Roles", value=str(role_count), inline=False)
        server_info_embed.add_field(name="Bots", value=", ".join(list_of_bots), inline=False)

        await ctx.send(embed=server_info_embed)
    

    @serverinfo.error
    async def serverinfo_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.reply("You don't have permission see server informations")
        else:
            raise error


def setup(client):
    client.add_cog(ServerInfo(client))