import discord
import os
import time
import requests

from discord.ext import commands
from utils import config
from utils import codeblock
from utils import cmdhelper
from utils import imgembed
from utils import scripts

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.description = cmdhelper.cog_desc("help", "Get help with a command")

    @commands.command(name="help", description="A list of all categories.", usage="")
    async def help(self, ctx, command: str = None):
        cfg = config.Config()
        description = ""
        cmds = []

        for cog_name in self.bot.cogs:
            cog = self.bot.get_cog(cog_name)

            if cog.description is not None:
                desc = cog.description.split("\n")[0]
                cmd_name = cog.description.split("\n")[1]

                if cog_name.lower() != "general":
                    cmds.append({"name": cmd_name, "description": desc})

        cmds = sorted(cmds, key=lambda k: len(k["name"]))

        for cmd in cmds:
            if cfg.get("message_settings")["style"] == "codeblock":
                description += f"{cmd['name']} :: {cmd['description']}\n"
            else:
                description += f"{self.bot.command_prefix}**{cmd['name']}** {cmd['description']}\n"

        if command is None:
            if cfg.get("message_settings")["style"] == "codeblock":
                msg = codeblock.Codeblock(f"{cfg.get('theme')['emoji']} {cfg.get('theme')['title']}", description)

                await ctx.send(msg, delete_after=cfg.get("message_settings")["auto_delete_delay"])

            else:
                embed = imgembed.Embed(title=cfg.get('theme')['title'], description=f"{description}\nThere are **{len(self.bot.commands)}** commands!", colour=cfg.get("theme")["colour"])
                embed.set_footer(text=cfg.get("theme")["footer"])
                embed.set_thumbnail(url=cfg.get("theme")["image"])
                embed_file = embed.save()

                await ctx.send(file=discord.File(embed_file, filename="embed.png"), delete_after=cfg.get("message_settings")["auto_delete_delay"])
                os.remove(embed_file)

        else:
            cmd_obj = self.bot.get_command(command)
            if cmd_obj is None:
                if cfg.get("message_settings")["style"] == "codeblock":
                    await ctx.send(codeblock.Codeblock(title=f"help", description=f"Command not found.", extra_title=command), delete_after=cfg.get("message_settings")["auto_delete_delay"])

                else:
                    embed = imgembed.Embed(title=f"Help", description=f"That command wasn't found.", colour=cfg.get("theme")["colour"])
                    embed.set_footer(text=cfg.get("theme")["footer"])
                    embed_file = embed.save()

                    await ctx.send(file=discord.File(embed_file, filename="embed.png"), delete_after=cfg.get("message_settings")["auto_delete_delay"])
                    os.remove(embed_file)

            else:

                if cfg.get("message_settings")["style"] == "codeblock":
                    msg = codeblock.Codeblock(f"help", f"""Name        :: {cmd_obj.name}
Description :: {cmd_obj.description}
Usage       :: {cmd_obj.usage}""")

                    await ctx.send(msg, delete_after=cfg.get("message_settings")["auto_delete_delay"])

                else:
                    embed = imgembed.Embed(title="Help", description=f"""**Name:** {cmd_obj.name}
**Description:** {cmd_obj.description}
**Usage:** {cmd_obj.usage}""", colour=cfg.get("theme")["colour"])
                    embed.set_footer(text=cfg.get("theme")["footer"])
                    embed_file = embed.save()

                    await ctx.send(file=discord.File(embed_file, filename="embed.png"), delete_after=cfg.get("message_settings")["auto_delete_delay"])
                    os.remove(embed_file)

    @commands.command()
    async def ping(self, ctx):
        cfg = config.Config()
        latency = requests.get("https://discord.com/api/users/@me", headers={"Authorization": cfg.get("token")}).elapsed.total_seconds()
        msg = codeblock.Codeblock(f"ping", extra_title=f"Your latency is {round(latency * 1000)}ms")

        await ctx.send(msg, delete_after=cfg.get("message_settings")["auto_delete_delay"])
    
    @commands.command(name="search", description="Search for commands.", usage="[query]")
    async def search(self, ctx, query: str, selected_page: int = 1):
        cfg = config.Config()
        commands = self.bot.walk_commands()
        commands_formatted = []
        commands_2 = []
        spacing = 0
        pages = []

        for cmd in commands:
            if query in cmd.name or query in cmd.description:
                prefix = cmdhelper.get_command_help(cmd)

                if len(prefix) > spacing:
                    spacing = len(prefix)

                commands_2.append([prefix, cmd.description])

        for cmd in commands_2:
            if cfg.get("message_settings")["style"] == "codeblock":
                commands_formatted.append(f"{cmd[0]}{' ' * (spacing - len(cmd[0]))} :: {cmd[1]}")
            else:
                commands_formatted.append(f"**{cmd[0]}** {cmd[1]}")

        commands_str = ""
        for cmd in commands_formatted:
            if len(commands_str) + len(cmd) > 1000:
                pages.append(commands_str)
                commands_str = ""

            commands_str += f"{cmd}\n"

        if len(commands_str) > 0:
            pages.append(commands_str)
        
        if len(pages) == 0:
            if cfg.get("message_settings")["style"] == "codeblock":
                msg = codeblock.Codeblock(title=f"search", description=f"No results found.", extra_title=query)
                await ctx.send(msg, delete_after=cfg.get("message_settings")["auto_delete_delay"])

            else:
                embed = imgembed.Embed(title="Search", description=f"No results found for **{query}**.", colour=cfg.get("theme")["colour"])
                embed.set_footer(text=cfg.get("theme")["footer"])
                embed_file = embed.save()

                await ctx.send(file=discord.File(embed_file, filename="embed.png"), delete_after=cfg.get("message_settings")["auto_delete_delay"])
                os.remove(embed_file)

        else:
            if cfg.get("message_settings")["style"] == "codeblock":
                msg = codeblock.Codeblock(title=f"search", description=pages[selected_page - 1], extra_title=f"Page {selected_page}/{len(pages)}")
                await ctx.send(msg, delete_after=cfg.get("message_settings")["auto_delete_delay"])

            else:
                embed = imgembed.Embed(title="Search", description=pages[selected_page - 1], colour=cfg.get("theme")["colour"])
                embed.set_footer(text=f"Page {selected_page}/{len(pages)}")
                embed_file = embed.save()

                await ctx.send(file=discord.File(embed_file, filename="embed.png"), delete_after=cfg.get("message_settings")["auto_delete_delay"])
                os.remove(embed_file)

    @commands.command(name="scripts", description="List all scripts.", usage="")
    async def scripts_cmd(self, ctx, selected_page: int = 1):
        cfg = config.Config()
        scripts_list = scripts.get_scripts()

        if len(scripts_list) == 0:
            if cfg.get("message_settings")["style"] == "codeblock":
                msg = codeblock.Codeblock(title=f"scripts", description=f"No scripts found.")
                await ctx.send(msg, delete_after=cfg.get("message_settings")["auto_delete_delay"])

            else:
                embed = imgembed.Embed(title="Scripts", description=f"No scripts found.", colour=cfg.get("theme")["colour"])
                embed.set_footer(text=cfg.get("theme")["footer"])
                embed_file = embed.save()

                await ctx.send(file=discord.File(embed_file, filename="embed.png"), delete_after=cfg.get("message_settings")["auto_delete_delay"])
                os.remove(embed_file)

        else:
            pages = []
            scripts_str = ""
            for script in scripts_list:
                if len(scripts_str) + len(script) > 1000:
                    pages.append(scripts_str)
                    scripts_str = ""

                script_in_cmds = False
                script_name = script.split("/")[-1].replace(".py", "")

                for cmd in self.bot.commands:
                    if cmd.name == script_name:
                        script_in_cmds = True
                        break

                if script_in_cmds:
                        if cfg.get("message_settings")["style"] == "codeblock":
                            scripts_str += f"{cmd.name} :: {cmd.description}\n"
                        else:
                            scripts_str += f"**{self.bot.command_prefix}{cmd.name}** {cmd.description}\n" 
                else:
                    if cfg.get("message_settings")["style"] == "codeblock":
                        scripts_str += f"{script_name} :: Script name not found as a command\n"
                    else:
                        scripts_str += f"**{script_name}** Script name not found as a command\n" 

            if len(scripts_str) > 0:
                pages.append(scripts_str)

            if cfg.get("message_settings")["style"] == "codeblock":
                msg = codeblock.Codeblock(title=f"scripts", description=pages[selected_page - 1], extra_title=f"Page {selected_page}/{len(pages)}")
                await ctx.send(msg, delete_after=cfg.get("message_settings")["auto_delete_delay"])

            else:
                embed = imgembed.Embed(title="Scripts", description=pages[selected_page - 1], colour=cfg.get("theme")["colour"])
                embed.set_footer(text=f"Page {selected_page}/{len(pages)}")
                embed_file = embed.save()

                await ctx.send(file=discord.File(embed_file, filename="embed.png"), delete_after=cfg.get("message_settings")["auto_delete_delay"])
                os.remove(embed_file)

def setup(bot):
    bot.add_cog(General(bot))