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
            await asyncio.sleep(0.86)

    @commands.command(name="cembed", description="Create a custom embed.", usage="[title] [description] [footer] [colour] [image]", aliases=["customembed"])
    async def cembed(self, ctx, title: str, description: str, footer: str = "", colour: str = "111112", image: str = ""):
        await cmdhelper.send_message(ctx, {
            "title": title,
            "description": description,
            "footer": footer,
            "colour": colour,
            "thumbnail": image
        }, extra_title=footer)

    @commands.command(name="passwordgen", description="Generate a password.", usage="[length]", aliases=["genpassword"])
    async def passwordgen(self, ctx, length: int = 16):
        password = "".join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()", k=length))
        await ctx.send(password)

    @commands.command(name="codeblock", description="Create a codeblock.", usage="[language] [code]", aliases=["block"])
    async def codeblock(self, ctx, language: str, *, code: str):
        await ctx.send(f"```{language}\n{code}\n```")

    @commands.command(name="json", description="Create a json codeblock.", usage="[json]", aliases=["jblock"])
    async def json(self, ctx, *, json: str):
        await self.codeblock(ctx, "json", code=json)

    @commands.command(name="python", description="Create a python codeblock.", usage="[python]", aliases=["pyblock"])
    async def python(self, ctx, *, python: str):
        await self.codeblock(ctx, "python", code=python)

    @commands.command(name="js", description="Create a javascript codeblock.", usage="[javascript]", aliases=["jsblock", "javascript"])
    async def js(self, ctx, *, js: str):
        await self.codeblock(ctx, "javascript", code=js)

    @commands.command(name="html", description="Create a html codeblock.", usage="[html]", aliases=["htmlblock"])
    async def html(self, ctx, *, html: str):
        await self.codeblock(ctx, "html", code=html)

    @commands.command(name="css", description="Create a css codeblock.", usage="[css]", aliases=["cssblock"])
    async def css(self, ctx, *, css: str):
        await self.codeblock(ctx, "css", code=css)

    @commands.command(name="java", description="Create a java codeblock.", usage="[java]", aliases=["javablock"])
    async def java(self, ctx, *, java: str):
        await self.codeblock(ctx, "java", code=java)

    @commands.command(name="c", description="Create a c codeblock.", usage="[c]", aliases=["cblock"])
    async def c(self, ctx, *, c: str):
        await self.codeblock(ctx, "c", code=c)

    @commands.command(name="cpp", description="Create a cpp codeblock.", usage="[cpp]", aliases=["cppblock"])
    async def cpp(self, ctx, *, cpp: str):
        await self.codeblock(ctx, "cpp", code=cpp)

    @commands.command(name="php", description="Create a php codeblock.", usage="[php]", aliases=["phpblock"])
    async def php(self, ctx, *, php: str):
        await self.codeblock(ctx, "php", code=php)

    @commands.command(name="lua", description="Create a lua codeblock.", usage="[lua]", aliases=["luablock"])
    async def lua(self, ctx, *, lua: str):
        await self.codeblock(ctx, "lua", code=lua)

    @commands.command(name="reverse", description="Reverse your text.", usage="[text]")
    async def reverse(self, ctx, *, text: str):
        await ctx.send(text[::-1])

def setup(bot):
    bot.add_cog(Text(bot))