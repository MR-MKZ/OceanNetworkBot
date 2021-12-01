import asyncio
import DiscordUtils
from discord.ext import commands, tasks
import discord
import DiscordUtils
import random
from bot_config.config import PLAYING_STATUS, WATCHING_STATUS, STATUS_LOOP_TIME

class Listeners(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.tracker = DiscordUtils.InviteTracker(client)
        
    


    @tasks.loop(seconds=10)
    async def PresenceChanger(self):
        global x
        global count

        guild = self.client.get_guild(897058199943917598)
        count = guild.member_count
        choose = iter(
            [
                "1",
                "2",
            ]
        )  
        for x in range(random.randint(1, 2)):
            x = next(choose)
        
        if x == "1":
            await self.client.change_presence(activity=discord.Game(name=PLAYING_STATUS))
        elif x == "2":
            await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=WATCHING_STATUS.format(str(count), guild.name)))

    
    @commands.Cog.listener()
    async def on_ready(self):
        print("-----\nListeners loaded")
        await self.PresenceChanger.start()
    
    

    # @commands.Cog.listener()
    # async def on_command_error(self, ctx, error):
    #     if isinstance(error, commands.CommandNotFound):
    #         await ctx.send(f"Command `{ctx.message.content[1:]}` not found")
    #         await asyncio.sleep(20)
    #         await ctx.channel.purge(limit=2)
    

    # @commands.Cog.listener()
    # async def on_reaction_add(self, reaction, user):
    #     print(f"reaction added by {user}")


    # @commands.Cog.listener()
    # async def on_raw_reaction_remove(self, payload):
    #     userid = payload.user_id
    #     channel = payload.channel_id
    #     print(f"user <@!{userid}> has removed a reaction\nchannel: <#{channel}>")
        

def setup(client):
    client.add_cog(Listeners(client))