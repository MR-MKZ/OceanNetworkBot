import asyncio

import discord
from bot_config.config import (ACTIVIE_EMPTYCHANNEL_TIMEOUT, HUB_CATEGORY_NAME,
                               HUB_LOGS_CHANNEL_NAME, LOOP_HUB_CHECKER_TIME)
from discord.ext import commands, tasks
from discord.utils import get


class CreateHub(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.ids_list = []
        self.member_id = []
        self.names_list = ["test"]
        self.client.test_configs = {}

    @commands.Cog.listener()
    async def on_ready(self):
        print("-----\nHub setup  loaded")


    @tasks.loop(seconds=LOOP_HUB_CHECKER_TIME)
    async def HubChecker(self):

        if hub_logs_channel is not None:

            channel_for_send = self.client.get_channel(hub_logs_channel.id)

        else:

            channel_for_send = None

        for channel_id in self.ids_list:
            channel = self.client.get_channel(channel_id)

            try:
                members = len(channel.members)
            except:
                pass

            # print(members)
            try:
                if channel_for_send is not None:

                    if members == 0:
                        await channel.delete()
                        await channel_for_send.send(f"**`ویس '{channel}' به دلیل خالی بودن و نداشتن عضو پاک شد`**")
                        self.ids_list.remove(channel_id)
                        self.names_list.remove(channel.name)
                        self.member_id.remove(member_id)
                    else:
                        pass
                else:
                    pass
            except:
                pass
    


    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.member.id != self.client.user.id and str(payload.emoji) == u"\u2705":
            msg_id, channel_id, category_id = self.client.test_configs[payload.guild_id]
            global member_id

            if payload.message_id == msg_id:
                guild = self.client.get_guild(payload.guild_id)

                for category in guild.categories:
                    if category.id == category_id:
                        break 
                

                user_name = payload.member.display_name
                

                member_id = payload.member.id

                self.member_id.append(member_id)

                for member in self.member_id:
                    member_id_count = self.member_id.count(member)

                if member_id_count < 2:
 
                    await hub_category.create_voice_channel(f"{user_name} Hub")

                    voice_channel = get(guild.voice_channels,
                                    name=f"{user_name} Hub")

                    id = voice_channel.id

                    name = voice_channel.name
                                    
                    self.ids_list.append(id)

                    self.names_list.append(name)

                    channel = guild.get_channel(channel_id)

                    message = await channel.fetch_message(msg_id)
                                    
                    await message.remove_reaction(payload.emoji, payload.member)

                    await asyncio.sleep(ACTIVIE_EMPTYCHANNEL_TIMEOUT)

                    try:
                        await self.HubChecker.start()
                    except:
                        pass

                else:

                    channel = self.client.get_channel(channel_id)
                        
                    message = await channel.fetch_message(msg_id)

                    await message.remove_reaction(payload.emoji, payload.member)

                    error_msg = await channel.send("شما نمی توانید بیشتر از یک هاب بسازید!")

                    self.member_id.remove(member_id)

                    await asyncio.sleep(5)

                    await error_msg.delete()



                
                # for uservc in self.names_list:

                #     count = self.names_list.count(uservc)

                #     print(uservc," : ", count)

                #     if count == 2:

                #         channel = self.client.get_channel(channel_id)
                        
                #         message = await channel.fetch_message(msg_id)

                #         await message.remove_reaction(payload.emoji, payload.member)

                #         self.ids_list.remove(voice_channel.id)

                #         self.names_list.remove(uservc)

                #         error_msg = await channel.send("شما نمی توانید بیشتر از یک هاب بسازید!")

                #         await asyncio.sleep(5)

                #         await error_msg.delete()

                #         await voice_channel.delete()

                #     else:
                #         print(uservc," : ", count)
                #         await hub_category.create_voice_channel(f"{user_name} Hub")

                #         voice_channel = get(guild.voice_channels,
                #                         name=f"{user_name} Hub")

                #         id = voice_channel.id

                #         name = voice_channel.name
                                        
                #         self.ids_list.append(id)

                #         self.names_list.append(name)

                #         channel = guild.get_channel(channel_id)

                #         message = await channel.fetch_message(msg_id)
                                        
                #         await message.remove_reaction(payload.emoji, payload.member)

                #         await asyncio.sleep(ACTIVIE_EMPTYCHANNEL_TIMEOUT)

                #         try:
                #             await self.HubChecker.start()
                #         except:
                #             pass
                        


    @commands.command(name="hub_setup", description="Setup for hub creator embed")
    async def hub_setup(self, ctx):
        global sender_channel
        global hub_category
        global user_name
        global hub_logs_channel

        await ctx.channel.purge(limit=1)

        sender_channel = ctx.message.channel.id

        hub_category = get(ctx.guild.categories, name=HUB_CATEGORY_NAME)

        if HUB_LOGS_CHANNEL_NAME is not None:

            hub_logs_channel = get(ctx.guild.channels, name=HUB_LOGS_CHANNEL_NAME)
        else:
            hub_logs_channel = None

        hub_embed = discord.Embed(
            title="ساختن هاب",
            description="برای ساختن هاب استیکر :white_check_mark: رو ری اکشن کنید",
            colour=0x0DEAB8
        )

        hub_message = await ctx.send(embed=hub_embed)

        self.client.test_configs[ctx.guild.id] = [
            hub_message.id, hub_message.channel.id, hub_category.id]

        await hub_message.add_reaction(u"\u2705")



        # await ctx.guild.create_voice_channel(f"{user_name} Hub", category=hub_category)


        # # await ctx.reply(f"Hub was created! <#{id}>")

        # hub_embed = discord.Embed(
        #     description=f"**ویس چنل شما ساخته شد __<#{id}>__**",
        #     colour=0x0DEAB8,
        #     timestamp=ctx.message.created_at
        # )
        # hub_embed.set_author(name=self.client.user.display_name,
        #                      icon_url=self.client.user.avatar_url)


        # await ctx.reply(embed=hub_embed, content=ctx.author.mention)




def setup(client):
    client.add_cog(CreateHub(client))
