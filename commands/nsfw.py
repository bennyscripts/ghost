import requests
import discord
import os
import random

from discord.ext import commands

from utils import config
from utils import codeblock
from utils import cmdhelper
from utils import imgembed

class NSFW(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.description = cmdhelper.cog_desc("nsfw", "NSFW commands")
        self.cfg = config.Config()

    @commands.command(name="nsfw", description="NSFW commands.", aliases=["notsafeforwork"], usage="")
    async def nsfw(self, ctx, selected_page: int = 1):
        cfg = config.Config()
        pages = cmdhelper.generate_help_pages(self.bot, "NSFW")

        if cfg.get("message_settings")["style"] == "codeblock":
                msg = codeblock.Codeblock(
                    f"{cfg.get('theme')['emoji']} nsfw commands",
                    description=pages["codeblock"][selected_page - 1],
                    extra_title=f"Page {selected_page}/{len(pages['codeblock'])}"
                )

                await ctx.send(msg, delete_after=cfg.get("message_settings")["auto_delete_delay"])

        else:
                embed = imgembed.Embed(title="NSFW Commands", description=pages["image"][selected_page - 1], colour=cfg.get("theme")["colour"])
                embed.set_footer(text=f"Page {selected_page}/{len(pages['image'])}")
                embed.set_thumbnail(url=cfg.get("theme")["image"])
                embed_file = embed.save()

                await ctx.send(file=discord.File(embed_file, filename="embed.png"), delete_after=cfg.get("message_settings")["auto_delete_delay"])
                os.remove(embed_file)
    
    @commands.command(name="hentai", description="Get a random hentai image.", usage="")
    async def hentai(self, ctx):
        cfg = config.Config()
        r = requests.get("https://nekobot.xyz/api/image?type=hentai")
        data = r.json()
        await ctx.send(data["message"], delete_after=cfg.get("message_settings")["auto_delete_delay"])

    @commands.command(name="thighs", description="Get a random thighs image.", aliases=["thigh", "hthigh"],usage="")
    async def thigh(self, ctx):
        cfg = config.Config()
        r = requests.get("https://nekobot.xyz/api/image?type=hthigh")
        data = r.json()
        await ctx.send(data["message"], delete_after=cfg.get("message_settings")["auto_delete_delay"])

    @commands.command(name="ass", description="Get a random ass image.", usage="")
    async def ass(self, ctx):
        cfg = config.Config()
        r = requests.get("https://nekobot.xyz/api/image?type=hass")
        data = r.json()
        await ctx.send(data["message"], delete_after=cfg.get("message_settings")["auto_delete_delay"])     

    @commands.command(name="femboy", description="Get a random femboy image.", usage="")
    async def femboy(self, ctx):
        cfg = config.Config()
        r = requests.get("https://r34-json-api.herokuapp.com/posts?tags=femboy")
        data = r.json()
        randimg = random.choice(data)
        await ctx.send(randimg["file_url"], delete_after=cfg.get("message_settings")["auto_delete_delay"])

    @commands.command(name="neko", description="Get a random neko image.", usage="")
    async def neko(self, ctx):
        cfg = config.Config()
        r = requests.get("https://nekobot.xyz/api/image?type=neko")
        data = r.json()
        await ctx.send(data["message"], delete_after=cfg.get("message_settings")["auto_delete_delay"])

    @commands.command(name="rule34", description="Get a rule34 image by tag.", aliases=["r34"], usage="")  
    async def rule34(self, ctx, *, tag):
        cfg = config.Config()
        if (("child" in tag) or ("shota" in tag) or ("loli" in tag)):
            await ctx.send("Sorry, but that tag is illegal ❌", delete_after=cfg.get("message_settings")["auto_delete_delay"]) 
            return
        r = requests.get(f"https://r34-json-api.herokuapp.com/posts?tags={tag}")
        data = r.json()
        randimg = random.choice(data)
        await ctx.send(randimg["file_url"], delete_after=cfg.get("message_settings")["auto_delete_delay"])  


def setup(bot):
    bot.add_cog(NSFW(bot))