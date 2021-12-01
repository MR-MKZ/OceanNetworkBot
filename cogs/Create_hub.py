import asyncio

import discord
from bot_config.config import (ACTIVIE_EMPTYCHANNEL_TIMEOUT, HUB_CATEGORY_NAME,
                               HUB_LOGS_CHANNEL_NAME, LOOP_HUB_CHEKER_TIME)
from discord.ext import commands, tasks
from discord.utils import get


class CreateHub(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.ids_list = []

    @commands.Cog.listener()
    async def on_ready(self):
        print("-----\ncreate hub  loaded")

    @tasks.loop(seconds=LOOP_HUB_CHEKER_TIME)
    async def HubChecker(self):

        channel_for_send = self.client.get_channel(hub_logs_channel.id)

        for channel_id in self.ids_list:
            channel = self.client.get_channel(channel_id)
            
            try:
                members = len(channel.members)
            except:
                pass

            # print(members)
            try:
                if members == 0:
                    await channel.delete()
                    dead_msg = await channel_for_send.send(f"**`ویس '{channel}' به دلیل خالی بودن و نداشتن عضو پاک شد`**")
                    self.ids_list.remove(channel_id)
                    await asyncio.sleep(2)
                    await dead_msg.delete()
                else:
                    pass
            except:
                pass

    @commands.command(aliases=["hub"], name="create_hub", description="For creating hub")
    async def create_hub(self, ctx):
        global sender_channel
        global hub_logs_channel

        sender_channel = ctx.message.channel.id

        user_name = ctx.author.display_name

        hub_category = get(ctx.guild.categories, name=HUB_CATEGORY_NAME)

        hub_logs_channel = get(ctx.guild.channels, name=HUB_LOGS_CHANNEL_NAME)

        await ctx.guild.create_voice_channel(f"{user_name} Hub", category=hub_category)
        voice_channel = get(ctx.guild.voice_channels,
                                name=f"{user_name} Hub")

        id = voice_channel.id

        # await ctx.reply(f"Hub was created! <#{id}>")

        hub_embed = discord.Embed(
            description=f"**ویس چنل شما ساخته شد __<#{id}>__**",
            colour=0x0DEAB8,
            timestamp=ctx.message.created_at
        )
        hub_embed.set_author(name=self.client.user.display_name,
                             icon_url=self.client.user.avatar_url)

        self.ids_list.append(id)

        await ctx.reply(embed=hub_embed, content=ctx.author.mention)

        await asyncio.sleep(ACTIVIE_EMPTYCHANNEL_TIMEOUT)

        try:
            await self.HubChecker.start()
        except:
            pass


def setup(client):
    client.add_cog(CreateHub(client))
