import asyncio
import json
from difflib import SequenceMatcher

import discord
from discord.ext import commands


async def getHelpEmbed(ctx):
    embed = discord.Embed(
        title="راهنمای استفاده:",
        description="""
        
        دیدن توضیحات یک تاپیک
        ``-info اسم تاپیک``

        Topic Managers Role:

        اینجاد توضیحات درباره یک تاپیک
        ``-info create [توضیحات تاپیک] [اسم تاپیک ( 1 کلمه)]``

        پاک کردن یک تاپیک:
        ``-info delete [اسم تاپیک]``

        ادیت تاپیک:
        ``-info edit [توضیحات تاپیک] [اسم تاپیک ( 1 کلمه)]``
        
        """,
        color=0x00FEE3
    )
    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
    embed.set_footer(text="By OceanNetwork Community")
    return embed


async def checkForOtherArguments(usage, key, description):
    if usage == "create" or usage == "edit":

        if key == "" or description == "":
            return False
        else:
            return True
    elif usage == "delete":
        if key == "":
            return False
        else:
            return True


async def rightPerm(ctx):
    roles = [907564611044261909]
    roleids = ctx.author.roles
    memberid = ctx.author.id
    result = False

    if memberid in roles:
        result = True
    for i in roleids:
        if i.id in roles:
            result = True

    return result


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


class Topics(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("-----\nTopics loaded")

    @commands.command(name="info", description="For add delete or see a topic!")
    async def info(self, ctx, usage="", key="", *, description=""):
        # help command
        if usage == "":
            embed = await getHelpEmbed(ctx)
            await ctx.send(embed=embed)
        elif usage.lower() == "create":
            if await checkForOtherArguments(usage.lower(), key, description) == False:
                await ctx.send(embed=await getHelpEmbed())
            else:
                if await rightPerm(ctx):

                    with open("OceanNetworkBot\\bot_config\\topics.json", "r") as f:
                        loaded = json.load(f)

                    if key.lower() in loaded:
                        await ctx.send("این تاپیک قبلا به ثبت رسیده!")
                    else:
                        loaded[key.lower()] = {}
                        loaded[key.lower()]["description"] = description
                        loaded[key.lower()]["by"] = ctx.author.name

                        with open('OceanNetworkBot\\bot_config\\topics.json', 'w') as f:
                            json.dump(loaded, f)

                        embed = discord.Embed(
                            title=f"تاپیک ({key}) با موفقیت ثبت شد",
                            description=f"""
                            
                            توضیحات تاپیک:
                            \n

                            {description}
                            


                            ``-info {key}``
                            """
                        )
                        embed.set_footer(
                            text=f"By OceanNetwork Community - {ctx.author.name}")
                        await ctx.send(embed=embed)
                else:
                    await ctx.send("دسترسی این کار برای شما وجود ندارد.")

        elif usage.lower() == "delete":
            if await checkForOtherArguments(usage.lower(), key, description) == False:
                await ctx.send(embed=await getHelpEmbed(ctx))
            else:
                if await rightPerm(ctx):

                    with open("OceanNetworkBot\\bot_config\\topics.json", "r") as f:
                        loaded = json.load(f)

                    if not key.lower() in loaded:

                        await ctx.send("این تاپیک وجود ندارد.")
                    else:

                        del loaded[key.lower()]

                        with open('OceanNetworkBot\\bot_config\\topics.json', 'w') as f:
                            json.dump(loaded, f)

                        await ctx.send("این تاپیک با موفقیت حذف شد.")
                else:
                    await ctx.send("دسترسی این کار برای شما وجود ندارد.")

        elif usage.lower() == "edit":
            if await checkForOtherArguments(usage.lower(), key, description) == False:
                await ctx.send(embed=await getHelpEmbed(ctx))
            else:
                if await rightPerm(ctx):

                    with open("OceanNetworkBot\\bot_config\\topics.json", "r") as f:
                        loaded = json.load(f)

                    if not key.lower() in loaded:
                        await ctx.send("این تاپیک وجود ندارد.")
                    else:

                        loaded[key.lower()]["description"] = description
                        loaded[key.lower()]["by"] = ctx.author.name

                        with open('OceanNetworkBot\\bot_config\\topics.json', 'w') as f:
                            json.dump(loaded, f)

                        await ctx.send("توضیحات این تاپیک ادیت شد.")
                else:
                    await ctx.send("دسترسی این کار برای شما وجود ندارد.")
        else:
            usage = usage.lower()
            with open("OceanNetworkBot\\bot_config\\topics.json", "r") as f:
                loaded = json.load(f)

            if usage in loaded:
                description = loaded[usage]["description"]
                by = loaded[usage]["by"]

                embed = discord.Embed(
                    title=f"درباره تاپیک: {usage}",
                    description=description,
                    color=0x00FEE3
                )
                embed.set_footer(text=f"By OceanNetwork Community - {by}")
                async with ctx.typing():
                    await asyncio.sleep(1)
                await ctx.send(embed=embed)
            else:
                list = []
                results = []
                for i in loaded:
                    list.append(i)

                for i in list:
                    if i in usage or usage in i:
                        results.append(i)

                description = ''
                if len(results) != 0:

                    for i in results:
                        description = description + f"\n ``-info {i}``"

                    embed = discord.Embed(
                        title="منظور شما این بود؟",
                        description=description,
                        color=0x00FEE3
                    )
                    embed.set_author(name=ctx.author.name,
                                     icon_url=ctx.author.avatar_url)
                    embed.set_footer(
                        text="By OceanNetwork Community")
                    await ctx.send(embed=embed)
                else:

                    results = []
                    for i in list:
                        if similar(i, usage.lower()) >= 0.5:
                            results.append(i)

                    if len(results) != 0:

                        for i in results:
                            description = description + f"\n ``-info {i}``"

                        embed = discord.Embed(
                            title="منظور شما این بود؟",
                            description=description,
                            color=0x00FEE3
                        )
                        embed.set_author(name=ctx.author.name,
                                         icon_url=ctx.author.avatar_url)
                        embed.set_footer(
                            text="By OceanNetwork Community")
                        await ctx.send(embed=embed)
                    else:
                        await ctx.send("این تاپیک وجود ندارد.")


def setup(client):
    client.add_cog(Topics(client))
