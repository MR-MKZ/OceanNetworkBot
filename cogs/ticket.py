import asyncio

import aiofiles
import discord
from discord.ext.commands.errors import MissingPermissions
from bot_config.config import (TICKET_CLOSER_TIMEOUT,
                               TICKET_OPENED_COLOR_EMBED,
                               TICKET_OPENED_DESCRIPTION_EMBED,
                               TICKET_OPENED_TITLE_EMBED,
                               REACTION_FOR_TICKET_EMBED_COLOR)
from discord.ext import commands



class Ticket(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.ticket_configs = {}

    @commands.Cog.listener()
    async def on_ready(self):
        for file in ["ticket_configs.txt"]:
            async with aiofiles.open("ticket_configs.txt", mode="a") as temp:
                pass

        async with aiofiles.open("ticket_configs.txt", mode="r") as file:
            lines = await file.readlines()
            for line in lines:
                data = line.split(" ")
                self.ticket_configs[int(data[0])] = [int(data[1])], [int(data[2]), [int(data[3])]
                                                                            ]

        print("-----\nticket loaded")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.member.id != self.client.user.id and str(payload.emoji) == u"\U0001f4e9":
            msg_id, channel_id, category_id = self.ticket_configs[payload.guild_id]

            if payload.message_id == msg_id:
                guild = self.client.get_guild(payload.guild_id)

                for category in guild.categories:
                    if category.id == category_id:
                        break

                channel = guild.get_channel(channel_id)

                ticket_num = 1 if len(category.channels) == 0 else int(
                    category.channels[-1].name.split("-")[1]) + 1
                ticket_channel = await category.create_text_channel(f"ticket {ticket_num}", topic=f"A channel for ticket number {ticket_num}", permission_synced=True)

                await ticket_channel.set_permissions(payload.member, read_messages=True, send_messages=True)

                message = await channel.fetch_message(msg_id)
                await message.remove_reaction(payload.emoji, payload.member)

                ticket_embed = discord.Embed(
                    title=TICKET_OPENED_TITLE_EMBED,
                    description=TICKET_OPENED_DESCRIPTION_EMBED,
                    colour=TICKET_OPENED_COLOR_EMBED
                )

                ticket_msg = await ticket_channel.send(content=f"{payload.member.mention} Welcome", embed=ticket_embed)

                await ticket_msg.add_reaction(u"\U0001f512")

                try:

                    try:
                        await self.client.wait_for("message", check=lambda m: m.channel == ticket_channel and m.author == payload.member, timeout=TICKET_CLOSER_TIMEOUT)
                    except asyncio.TimeoutError:
                        await ticket_channel.delete()
                except:
                    pass

                else:
                    await ticket_channel.delete()
        elif payload.member.id != self.client.user.id and str(payload.emoji) == u"\U0001f512":

            guild = self.client.get_guild(payload.guild_id)

            ticket_opened_channel = guild.get_channel(payload.channel_id)

            await ticket_opened_channel.send("درحال بستن تیکت . . .")

            message = await ticket_opened_channel.fetch_message(payload.message_id)

            await message.remove_reaction(payload.emoji, payload.member)

            await asyncio.sleep(2)

            await ticket_opened_channel.delete()

    @commands.command(aliases=["ct"], name="ticket", description="For configuring ticket system")
    @commands.has_permissions(manage_messages=True)
    async def ticket(self, ctx, category: discord.CategoryChannel = None):
        if category is None:
            await ctx.channel.send("نیکت پیکربندی نشد! به دلیل وارد نکردن آرگومان یا نا معتبر بودن آن")
            return

        await ctx.channel.purge(limit=1)

        ticket_embed = discord.Embed(
            title="تیکت",
            description="برای ساختن تیکت استیکر :envelope_with_arrow: رو ری اکشن کنید",
            colour=REACTION_FOR_TICKET_EMBED_COLOR
        )

        msg = await ctx.send(embed=ticket_embed)

        self.client.ticket_configs[ctx.guild.id] = [
            msg.id, msg.channel.id, category.id]

        async with aiofiles.open("ticket_configs.txt", mode="r") as file:
            data = await file.readlines()

        async with aiofiles.open("ticket_configs.txt", mode="w") as file:
            await file.write(f"{ctx.guild.id} {msg.id} {msg.channel.id} {category.id}\n")

            for line in data:
                if int(line.split(" ")[0]) != ctx.guild.id:
                    await file.write(line)

        await msg.add_reaction(u"\U0001f4e9")
        ok_msg = await ctx.channel.send("سیستم تیکت با موفقیت پیکربندی شد!")
        await asyncio.sleep(5)
        await ok_msg.delete()
    

    @ticket.error
    async def ticket_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.reply("You don't have permission to configure ticket!")


def setup(client):
    client.add_cog(Ticket(client))
