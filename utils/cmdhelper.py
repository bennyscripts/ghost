import os
import discord

from . import codeblock
from . import config
from . import imgembed

def cog_desc(cmd, desc):
    return f"{desc}\n{cmd}"

def get_command_help(cmd):
    prefix = ""

    if cmd.parent is not None:
        prefix = f"{cmd.parent.name} {cmd.name}"
    else:
        prefix = f"{cmd.name}"

    return prefix

def generate_help_pages(bot, cog):
    pages = []
    pages_2 = []
    commands = bot.get_cog(cog).walk_commands()
    commands_formatted = []
    commands_formatted_2 = []
    commands_2 = []
    spacing = 0

    for cmd in commands:
        if cmd.name.lower() != cog.lower():
            prefix = get_command_help(cmd)

            if len(prefix) > spacing:
                spacing = len(prefix)

            commands_2.append([prefix, cmd.description])

    for cmd in commands_2:
        commands_formatted_2.append(f"{cmd[0]}{' ' * (spacing - len(cmd[0]))} :: {cmd[1]}")
        commands_formatted.append(f"**{bot.command_prefix}{cmd[0]}** {cmd[1]}")

    commands_str = ""
    for cmd in commands_formatted:
        if len(commands_str) + len(cmd) > 300:
            pages.append(commands_str)
            commands_str = ""

        commands_str += f"{cmd}\n"

    if len(commands_str) > 0:
        pages.append(commands_str)

    commands_str = ""
    for cmd in commands_formatted_2:
        if len(commands_str) + len(cmd) > 500:
            pages_2.append(commands_str)
            commands_str = ""

        commands_str += f"{cmd}\n"

    if len(commands_str) > 0:
        pages_2.append(commands_str)

    return {"codeblock": pages_2, "image": pages}

async def send_message(ctx, embed_obj: dict, extra_title=""):
    cfg = config.Config()
    title = embed_obj.get("title", cfg.get("theme")["title"])
    description = embed_obj.get("description", "")
    colour = embed_obj.get("colour", cfg.get("theme")["colour"])
    footer = embed_obj.get("footer", cfg.get("theme")["footer"])
    thumbnail = embed_obj.get("thumbnail", cfg.get("theme")["image"])

    if cfg.get("message_settings")["style"] == "codeblock":
        description = description.replace("*", "")
        description = description.replace("`", "")

        return await ctx.send(str(codeblock.Codeblock(title=title, description=description, extra_title=extra_title)), delete_after=cfg.get("message_settings")["auto_delete_delay"])
    elif cfg.get("message_settings")["style"] == "image":
        embed2 = imgembed.Embed(title=title, description=description, colour=colour)
        embed2.set_footer(text=footer)
        embed2.set_thumbnail(url=thumbnail)
        embed_file = embed2.save()
        
        msg = await ctx.send(file=discord.File(embed_file, filename="embed.png"), delete_after=cfg.get("message_settings")["auto_delete_delay"])
        os.remove(embed_file)

        return msg
