from os import name
import discord
from discord.ext import commands
from discord.ext.commands import context
from discord.ext.commands.core import cooldown
from discord.ext.commands.errors import MissingPermissions, MissingRole
from files.util import Pag


class Warns(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("-----\nwarn loaded")
    


    @commands.command(name="warn", description="For warn a member")
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx, member: discord.Member, *, reason=None):
        if member.id in [ctx.author.id, self.client.user.id]:
            return await ctx.send("You can't warn your self or the bot!")
        

        current_warn_count = len(
            await self.client.warnss.find_many_by_custom(
                {
                    "user_id": member.id,
                    "guild_id": member.guild.id
                }
            )
        ) + 1

        filter_dict = {"user_id": member.id, "guild_id": member.guild.id}

        warn_filter = {"user_id": member.id, "guild_id": member.guild.id, "number": current_warn_count}
        if not reason is None:
            warn_data = {"reason": reason, "timestamp": ctx.message.created_at, "warned_by": ctx.author.id}

            

            if current_warn_count == 1:
                warn_embed = discord.Embed(
                    title="You are being warned:",
                    description=f"__**Reason**__:\n{reason}\nwarn {current_warn_count}/3",
                    colour=0xFDE8BE,
                    timestamp=ctx.message.created_at
                )

                warn_embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
                warn_embed.set_footer(text=f"Warn {current_warn_count}/3")

            elif current_warn_count == 2:
                warn_embed = discord.Embed(
                    title="You are being warned:",
                    description=f"__**Reason**__:\n{reason}\nwarn {current_warn_count}/3",
                    colour=0xF7A933,
                    timestamp=ctx.message.created_at
                )

                warn_embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
                warn_embed.set_footer(text=f"Warn {current_warn_count}/3")
            
            elif current_warn_count == 3:
                warn_embed = discord.Embed(
                    title="Member was banned:",
                    description=f"__**Reason**__:\n{reason}",
                    colour=0xFF0000,
                    timestamp=ctx.message.created_at
                )

                warn_embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
                warn_embed.set_footer(text=f"Warn {current_warn_count}/3")


            try:
                await member.send(embed=warn_embed)
                if current_warn_count != 3:
                    await ctx.send("Warned that user in dm's for you.")
                    await self.client.warnss.upsert_custom(warn_filter, warn_data)
                elif current_warn_count == 3:
                    await self.client.warnss.delete_by_custom(filter_dict)
                    await member.ban(reason=reason)
                    await ctx.send("Banned that user from server!")

            except:
                if current_warn_count != 3:
                    await ctx.send(member.mention, embed=warn_embed)
                    await self.client.warnss.upsert_custom(warn_filter, warn_data)
                elif current_warn_count == 3:
                    await self.client.warnss.delete_by_custom(filter_dict)
                    await member.ban(reason=reason)
                    await ctx.send("Banned that user from server!")
        else:
            await ctx.send("Please enter reason!")
        


    @commands.command(name="warns", description="For see warns of a member")
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def warns(self, ctx, member: discord.Member = None):

        if member is None:
            await ctx.send("Please mention a member!")
        else:
            warn_filter = {"user_id": member.id, "guild_id": member.guild.id}
            warns = await self.client.warnss.find_many_by_custom(warn_filter)
                
            if not bool(warns):
                return await ctx.send(f"Couldn't find any warns for: `{member.display_name}`")
                
            warns = sorted(warns, key=lambda x: x["number"])
                
            pages = []
            for warn in warns:
                description = f"""
                Warn Number: `{warn['number']}`
                Warn Reason: `{warn['reason']}`
                Warned By: <@{warn['warned_by']}>
                Warn Date: {warn['timestamp'].strftime("%I:%M %p %B %d, %Y")}
                """
                pages.append(description)
                

            await Pag(
                title=f"Warns for `{member.display_name}`",
                colour=0xCE2029,
                entries=pages,
                length=1
            ).start(ctx)

    @commands.command(aliases=["delwarn"], name="delete_warn", description="For delete warns or warn of a member")
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def delete_warn(self, ctx, member: discord.Member, warn: int = None):
        
        filter_dict = {"user_id": member.id, "guild_id": member.guild.id}
        if warn:
            filter_dict["number"] = warn

        was_deleted = await self.client.warnss.delete_by_custom(filter_dict)
        if was_deleted and was_deleted.acknowledged:
            if warn:
                return await ctx.send(
                    f"I deleted warn number `{warn}` for `{member.display_name}`"
                )

            return await ctx.send(
                f"I deleted `{was_deleted.deleted_count}` warns for `{member.display_name}`"
            )

        await ctx.send(
            f"I could not find any warns for `{member.display_name}` to delete matching your input"
        )
    

    @delete_warn.error
    async def deletewarnerror(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.reply("You don't have permission to delete warns of members")
        else:
            raise error
    

    @warns.error
    async def warns_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.reply("You don't have permission to see warns of members")
        else:
            raise error
    

    @warn.error
    async def warn_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.reply("You don't have permission to warn members")


def setup(client):
    client.add_cog(Warns(client))