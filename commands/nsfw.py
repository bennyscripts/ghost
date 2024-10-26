import requests
import discord
import os
import random

from discord.ext import commands

from utils import config
from utils import codeblock
from utils import cmdhelper
from utils import imgembed

class RedditNSFW:
    def __init__(self):
        self.types = ["boobs", "ass", "hentai", "porn", "pussy", "tittydrop", "tittypop", "femboy", "thighs"]
        self.user_agent = "Mozilla/5.0 (Windows NT 6.2;en-US) AppleWebKit/537.32.36 (KHTML, live Gecko) Chrome/56.0.3075.83 Safari/537.32"
        self.headers = {"User-Agent": self.user_agent}

    def get_image(self, type):
        if type not in self.types:
            return "Invalid type."
    
        else:
            for t in self.types:
                if type == t:
                    request = requests.get(f"https://www.reddit.com/r/{t}/random.json", headers=self.headers)
                    if request.status_code == 200:
                        data = request.json()
                        url = data[0]["data"]["children"][0]["data"]["url"]
                        if "redgifs" in str(url):
                            url = data[0]["data"]["children"][0]["data"]["preview"]["reddit_video_preview"]["fallback_url"]

                        return url

    def porn(self):
        url = None

        while url is None:
            url = self.get_image("porn")

        return url

    def boobs(self):
        url = None

        while url is None:
            url = self.get_image(random.choice(["boobs", "tittydrop", "tittypop"]))

        return url
    
    def ass(self):
        url = None

        while url is None:
            url = self.get_image("ass")

        return url
    
    def pussy(self):
        url = None

        while url is None:
            url = self.get_image("pussy")

        return url
    
    def thighs(self):
        url = None

        while url is None:
            url = self.get_image("thighs")

        return url

class NSFW(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.description = cmdhelper.cog_desc("nsfw", "NSFW commands")
        self.cfg = config.Config()
        self.reddit_client = RedditNSFW()

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
        r = requests.get("https://nekobot.xyz/api/image?type=hentai")
        data = r.json()
        await ctx.send(data["message"])

    @commands.command(name="thighs", description="Get a random thighs pic.", aliases=["thigh"],usage="")
    async def thigh(self, ctx):
        data = self.reddit_client.thighs()
        await ctx.send(data)

    @commands.command(name="ass", description="Get a random ass pic.", usage="")
    async def ass(self, ctx):
        data = self.reddit_client.ass()
        await ctx.send(data)     

    @commands.command(name="boobs", description="Get a random tit pic.", usage="", aliases=["tits", "tittys", "titty"])
    async def boobs(self, ctx):
        data = self.reddit_client.boobs()
        await ctx.send(data)     

    @commands.command(name="pussy", description="Get a random pussy pic.", usage="")
    async def pussy(self, ctx):
        data = self.reddit_client.pussy()
        await ctx.send(data)     

    @commands.command(name="porn", description="Get a random porn gif.", usage="", aliases=["porngif"])
    async def porn(self, ctx):
        data = self.reddit_client.porn()
        await ctx.send(data)     

    @commands.command(name="neko", description="Get a random neko image.", usage="")
    async def neko(self, ctx):
        r = requests.get("https://nekobot.xyz/api/image?type=neko")
        data = r.json()
        await ctx.send(data["message"])

def setup(bot):
    bot.add_cog(NSFW(bot))