# await ctx.author.avatar_url_as(format="png").save(fp="filenamehere.png")
import discord
from discord.ext import commands
import shutil
from discord.ext.commands.errors import MissingPermissions
import requests
import os
import asyncio



class ChangeProf(commands.Cog):
    def __init__(self, client):
        self.client = client
    

    @commands.Cog.listener()
    async def on_ready(self):
        print("-----\nProfileChanger loaded")
    


    @commands.command(name="avatar", description="For change bot avatar")
    @commands.has_permissions(manage_nicknames=True)
    async def avatar(self, ctx, pic_url=None):

        if pic_url is not None:
            pass
        else:
            pic_url = ctx.guild.icon_url

        url = requests.get(pic_url)

        file_name = "profile.png"

        if url.status_code == 200:
            with requests.get(pic_url, stream=True) as r:
                with open(f"OceanNetworkBot\\{file_name}", 'wb') as f:
                    shutil.copyfileobj(r.raw, f)

            with open(f"OceanNetworkBot\\{file_name}", "rb") as image:
                await self.client.user.edit(avatar=image.read())

            embed = discord.Embed(
            title="ProfileChanged",
            description="The bot profile picture has been changed!"
            )
            
            try:
                embed.set_image(url=pic_url)
            except:
                pass

            await ctx.send(embed=embed)

            await asyncio.sleep(10)

            os.remove(f"OceanNetworkBot\\{file_name}")

                

        elif url.status_code == 404:
            await ctx.reply("Your link has a problem!")
    


    @avatar.error
    async def avatar_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.reply("You don't have permission for changing bot avatar!")
        else:
            raise error


def setup(client):
    client.add_cog(ChangeProf(client))