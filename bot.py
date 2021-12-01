import logging
import os
from pathlib import Path

import discord
import motor.motor_asyncio
from discord.ext import commands

import files.json_loader
from files.mongo import Document

cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(f"{cwd}\n-----")


async def get_prefix(bot, message):

    if not message.guild:
        return commands.when_mentioned_or("-")(bot, message)

    try:
        data = await bot.config.find(message.guild.id)

        if not data or "prefix" not in data:
            return commands.when_mentioned_or("-")(bot, message)
        return commands.when_mentioned_or(data["prefix"])(bot, message)
    except:
        return commands.when_mentioned_or("-")(bot, message)


intents = discord.Intents().all()
secret_file = files.json_loader.read_json('secrets')
bot = commands.Bot(
    command_prefix=get_prefix, case_insensitive=True, intents=intents, help_command=None
)
bot.config_token = secret_file["token"]
bot.connection_url = secret_file["mongo"]
logging.basicConfig(level=logging.INFO)

bot.cwd = cwd


@bot.event
async def on_ready():
    print(f"-----\nLogged in as: {bot.user.name} : {bot.user.id}")
    print("-----\nInitialized Database")


if __name__ == "__main__":
    # DataBases
    bot.mongo = motor.motor_asyncio.AsyncIOMotorClient(str(bot.connection_url))
    bot.db = bot.mongo["OceanNetwork"]
    bot.warnss = Document(bot.db, "warns")
    bot.invites = Document(bot.db, "invites")
    # ---------------------------------------------------------
    for file in os.listdir(cwd + "/cogs"):
        if file.endswith(".py") and not file.startswith("_"):
            bot.load_extension(f"cogs.{file[:-3]}")

bot.run(bot.config_token)
