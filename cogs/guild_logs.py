from discord.ext import commands
from discord.ext.commands.errors import MissingPermissions



async def save_audit_logs(self, guild):
    number = 1
    with open(f'OceanNetworkBot\\bot_config\\audit_logs', 'w+') as f:
        async for entry in guild.audit_logs(limit=100):
            f.write(f'{number}- "{entry.user}" did "{entry.action}" to "{entry.target}"\n\n')
            number += 1



class ChannelLogs(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.Cog.listener()
    async def on_ready(self):
        print("-----\naudit log loaded")



    @commands.command(name="audit", description="For save server audit log")
    @commands.has_permissions(view_audit_log=True)
    async def audit(self, ctx):
        await save_audit_logs(self, ctx.message.channel.guild)
        await ctx.reply("Audit log was saved!")

    

    @audit.error
    async def audit_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.reply("You don't have permission to save server audit log!")





def setup(client):
    client.add_cog(ChannelLogs(client))