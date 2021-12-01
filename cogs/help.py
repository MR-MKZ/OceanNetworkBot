# Requires pip install buttons
from os import name
from discord.ext import commands
import discord

from files.util import Pag

class Help(commands.Cog, name="Help command"):
    def __init__(self, bot):
        self.bot = bot
        self.cmds_per_page = 6

    def get_command_signature(self, command: commands.Command, ctx: commands.Context):
        aliases = "|".join(command.aliases)
        cmd_invoke = f"[{command.name}|{aliases}]" if command.aliases else command.name

        full_invoke = command.qualified_name.replace(command.name, "")

        signature = f"{ctx.prefix}{full_invoke}{cmd_invoke} {command.signature}"
        return signature

    async def return_filtered_commands(self, walkable, ctx):
        filtered = []

        for c in walkable.walk_commands():
            try:
                if c.hidden:
                    continue

                elif c.parent:
                    continue

                await c.can_run(ctx)
                filtered.append(c)
            except commands.CommandError:
                continue

        return self.return_sorted_commands(filtered)

    def return_sorted_commands(self, commandList):
        return sorted(commandList, key=lambda x: x.name)

    async def help_normal(self, ctx, entity=None, title=None):
        entity = entity or self.bot
        title = title or self.bot.description

        # pages = []


        help_embed = discord.Embed(
            title="Help for commands",
            colour=0xFF5757
        )

        if isinstance(entity, commands.Command):
            filtered_commands = (
                list(set(entity.all_commands.values()))
                if hasattr(entity, "all_commands")
                else []
            )
            filtered_commands.insert(0, entity)

        else:
            filtered_commands = await self.return_filtered_commands(entity, ctx)

        for i in range(0, len(filtered_commands), self.cmds_per_page):
            next_commands = filtered_commands[i : i + self.cmds_per_page]
            # commands_entry = ""

            for cmd in next_commands:
                desc = cmd.short_doc or cmd.description
                signature = self.get_command_signature(cmd, ctx)
                # subcommand = "Has subcommands" if hasattr(cmd, "all_commands") else ""

                if isinstance(entity, commands.Command):
                    help_embed.add_field(name=f"**__{cmd.name}__**", value=f"```{signature}```")
                    help_embed.set_footer(text=desc)
                else:
                    help_embed.add_field(name=f"**__{cmd.name}__**", value=f"{desc}")

        await ctx.send(embed=help_embed)
                # commands_entry += (
                #     f"• **__{cmd.name}__**\n```\n{signature}\n```\n{desc}\n"
                #     if isinstance(entity, commands.Command)
                #     else f"• **__{cmd.name}__**\n{desc}\n    {subcommand}\n"
                # )
        #     pages.append(commands_entry)

        # await Pag(title=title, colour=0xFF5757, entries=pages, length=3).start(ctx)

    @commands.Cog.listener()
    async def on_ready(self):
        print("-----\nhelp loaded")

    @commands.command(
        name="help", aliases=["h", "commands"], description="The help command!"
    )
    async def help_command(self, ctx, *, entity=None):
        if not entity:
            await self.help_normal(ctx)

        else:
            cog = self.bot.get_cog(entity)
            if cog:
                await self.help_normal(ctx, cog, f"{cog.qualified_name}'s commands")

            else:
                command = self.bot.get_command(entity)
                if command:
                    await self.help_normal(ctx, command, command.name)

                else:
                    await ctx.send("Entity not found.")


def setup(bot):
    bot.add_cog(Help(bot))
