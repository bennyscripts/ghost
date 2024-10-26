import requests
import discord
import os
import random
import json
import mimetypes

from PIL import Image
from discord.ext import commands

from utils import config
from utils import codeblock
from utils import cmdhelper
from utils import imgembed

class Img(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.description = cmdhelper.cog_desc("img", "Image commands")
        self.cfg = config.Config()

    @commands.command(name="img", description="Image commands.", aliases=["image"], usage="")
    async def img(self, ctx, selected_page: int = 1):
        cfg = config.Config()
        pages = cmdhelper.generate_help_pages(self.bot, "Img")

        if cfg.get("message_settings")["style"] == "codeblock":
            msg = codeblock.Codeblock(
                f"{cfg.get('theme')['emoji']} img commands",
                description=pages["codeblock"][selected_page - 1],
                extra_title=f"Page {selected_page}/{len(pages['codeblock'])}"
            )

            await ctx.send(msg, delete_after=cfg.get("message_settings")["auto_delete_delay"])

        else:
            embed = imgembed.Embed(title="Image Commands", description=pages["image"][selected_page - 1], colour=cfg.get("theme")["colour"])
            embed.set_footer(text=f"Page {selected_page}/{len(pages['image'])}")
            embed.set_thumbnail(url=cfg.get("theme")["image"])
            embed_file = embed.save()

            await ctx.send(file=discord.File(embed_file, filename="embed.png"), delete_after=cfg.get("message_settings")["auto_delete_delay"])
            os.remove(embed_file)

    @commands.command(name="gato", description="Get a random cat picture.", aliases=["cat", "catpic"], usage="")
    async def gato(self, ctx):
        cfg = config.Config()
        resp = requests.get("https://api.alexflipnote.dev/cats")
        image = resp.json()["file"]

        await ctx.send(image, delete_after=cfg.get("message_settings")["auto_delete_delay"])

    @commands.command(name="doggo", description="Get a random dog picture.", aliases=["dog", "dogpic"], usage="")
    async def doggo(self, ctx):
        cfg = config.Config()
        resp = requests.get("https://api.alexflipnote.dev/dogs")
        image = resp.json()["file"]

        await ctx.send(image, delete_after=cfg.get("message_settings")["auto_delete_delay"])

    @commands.command(name="bird", description="Get a random bird picture.", aliases=["birb", "birdpic"], usage="")
    async def birb(self, ctx):
        cfg = config.Config()
        resp = requests.get("https://api.alexflipnote.dev/birb")
        image = resp.json()["file"]

        await ctx.send(image, delete_after=cfg.get("message_settings")["auto_delete_delay"])

    @commands.command(name="fox", description="Get a random fox picture.", aliases=["foxpic"], usage="")
    async def fox(self, ctx):
        cfg = config.Config()
        resp = requests.get("https://randomfox.ca/floof/")
        image = resp.json()["image"]

        await ctx.send(image, delete_after=cfg.get("message_settings")["auto_delete_delay"])

    @commands.command(name="searchimage", description="Search for an image on google", usage="[query]", aliases=["searchimg", "imgsearch", "imagesearch"])
    async def searchimage(self, ctx, *, query):
        cfg = config.Config()
        api_key = cfg.get("apis")["serpapi"]
        base_url = "https://serpapi.com/search.json?"

        params = {
            "q": query.replace(" ", "+"),
            "engine": "google_images",
            "ijn": 0,
            "api_key": api_key
        }

        attempting_msg = await ctx.send(f"> Starting search for `{query}`.")

        url = base_url + "&".join(f"{param}={params[param]}" for param in params)
        data = requests.get(url)

        if data.status_code == 200:
            await attempting_msg.delete()

            body = data.json()

            if body["search_metadata"]["status"] != "Success":
                await cmdhelper.send_message(ctx, {
                    "title": "Image Search",
                    "description": "The search failed, try another query.",
                    "colour": "#ff0000",
                    "footer": cfg.get("theme")["footer"],
                })
            else:
                if "suggested_searches" not in body:
                    await cmdhelper.send_message(ctx, {
                        "title": "Image Search",
                        "description": "The search failed, try another query.",
                        "colour": "#ff0000",
                        "footer": cfg.get("theme")["footer"],
                    })

                else:
                    images_results = body["images_results"]
                    amount_to_send = len(images_results)
                    images = []

                    if len(images_results) > 4:
                        await cmdhelper.send_message(ctx, {
                            "title": "Image Search",
                            "description": f"We found {len(images_results)} results for {query}. A random result will be sent.",
                            "colour": cfg.get("theme")["colour"],
                            "footer": cfg.get("theme")["footer"]
                        })

                    
                    image_to_send = random.randint(0, amount_to_send - 1)

                    image = images_results[image_to_send]["original"]
                    res = requests.get(image)
                    if "content-type" in res.headers:
                        extension = str(mimetypes.guess_extension(res.headers["content-type"])).replace(".", "")
                        
                        if extension in ["jpeg", "png", "jpg"]:
                            new_name = str(random.randint(1000,9999)) + f".{extension}"

                            with open(f"data/cache/{new_name}", "wb") as file:
                                file.write(res.content)

                                images.append(new_name)

                    await ctx.send(files=[discord.File(f"data/cache/{image}") for image in images])

                    for image in images:
                        os.remove(f"data/cache/{image}")
        else:
            await attempting_msg.delete()
            await cmdhelper.send_message(ctx, {
                "title": "Image Search",
                "description": "The search failed, try another query.",
                "colour": "#ff0000",
                "footer": cfg.get("theme")["footer"],
            }) 

def setup(bot):
    bot.add_cog(Img(bot))