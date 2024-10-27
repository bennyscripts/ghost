import os
import sys
import discord
import json
import psutil
import platform

from discord.ext import commands
from utils import config
from utils import codeblock
from utils import cmdhelper
from utils import imgembed

class Util(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.description = cmdhelper.cog_desc("util", "Utility commands")
        self.cfg = config.Config()

    @commands.command(name="util", description="Utility commands.", aliases=["utilities", "utility", "utils"], usage="")
    async def util(self, ctx, selected_page: int = 1):
        cfg = config.Config()
        pages = cmdhelper.generate_help_pages(self.bot, "Util")

        if cfg.get("message_settings")["style"] == "codeblock":
            msg = codeblock.Codeblock(
                f"{cfg.get('theme')['emoji']} utility commands",
                description=pages["codeblock"][selected_page - 1],
                extra_title=f"Page {selected_page}/{len(pages['codeblock'])}"
            )

            await ctx.send(msg, delete_after=cfg.get("message_settings")["auto_delete_delay"])

        else:
            embed = imgembed.Embed(title="Utility Commands", description=pages["image"][selected_page - 1], colour=cfg.get("theme")["colour"])
            embed.set_footer(text=f"Page {selected_page}/{len(pages['image'])}")
            embed.set_thumbnail(url=cfg.get("theme")["image"])
            embed_file = embed.save()

            await ctx.send(file=discord.File(embed_file, filename="embed.png"), delete_after=cfg.get("message_settings")["auto_delete_delay"])
            os.remove(embed_file)

    @commands.group(name="config", description="Configure ghost.", usage="")
    async def config(self, ctx):
        cfg = config.Config()

        if ctx.invoked_subcommand is None:
            new_cfg = cfg.config_without_theme_dict
            new_cfg.pop("token")

            for api_key in new_cfg["apis"]:
                new_cfg["apis"][api_key] = "******"

            cfg_str = json.dumps(cfg.config_without_theme_dict, indent=4, sort_keys=False)[1:][:-1]
            description = ""

            for line in cfg_str.split("\n"):
                description += line[4:] + "\n"

            await ctx.send(str(codeblock.Codeblock(title="config", description=description, style="yaml")), delete_after=self.cfg.get("message_settings")["auto_delete_delay"])

    @config.command(name="set", description="Set a config value.", usage="[key] [value]")
    async def set(self, ctx, key, *, value):
        if value.lower() == "true":
            value = True
        elif value.lower() == "false":
            value = False

        if key.lower() == "message_settings.auto_delete_delay":
            try:
                value = int(value)
            except ValueError:
                await ctx.send(str(codeblock.Codeblock(title="error", extra_title="the value isnt an integer")), delete_after=self.cfg.get("message_settings")["auto_delete_delay"])
                return

        if "." in key:
            key2 = key.split(".")
            if key2[0] not in self.cfg.config or key2[1] not in self.cfg.config[key2[0]]:
                await ctx.send(str(codeblock.Codeblock(title="error", extra_title="invalid key")), delete_after=self.cfg.get("message_settings")["auto_delete_delay"])
                return
        
        else:
            if key not in self.cfg.config:
                await ctx.send(str(codeblock.Codeblock(title="error", extra_title="invalid key")), delete_after=self.cfg.get("message_settings")["auto_delete_delay"])
                return

        if key == "prefix":
            self.bot.command_prefix = value

        if "." in key:
            key2 = key.split(".")
            self.cfg.config[key2[0]][key2[1]] = value

        else:
            self.cfg.config[key] = value

        self.cfg.save()
        await ctx.send(str(codeblock.Codeblock(title="config", extra_title="key updated", description=f"{key} :: {value}")), delete_after=self.cfg.get("message_settings")["auto_delete_delay"])

    @commands.command(name="restart", description="Restart the bot.", usage="", aliases=["reboot", "reload"])
    async def restart(self, ctx):
        cfg = config.Config()
        
        await cmdhelper.send_message(ctx, {
            "title": cfg.get("theme")["title"],
            "description": "restarting the ghost...",
        })
        
        os.execl(sys.executable, sys.executable, *sys.argv)

    @commands.command(name="settings", description="View ghost's settings.", usage="")
    async def settings(self, ctx):
        cfg = config.Config()
        command_amount = len(self.bot.commands)

        if cfg.get("message_settings")["style"] == "codeblock":
            await ctx.send(str(codeblock.Codeblock(title="settings", description=f"""prefix         :: {self.bot.command_prefix}
version        :: {config.VERSION}
command amount :: {command_amount}""")), delete_after=self.cfg.get("message_settings")["auto_delete_delay"])

        else:
            embed = imgembed.Embed(title="Settings", description=f"**Prefix:** {self.bot.command_prefix}\n**Version:** {config.VERSION}\n**Command Amount:** {command_amount}", colour=cfg.get("theme")["colour"])
            embed.set_footer(text=cfg.get("theme")["footer"])
            embed_file = embed.save()

            await ctx.send(file=discord.File(embed_file, filename="embed.png"), delete_after=cfg.get("message_settings")["auto_delete_delay"])
            os.remove(embed_file)


    @commands.command(name="prefix", description="Set the prefix", usage="[prefix]")
    async def prefix(self, ctx, prefix):
        cfg = config.Config()
        if self.bot.command_prefix == prefix:
            await cmdhelper.send_message(ctx, discord.imgembed.Embed(title="prefix", description=f"{prefix} is already youre prefix").to_dict())
        else:
            await cmdhelper.send_message(ctx, discord.imgembed.Embed(title="prefix", description=f"Set your prefix to {prefix}").to_dict())
            self.bot.command_prefix = prefix
            cfg.set("prefix", prefix)

    @commands.command(name="specs", description="View your computer's specs", usage="")
    async def specs(self, ctx):
        cpu_name = platform.processor()
        ram_size = psutil.virtual_memory().total
        disk_size = psutil.disk_usage("/").total
        os_name = platform.system()
        python_version = platform.python_version()

        if platform.system() == "Windows":
            disk_size = psutil.disk_usage("C:").total

        ram_size = f"{ram_size // 1000000000}GB"
        disk_size = f"{disk_size // 1000000000}GB"

        info = {
            "OS": f"{os_name}",
            "CPU": cpu_name if cpu_name else "Unknown",
            "RAM": f"{ram_size}",
            "Disk": f"{disk_size}",
            "Python": python_version,
        }

        longest_key = max([len(key) for key in info.keys()])

        await cmdhelper.send_message(ctx, {
            "title": "Computer Specs",
            "description": "\n".join([f"**{key}:** {value}" for key, value in info.items()]),
            "codeblock_desc": "\n".join([f"{key}{' ' * (longest_key - len(key))} :: {value}" for key, value in info.items()]),
            "thumbnail": ""
        })

def setup(bot):
    bot.add_cog(Util(bot))