import discord
from discord.ext import commands
from discord.ext.commands.errors import MissingPermissions
import asyncio


class Clear(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("-----\nclear loaded")

    @commands.command(no_pm=True, name="clear", description="For clear a channel", aliases=["purge"])
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=1000):
        mention = ctx.author.mention
        clear_embed = discord.Embed(
            description="پیام ها با موفقیت پاک شدند",
            colour=0xFF0051
        )
        await ctx.channel.purge(limit=amount+1)
        msg = await ctx.send(mention, embed=clear_embed)
        await asyncio.sleep(10)
        await msg.delete()

    
    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.reply("You don't have permission to clear channel")
        else:
            raise error

def setup(client):
    client.add_cog(Clear(client))