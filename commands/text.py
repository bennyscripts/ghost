import discord
import requests
import asyncio
import random
import art as asciiart
import os

from discord.ext import commands
from utils import config
from utils import codeblock
from utils import cmdhelper
from utils import fonts
from utils import imgembed

class Text(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.description = cmdhelper.cog_desc("text", "Text commands")
        self.cfg = config.Config()

    @commands.command(name="text", description="Text commands.", usage="")
    async def text(self, ctx, selected_page: int = 1):
        cfg = config.Config()
        pages = cmdhelper.generate_help_pages(self.bot, "Text")

        if cfg.get("message_settings")["style"] == "codeblock":
            msg = codeblock.Codeblock(
                f"{cfg.get('theme')['emoji']} text commands",
                description=pages["codeblock"][selected_page - 1],
                extra_title=f"Page {selected_page}/{len(pages['codeblock'])}"
            )

            await ctx.send(msg, delete_after=cfg.get("message_settings")["auto_delete_delay"])

        else:
            embed = imgembed.Embed(title="Text Commands", description=pages["image"][selected_page - 1], colour=cfg.get("theme")["colour"])
            embed.set_footer(text=f"Page {selected_page}/{len(pages['image'])}")
            embed.set_thumbnail(url=cfg.get("theme")["image"])
            embed_file = embed.save()

            await ctx.send(file=discord.File(embed_file, filename="embed.png"), delete_after=cfg.get("message_settings")["auto_delete_delay"])
            os.remove(embed_file)

    @commands.command(name="shrug", description="Shrug your arms.", usage="")
    async def shrug(self, ctx):
        await ctx.send("¯\_(ツ)_/¯")

    @commands.command(name="tableflip", description="Flip the table.", usage="")
    async def tableflip(self, ctx):
        await ctx.send("(╯°□°）╯︵ ┻━┻")

    @commands.command(name="unflip", description="Put the table back.", usage="")
    async def unflip(self, ctx):
        await ctx.send("┬─┬ ノ( ゜-゜ノ)")

    @commands.command(name="lmgtfy", description="Let me Google that for you.", usage="[search]", aliases=["letmegooglethatforyou"])
    async def lmgtfy(self, ctx, *, search):
        await ctx.send(f"https://lmgtfy.app/?q={search.replace(' ', '+')}")

    @commands.command(name="blank", description="Send a blank message", usage="", aliases=["empty"])
    async def blank(self, ctx):
        await ctx.send("** **")

    @commands.command(name="fakepurge", description="Flood chat with blank messages", usage="")
    async def blank(self, ctx):
        msgs = [str("** **\n" * 5) for i in range(10)] 
        for msg in msgs:
            await ctx.send(msg)
            await asyncio.sleep(.5)

    @commands.command(name="ascii", description="Create ascii text art from text.", usage="[text]")
    async def ascii_(self, ctx, *, text: str):
        await ctx.send(f"```\n{asciiart.text2art(text)}\n```")

    @commands.command(name="aesthetic", description="Make your text aesthetic.", usage="[text]")
    async def aesthetic(self, ctx, *, text: str):
        result = " ".join(list(fonts.bypass(text)))
        await ctx.send(result)

    @commands.command(name="chatbypass", description="Bypass chat filters.", aliases=["bypass"], usage="[text]")
    async def chatbypass(self, ctx, *, text: str):
        await ctx.send(fonts.bypass(text))

    @commands.command(name="regional", description="Make your text out of emojis.", usage="[text]")
    async def regional(self, ctx, *, text: str):
        await ctx.send(fonts.regional(text))

    @commands.command(name="randomcase", description="Make your text random case.", usage="[text]")
    async def randomcase(self, ctx, *, text: str):
        result = "".join([random.choice([char.upper(), char.lower()]) for char in text])
        await ctx.send(result)

    @commands.command(name="animate", description="Animate your text.", usage="[text]")
    async def animate(self, ctx, *, text: str):
        output = ""
        text = list(text)
        msg = await ctx.send(text[0])
        for letter in text:
            output = output + letter + ""
            await msg.edit(content=output)
            await asyncio.sleep(0.5)

    @commands.command(name="zalgo", description="Make your text Zalgo.", usage="[text]")
    async def zalgo(self, ctx, *, text: str):
        await ctx.send(requests.get(f"https://api.timbw.xyz/zalgo?text={text}").text)

def setup(bot):
    bot.add_cog(Text(bot))