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
                cog_desc = cog.description.split("\n")

                try:
                    cmds.append({
                        "name": cog_desc[1].lower(),
                        "description": cog_desc[0]
                    })
                except:
                    pass

        cmds = sorted(cmds, key=lambda k: len(k["name"]))

        for cmd in cmds:
            if cmd["name"] == "help":
                continue
            elif cfg.get("message_settings")["style"] == "codeblock":
                description += f"{cmd['name']} :: {cmd['description']}\n"
            else:
                description += f"{self.bot.command_prefix}**{cmd['name']}** {cmd['description']}\n"

        if command is None:
            await cmdhelper.send_message(ctx, {
                "title": "Help",
                "description": description + f"\nThere are **{len(self.bot.commands)}** commands!",
                "codeblock_desc": description
            }, extra_title=f"{len(self.bot.commands)} total commands")

        else:
            cmd_obj = self.bot.get_command(command)
            if cmd_obj is None:
                await cmdhelper.send_message(ctx, {
                    "title": "Error",
                    "description": "That command wasn't found.",
                    "colour": "#ff0000"
                })

            else:
                info = {
                    "name": cmd_obj.name,
                    "description": cmd_obj.description,
                    "usage": cmd_obj.usage
                }

                longest_key = max([len(key) for key in info.keys()])

                await cmdhelper.send_message(ctx, {
                    "title": "Help",
                    "description": "\n".join([f"**{key}:** {value}" for key, value in info.items()]),
                    "codeblock_desc": "\n".join([f"{key}{' ' * (longest_key - len(key))} :: {value}" for key, value in info.items()])
                })

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
            await cmdhelper.send_message(ctx, {
                "title": "Search",
                "description": f"No results found for **{query}**.",
                "colour": "#ff0000"
            })

        else:
            await cmdhelper.send_message(ctx, {
                "title": "Search",
                "description": pages[selected_page - 1],
                "codeblock_desc": pages[selected_page - 1],
                "footer": f"Page {selected_page}/{len(pages)}"
            }, extra_title=f"Page {selected_page}/{len(pages)}")

    @commands.command(name="scripts", description="List all scripts.", usage="")
    async def scripts_cmd(self, ctx, selected_page: int = 1):
        cfg = config.Config()
        scripts_list = scripts.get_scripts()

        if len(scripts_list) == 0:
            await cmdhelper.send_message(ctx, {
                "title": "Scripts",
                "description": "No scripts found.",
                "colour": "#ff0000"
            })

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

            await cmdhelper.send_message(ctx, {
                "title": "Scripts",
                "description": pages[selected_page - 1],
                "codeblock_desc": pages[selected_page - 1],
                "footer": f"Page {selected_page}/{len(pages)}"
            }, extra_title=f"Page {selected_page}/{len(pages)}")

def setup(bot):
    bot.add_cog(General(bot))