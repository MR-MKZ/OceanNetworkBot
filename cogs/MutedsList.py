import discord
from discord.ext import commands
from discord.ext.commands.errors import ExpectedClosingQuoteError, MissingPermissions




class CountOfMuteds(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.Cog.listener()
    async def on_ready(self):
        print("-----\nMuteList loaded")
    


    @commands.command(pass_context=True, name="muted_members", description="For see muted members")
    @commands.has_permissions(manage_messages=True)
    async def muted_members(self, ctx):
        server = ctx.message.guild
        role_name = (''.join("Muted"))
        MutedMembers = []
        role_id = server.roles[0]
        for role in server.roles:
            if role_name == role.name:
                role_id = role
                break
        else:
            await ctx.send("Role Muted doesn't exist. You have to mute someone to create a mute role!\n||-mute <@member> <time: 10s(s=second, m=minutes, h=hours, d=day, w=week, M=month, y=year)>||")
            return

        for member in server.members:
            if role_id in member.roles:
                MutedMembers.append(member.mention)
        embed = discord.Embed(
            colour=0x01B2FF
        )
        embed.add_field(name="Muted Members", value='\n'.join(f"{i}" for i in MutedMembers), inline=True)

        await ctx.send(embed=embed)


    @muted_members.error
    async def muted_members_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.reply("You don't have permission to see muted members")
        else:
            raise error
    




def setup(client):
    client.add_cog(CountOfMuteds(client))