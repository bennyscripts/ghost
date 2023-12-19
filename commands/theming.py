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

        if cfg.get("message_settings")["style"] == "codeblock":
            msg = codeblock.Codeblock(
                f"{cfg.get('theme')['emoji']} Theme commands",
                description=pages["codeblock"][selected_page - 1],
                extra_title=f"Page {selected_page}/{len(pages['codeblock'])}"
            )

            await ctx.send(msg, delete_after=cfg.get("message_settings")["auto_delete_delay"])

        else:
            embed = imgembed.Embed(title="Theme Commands", description=pages["image"][selected_page - 1], colour=cfg.get("theme")["colour"])
            embed.set_footer(text=f"Page {selected_page}/{len(pages['image'])}")
            embed.set_thumbnail(url=cfg.get("theme")["image"])
            embed_file = embed.save()

            await ctx.send(file=discord.File(embed_file, filename="embed.png"), delete_after=cfg.get("message_settings")["auto_delete_delay"])
            os.remove(embed_file)

    @commands.command(name="themes", description="Lists all your themes.", usage="")
    async def themes(self, ctx):
        cfg = config.Config()
        await cmdhelper.send_message(ctx, {
            "title": "Themes",
            "description": "\n".join(cfg.get_themes()),
            "colour": cfg.get("theme")["colour"],
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
                theme = cfg.get("theme")
                if cfg.get("message_settings")["style"] == "image":
                    description = f"**Current Theme:** {cfg.config['theme_name']}\n\n"
                else:
                    description = f"Current Theme: {cfg.config['theme_name']}\n\n"

                for key, value in theme.items():
                    val = value
                    if len(value) > 50:
                        val = "Too long to display"
                        
                    description += f"{key}: {val}\n"

                await cmdhelper.send_message(ctx, {
                    "title": "Theme",
                    "description": description,
                    "colour": cfg.get("theme")["colour"],
                    "footer": f"Use {self.bot.command_prefix}theme set [name] to change your theme",
                })

    @theme.command(name="set", description="Change your theme", usage="[theme]")
    async def change_theme(self, ctx, theme_name: str = None):
        cfg = config.Config()
        description = ""
        colour = cfg.get("theme")["colour"]
        theme = cfg.get_theme_file(theme_name)

        if theme:
            cfg.set_theme(theme_name)
            cfg = config.Config()

            colour = cfg.get("theme")["colour"]
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
            "footer": cfg.get("theme")["footer"],
        })

    async def theme_set(self, ctx, key, value):
        cfg = config.Config()
        description = ""
        colour = ""

        cfg.config["theme"][key] = value
        cfg.save()
        description = f"{key} set to {value}"

        cfg = config.Config() # Re iniate the config var because it needs to load the new local version of the config dict
        
        await cmdhelper.send_message(ctx, {
            "title": "Theme",
            "description": description,
            "colour": cfg.get("theme")["colour"],
            "footer": cfg.get("theme")["footer"],
        })

    @theme.command(name="title", description="Set the title of the embed.", usage="[title]")
    async def theme_title(self, ctx, *, title: str):
        await self.theme_set(ctx=ctx, key="title", value=title)
        
    @theme.command(name="colour", description="Set the colour of the embed.", usage="[colour]", aliases=["color"])
    async def theme_colour(self, ctx, colour: str):
        await self.theme_set(ctx=ctx, key="colour", value=colour)

    @theme.command(name="footer", description="Set the footer of the embed.", usage="[footer]")
    async def theme_footer(self, ctx, *, footer: str):
        await self.theme_set(ctx=ctx, key="footer", value=footer)

    @theme.command(name="image", description="Set the image of the embed.", usage="[image]")
    async def theme_image(self, ctx, image: str):
        await self.theme_set(ctx=ctx, key="image", value=image)

    @theme.command(name="style", description="Set the style of the embed.", usage="[style]")
    async def theme_style(self, ctx, style: str):
        await self.theme_set(ctx=ctx, key="style", value=style)

    @commands.command(name="imagemode", description="Set your theme style to image.", usage="")
    async def imagemode(self, ctx):
        await self.theme_set(ctx=ctx, key="style", value="image")

    @commands.command(name="textmode", description="Set your theme style to codeblock.", usage="", aliases=["codeblockmode"])
    async def textmode(self, ctx):
        await self.theme_set(ctx=ctx, key="style", value="codeblock")

def setup(bot):
    bot.add_cog(Theming(bot))