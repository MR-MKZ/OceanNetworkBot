
import asyncio
import json
import discord
from discord import colour
from discord.ext.commands.errors import MissingPermissions
from bot_config.config import (TICKET_CLOSER_TIMEOUT,
                               TICKET_OPENED_COLOR_EMBED,
                               TICKET_OPENED_DESCRIPTION_EMBED,
                               TICKET_OPENED_TITLE_EMBED,
                               REACTION_FOR_TICKET_EMBED_COLOR,
                               REMOVE_TICKET_CHANNEL_TIMEOUT)
from discord.ext import commands



class Ticket(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.client.ticket_configs = []

    @commands.Cog.listener()
    async def on_ready(self):
        try:
            for file in ["bot_config/Databases.json"]:
                with open("bot_config/Databases.json", "a") as f:
                    pass
                    
            with open("bot_config/Databases.json", "r") as ff:

                loaded = json.load(ff)

                self.client.ticket_configs = [int(loaded["ticket"]["msg_id"]), int(loaded["ticket"]["channel_id"]), int(loaded["ticket"]["category_id"])]
        except:
            pass                                

        print("-----\nticket loaded")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.member.id != self.client.user.id and str(payload.emoji) == u"\U0001f4e9":
            
            msg_id = self.client.ticket_configs[0]

            channel_id = self.client.ticket_configs[1]
            
            category_id = self.client.ticket_configs[2]

            
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
                        await self.client.wait_for(timeout=TICKET_CLOSER_TIMEOUT)
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

            await asyncio.sleep(REMOVE_TICKET_CHANNEL_TIMEOUT)

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

        self.client.ticket_configs = [
            msg.id, msg.channel.id, category.id]

        with open("bot_config/Databases.json", "r") as ff:
            loaded = json.load(ff)

        loaded["ticket"] = {}
        
        loaded["ticket"]["msg_id"] = msg.id

        loaded["ticket"]["channel_id"] = ctx.channel.id

        loaded["ticket"]["category_id"] = category.id

        with open("bot_config/Databases.json", "w") as f:
            json.dump(loaded, f)

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
