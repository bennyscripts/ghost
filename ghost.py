import os
import sys
import requests
import time
import discord

from discord.errors import LoginFailure
from discord.ext import commands

from pypresence import Presence

from utils import console
from utils import config
from utils import notifier
from utils import scripts
from utils import files
from utils import cmdhelper

# import utils as ghost_utils
import commands as ghost_commands

cfg = config.Config()
cfg.check()
files.create_defaults()

status_resp = requests.get("https://discord.com/api/users/@me/settings", headers={"Authorization": cfg.get("token")})
status = "online" if status_resp.status_code != 200 else status_resp.json()["status"]

ghost = commands.Bot(
    command_prefix=cfg.get("prefix"),
    self_bot=True,
    help_command=None,
    status=discord.Status.try_value(status),
    chunk_guilds_at_startup=False
)

user = requests.get("https://discord.com/api/users/@me", headers={"Authorization": cfg.get("token")}).json()

try:
    if cfg.get("rich_presence"):
        text = f"Logged in as {user['username']}"
        if str(user['discriminator']) != "0":
            text += f"#{user['discriminator']}"

        rich_presence = Presence("1018195507560063039")
        rich_presence.connect()
        rich_presence.update(details=text, large_image="icon", start=time.time())
except Exception as e:
    console.print_error(f"Failed to connect to Discord RPC")

for script_file in os.listdir("scripts"):
    if script_file.endswith(".py"):
        scripts.add_script("scripts/" + script_file, globals(), locals())

@ghost.event
async def on_connect():
    text = f"Logged in as {ghost.user.name}"
    if str(ghost.user.discriminator) != "0":
        text += f"#{ghost.user.discriminator}"

    console.clear()
    console.resize(columns=90, rows=25)
    console.print_banner()
    console.print_info(text)
    await ghost.add_cog(ghost_commands.Account(ghost))
    await ghost.add_cog(ghost_commands.Fun(ghost))
    await ghost.add_cog(ghost_commands.General(ghost))
    await ghost.add_cog(ghost_commands.Img(ghost))
    await ghost.add_cog(ghost_commands.Info(ghost))
    await ghost.add_cog(ghost_commands.Mod(ghost))
    await ghost.add_cog(ghost_commands.NSFW(ghost))
    await ghost.add_cog(ghost_commands.Text(ghost))
    await ghost.add_cog(ghost_commands.Theming(ghost))
    await ghost.add_cog(ghost_commands.Util(ghost))
    console.print_info(f"You can now use commands with {cfg.get('prefix')}")
    print()

    notifier.Notifier.send("Ghost", text)

@ghost.event
async def on_command(ctx):
    try:
        await ctx.message.delete()
    except Exception as e:
        console.print_error(str(e))

    command = ctx.message.content[len(ghost.command_prefix):]
    console.print_cmd(command)

@ghost.event
async def on_command_error(ctx, error):
    cfg = config.Config()

    try:
        await ctx.message.delete()
    except Exception as e:
        console.print_error(str(e))

    try:
        await cmdhelper.send_message(ctx, {
            "title": "Error",
            "description": str(error),
            "colour": "#ff0000"
        })

    except Exception as e:
        console.print_error(f"{e}")

    console.print_error(str(error))

try:
    ghost.run(cfg.get("token"))
except LoginFailure:
    console.print_error("Invalid token, please set a new one below.")
    new_token = input("> ")
    cfg.set("token", new_token)
    cfg.save()
    os.execl(sys.executable, sys.executable, *sys.argv)
