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

async def send_message(ctx, embed_obj: dict, extra_title="", extra_message="", delete_after=None):
    cfg = config.Config()
    theme = cfg.theme
    title = embed_obj.get("title", theme.title)
    description = embed_obj.get("description", "")
    colour = embed_obj.get("colour", theme.colour)
    footer = embed_obj.get("footer", theme.footer)
    thumbnail = embed_obj.get("thumbnail", theme.image)
    codeblock_desc = embed_obj.get("codeblock_desc", description)
    if delete_after is None:
        delete_after = cfg.get("message_settings")["auto_delete_delay"]

    if cfg.get("message_settings")["style"] == "codeblock":
        description = description.replace("*", "")
        description = description.replace("`", "")

        msg = await ctx.send(str(codeblock.Codeblock(title=title, description=codeblock_desc, extra_title=extra_title)), delete_after=delete_after)
    elif cfg.get("message_settings")["style"] == "image":
        if theme.emoji in title:
            title = title.replace(theme.emoji, "")
        
        title = title.lstrip()
        embed2 = imgembed.Embed(title=title, description=description, colour=colour)
        embed2.set_footer(text=footer)
        embed2.set_thumbnail(url=thumbnail)
        embed_file = embed2.save()
        
        msg = await ctx.send(file=discord.File(embed_file, filename="embed.png"), delete_after=delete_after)
        os.remove(embed_file)
    
    if extra_message != "":
        extra_msg = await ctx.send(extra_message, delete_after=delete_after)
        return msg, extra_msg
    
    return msg

