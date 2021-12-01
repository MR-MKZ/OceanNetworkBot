from bot_config.config import BADWORDS
from discord.ext import commands



class BadWordsRemover(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.Cog.listener()
    async def on_ready(self):
        print("-----\nBadWordsRemover loaded")
    

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == self.client.user.id:
            return
        msg_content = message.content.lower()

        if any(word in msg_content for word in BADWORDS):
            await message.delete()

def setup(client):
    client.add_cog(BadWordsRemover(client))