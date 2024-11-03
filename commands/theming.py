import os
import sys
import discord

from discord.ext import commands
from utils import config
from utils import codeblock
from utils import cmdhelper
from utils import imgembed

class Theming(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.description = cmdhelper.cog_desc("theming", "Theme commands.")
        self.cfg = config.Config()

    @commands.command(name="theming", description="Theme commands.", aliases=["design"], usage="")
    async def theming(self, ctx, selected_page: int = 1):
        cfg = config.Config()
        pages = cmdhelper.generate_help_pages(self.bot, "Theming")

        await cmdhelper.send_message(ctx, {
            "title": f"{cfg.theme.emoji} theme commands",
            "description": pages["image"][selected_page - 1],
            "footer": f"Page {selected_page}/{len(pages['image'])}",
            "codeblock_desc": pages["codeblock"][selected_page - 1]
        }, extra_title=f"Page {selected_page}/{len(pages['image'])}")

    @commands.command(name="themes", description="Lists all your themes.", usage="")
    async def themes(self, ctx):
        cfg = config.Config()
        desc = ""

        for theme in cfg.get_themes():
            desc += f"- {theme}\n"

        await cmdhelper.send_message(ctx, {
            "title": "Themes",
            "description": desc,
            "colour": cfg.theme.colour,
            "footer": f"Use {self.bot.command_prefix}theme [name] to change your theme",
        })

    @commands.group(name="theme", description="Theme commands.", usage="")
    async def theme(self, ctx):
        cfg = config.Config()

        if ctx.invoked_subcommand is None:
            msg_split = ctx.message.content.split(" ")
            if len(msg_split) >= 2:
                await self.change_theme(ctx, msg_split[1])

            else:
                theme = cfg.theme
                await cmdhelper.send_message(ctx, {
                    "title": "Theme",
                    "description": f"Current theme: {theme.name}",
                    "colour": theme.colour,
                    "footer": theme.footer,
                })

    @theme.command(name="set", description="Change your theme", usage="[theme]")
    async def change_theme(self, ctx, theme_name: str = None):
        cfg = config.Config()
        description = ""
        colour = cfg.theme.colour
        theme = cfg.get_theme_file(theme_name)

        if theme:
            cfg.set_theme(theme_name)
            cfg = config.Config()

            colour = cfg.theme.colour
            description = f"Theme set to {theme_name}"
        else:
            colour = "#ff0000"
            description = f"There isn't a theme named {theme_name}"
        
        cfg.save()
        cfg = config.Config() # Re iniate the config var because it needs to load the new local version of the config dict
        
        await cmdhelper.send_message(ctx, {
            "title": "Theme",
            "description": description,
            "colour": colour,
            "footer": cfg.theme.footer,
        })

    async def theme_set(self, ctx, subkey, value):
        cfg = config.Config()
        description = ""

        key = "message_settings" if subkey == "style" else "theme"

        if key == "theme":
            theme = cfg.theme
            theme.__dict__[subkey] = value
            description = f"Theme {subkey} set to {value}"
            cfg.theme.save()

        elif key == "message_settings":
            message_settings = cfg.get(key)
            message_settings[subkey] = value
            description = f"Message setting {subkey} set to {value}"

        cfg.save()
        cfg = config.Config() # Re iniate the config var because it needs to load the new local version of the config dict
        
        await cmdhelper.send_message(ctx, {
            "title": "Theme",
            "description": description,
            "colour": cfg.theme.colour,
            "footer": cfg.theme.footer,
        })

    @theme.command(name="title", description="Set the title of the embed.", usage="[title]")
    async def theme_title(self, ctx, *, title: str):
        await self.theme_set(ctx=ctx, subkey="title", value=title)
        
    @theme.command(name="colour", description="Set the colour of the embed.", usage="[colour]", aliases=["color"])
    async def theme_colour(self, ctx, colour: str):
        await self.theme_set(ctx=ctx, subkey="colour", value=colour)

    @theme.command(name="footer", description="Set the footer of the embed.", usage="[footer]")
    async def theme_footer(self, ctx, *, footer: str):
        await self.theme_set(ctx=ctx, subkey="footer", value=footer)

    @theme.command(name="image", description="Set the image of the embed.", usage="[image]")
    async def theme_image(self, ctx, image: str):
        await self.theme_set(ctx=ctx, subkey="image", value=image)

    @theme.command(name="style", description="Set the style of the embed.", usage="[style]")
    async def theme_style(self, ctx, style: str):
        await self.theme_set(ctx=ctx, subkey="style", value=style)

    @commands.command(name="imagemode", description="Set your theme style to image.", usage="", aliases=["imgmode"])
    async def imagemode(self, ctx):
        await self.theme_set(ctx=ctx, subkey="style", value="image")

    @commands.command(name="textmode", description="Set your theme style to codeblock.", usage="", aliases=["codeblockmode"])
    async def textmode(self, ctx):
        await self.theme_set(ctx=ctx, subkey="style", value="codeblock")

def setup(bot):
    bot.add_cog(Theming(bot))