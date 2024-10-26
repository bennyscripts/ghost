import discord
import requests
import asyncio
import random
import faker
import datetime
import os
import threading

from PIL import Image, ImageDraw, ImageFont
from discord.ext import commands
from utils import config
from utils import codeblock
from utils import cmdhelper
from utils import imgembed
from utils import soundboard
from utils import console

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cfg = config.Config()
        self.fake = faker.Faker()
        self.description = cmdhelper.cog_desc("fun", "Fun commands")

    @commands.command(name="fun", description="Fun commands.", usage="")
    async def fun(self, ctx, selected_page: int = 1):
        cfg = config.Config()
        pages = cmdhelper.generate_help_pages(self.bot, "Fun")

        if cfg.get("message_settings")["style"] == "codeblock":
            msg = codeblock.Codeblock(
                f"{cfg.get('theme')['emoji']} fun commands",
                description=pages["codeblock"][selected_page - 1],
                extra_title=f"Page {selected_page}/{len(pages['codeblock'])}"
            )

            await ctx.send(msg, delete_after=cfg.get("message_settings")["auto_delete_delay"])

        else:
            embed = imgembed.Embed(title="Fun Commands", description=pages["image"][selected_page - 1], colour=cfg.get("theme")["colour"])
            embed.set_footer(text=f"Page {selected_page}/{len(pages['image'])}")
            embed.set_thumbnail(url=cfg.get("theme")["image"])
            embed_file = embed.save()

            await ctx.send(file=discord.File(embed_file, filename="embed.png"), delete_after=cfg.get("message_settings")["auto_delete_delay"])
            os.remove(embed_file)

    @commands.command(name="rickroll", description="Never gonna give you up.", usage="")
    async def rickroll(self, ctx):
        lyrics = requests.get("https://gist.githubusercontent.com/bennyscripts/c8f9a62542174cdfb45499fdf8719723/raw/2f6a8245c64c0ea3249814ad8e016ceac45473e0/rickroll.txt").text    
        for line in lyrics.splitlines():
            await ctx.send(line)
            await asyncio.sleep(1)

    @commands.command(name="coinflip", description="Flip a coin.", aliases=["cf"])
    async def coinflip(self, ctx):
        sides = ["heads", "tails"]
        msg = await ctx.send("> Flipping the coin...")

        await asyncio.sleep(1)
        await msg.edit(content=f"> The coin landed on `{random.choice(sides)}`!")

    @commands.command(name="iq", description="Get the IQ of a user.", usage="[user]", aliases=["howsmart", "iqrating"])
    async def iq(self, ctx, *, user: discord.User):
        iq = random.randint(45, 135)
        smart_text = ""

        if iq > 90 and iq < 135:
            smart_text = "They're very smart!"
        if iq > 70 and iq < 90:
            smart_text = "They're just below average."
        if iq > 50 and iq < 70:
            smart_text = "They might have some issues."
        elif iq < 50:
            smart_text = "They're severely retarded."

        embed = discord.Embed(title=f"{user.name}'s IQ", description=f"{user.name}'s IQ is {iq}. {smart_text}")
        await cmdhelper.send_message(ctx, embed.to_dict())

    @commands.command(name="howgay", description="Get the gayness of a user.", usage="[user]", aliases=["gay", "gayrating"])
    async def howgay(self, ctx, *, user: discord.User):
        gay_percentage = random.randint(0, 100)
        
        embed = discord.Embed(title=f"how gay is {user.name}?", description=f"{user.name} is {gay_percentage}% gay!")
        await cmdhelper.send_message(ctx, embed.to_dict())

    @commands.command(name="howblack", description="Get the blackness of a user.", usage="[user]", aliases=["black", "blackrating"])
    async def howblack(self, ctx, *, user: discord.User):
        black_percentage = random.randint(0, 100)

        embed = discord.Embed(title=f"how black is {user.name}?", description=f"{user.name} is {black_percentage}% black!")
        await cmdhelper.send_message(ctx, embed.to_dict())

    @commands.command(name="pp", description="Get the size of a user's dick.", usage="[user]", aliases=["dick", "dicksize", "penis"])
    async def pp(self, ctx, *, user: discord.User):
        penis = "8" + ("=" * random.randint(0, 12)) + "D"
        inches = str(len(penis)) + "\""

        embed = discord.Embed(title=f"{user.name}'s pp size", description=f"{user.name} has a {inches} pp.\n{penis}")
        await cmdhelper.send_message(ctx, embed.to_dict())

    @commands.command(name="blocksend", description="Send a message to a blocked user.", usage="[user] [message]")
    async def blocksend(self, ctx, user: discord.User, *, message: str):
        await user.unblock()
        await user.send(message)
        await user.block()

        embed = discord.Embed(title=f"block send", description=f"Sent a message to {user.name} ({user.id}).\n**Message:** {message}")
        await cmdhelper.send_message(ctx, embed_obj=embed.to_dict())

    def get_formatted_items(self, json_obj, tabs=0):
        formatted = ""
        sub_items_count = 0

        for item in json_obj:
            if isinstance(json_obj[item], dict):
                sub_items_count += 1 + tabs
                formatted += ("\t" * tabs) + f"{item}:\n"
                formatted += self.get_formatted_items(json_obj[item], sub_items_count)
                sub_items_count = 0
            else:
                formatted += ("\t" * tabs) + f"{item}: {json_obj[item]}\n"

        return formatted

    @commands.command(name="randomdata", description="Generate random data.", usage="[type]")
    async def randomdata(self, ctx, type_name: str = "unknown"):
        url = ""
        types = [{"name": "businesscreditcard", "url": "https://random-data-api.com/api/business_credit_card/random_card"},
            {"name": "cryptocoin", "url": "https://random-data-api.com/api/crypto_coin/random_crypto_coin"},
            {"name": "hipster", "url": "https://random-data-api.com/api/hipster/random_hipster_stuff"},
            {"name": "google", "url": "https://random-data-api.com/api/omniauth/google_get"},
            {"name": "facebook", "url": "https://random-data-api.com/api/omniauth/facebook_get"},
            {"name": "twitter", "url": "https://random-data-api.com/api/omniauth/twitter_get"},
            {"name": "linkedin", "url": "https://random-data-api.com/api/omniauth/linkedin_get"},
            {"name": "github", "url": "https://random-data-api.com/api/omniauth/github_get"},
            {"name": "apple", "url": "https://random-data-api.com/api/omniauth/apple_get"}]

        for _type in types:
            if type_name == _type["name"]:
                url = _type["url"]
                break
            else:
                url = "unknown"

        if url == "unknown":
            await ctx.send(str(codeblock.Codeblock("error", extra_title="Unkown data type.", description="The current types are: " + ", ".join([_type["name"] for _type in types]))))
            return

        resp = requests.get(url)

        if resp.status_code == 200:
            data = resp.json()
            formatted = self.get_formatted_items(data)

            msg = codeblock.Codeblock("random data", extra_title=f"Random {type_name}", description=formatted, style="yaml")
            await ctx.send(str(msg))
        else:
            await ctx.send(str(codeblock.Codeblock("error", extra_title="Failed to get data.")))

    @commands.command(name="kanye", description="Random kanye quote.", usage="")
    async def kanye(self, ctx):
        resp = requests.get("https://api.kanye.rest/")

        if resp.status_code == 200:
            data = resp.json()
            embed = discord.Embed(title=f"Kanye Quote", description=data["quote"])

        else:
            embed = discord.Embed(title="Error", description="Failed to get Kanye quote.")

        await cmdhelper.send_message(ctx, embed.to_dict())

    @commands.command(name="socialcredit", description="Get a user's social credit score.", usage="[user]", aliases=["socialcreditscore", "socialcreditrating", "socialcredits", "socialrating", "socialscore"])
    async def socialcredit(self, ctx, *, user: discord.User):
        score = random.randint(-5000000, 10000000)

        embed = discord.Embed(title=f"Social Credit", description=f"{user.name}'s social credit score is {score}.")
        await cmdhelper.send_message(ctx, embed.to_dict())

    @commands.command(name="dice", description="Roll a dice with a specific side count.", usage="[sides]", aliases=["roll"])
    async def dice(self, ctx, sides: int = 6):
        cfg = config.Config()
        number = random.randint(1, sides)

        embed = discord.Embed(title=f"{sides} side dice", description=f"You rolled a {number}.")
        await cmdhelper.send_message(ctx, embed.to_dict())

    # @commands.command(name="rainbow", description="Create rainbow text.", usage="[text]", aliases=["rainbowtext"])
    # async def rainbow(self, ctx, *, text: str):
    #     # colours = {"red": {"codeblock": "diff", "prefix": "-", "suffix": ""},
    #     #     "orange": {"codeblock": "cs", "prefix": "#", "suffix": ""},
    #     #     "yellow": {"codeblock": "fix", "prefix": "", "suffix": ""},
    #     #     "green": {"codeblock": "cs", "prefix": "'", "suffix": "'",},
    #     #     "blue": {"codeblock": "md", "prefix": "#", "suffix": ""}}
        
    #     # emojis = ["🟥", "🟧", "🟨", "🟩", "🟦", "🟪"]
    #     emojis = ["🔴", "🟠", "🟡", "🟢", "🔵", "🟣"]
    #     message = await ctx.send(text)

    #     for _ in range(5):
    #         # for colour in colours:
    #         #     colour = colours[colour]
    #         #     await message.edit(content=f"""> ```{colour['codeblock']}\n> {colour['prefix']}{text}{colour['suffix']}```""")
    #         #     await asyncio.sleep(1)
    #         for emoji in emojis:
    #             await message.edit(content=f"{emoji} {text}")
    #             await asyncio.sleep(.75)

    # @commands.command(name="rainbowreact", description="Create a rainbow reaction", usage=["[msg id]"])
    # async def rainbowreact(self, ctx, *, msg_id: int):
    #     emojis = ["🟥", "🟧", "🟨", "🟩", "🟦", "🟪"]
    #     message = await ctx.fetch_message(msg_id)

    #     # await message.add_reaction("🫡")
        
    #     for _ in range(5):
    #         for emoji in emojis:
    #             reaction = await message.add_reaction(emoji)
    #             await asyncio.sleep(0.25)
    #             await message.clear_reaction(emoji)

    #     # await message.clear_reaction("🫡")

    def calculate_age(self, born):
        today = datetime.date.today()
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

    @commands.command(name="dox", description="Dox a user.", usage=["[user]"])
    async def dox(self, ctx, *, user: discord.User):
        cfg = config.Config()

        name = self.fake.name()
        email = name.lower().split(" ")[0][:random.randint(3, 5)] + "." + name.lower().split(" ")[1] + str(random.randint(10, 99)) + random.choice(["@gmail.com", "@yahoo.com", "@hotmail.com", "@outlook.com"])
        dob = datetime.date(random.randint(1982, 2010), random.randint(1, 12), random.randint(1, 28))
        age = self.calculate_age(dob)
        phone = f"+1 ({random.randint(100, 999)}) {random.randint(100, 999)}-{random.randint(1000, 9999)}"

        address_resp = requests.post("https://randommer.io/random-address", data={"number": "1", "culture": "en_US"}, headers={"content-type": "application/x-www-form-urlencoded; charset=UTF-8", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"})
        address = address_resp.json()[0]
        
        if cfg.get("message_settings")["style"] == "codeblock":
            msg = codeblock.Codeblock("dox", extra_title=f"{user.name}'s dox", description=f"""Name          :: {name}
Email         :: {email}
Date of birth :: {dob.strftime("%d/%m/%Y")}
Current age   :: {age} years old
Phone number  :: {phone}
Address       :: {address}
""")

            await ctx.send(msg)

        else:
            embed = imgembed.Embed(title=f"{user.name}'s dox", description=f"""**Name:** {name}
**Email:** {email}
**Date of birth:** {dob.strftime("%d/%m/%Y")}
**Current age:** {age} years old
**Phone number:** {phone}
**Address:** {address}
""", colour=cfg.get("theme")["colour"])
            embed.set_footer(text=cfg.get("theme")["footer"])
            embed_file = embed.save()

            await ctx.send(file=discord.File(embed_file, filename="embed.png"))
            os.remove(embed_file)

    @commands.command(name="meme", description="Gets a random meme.", aliases=["getmeme", "randommeme"], usage="")
    async def meme(self, ctx):
        r = requests.get("https://www.reddit.com/r/memes.json?sort=top&t=week", headers={"User-agent": "Mozilla/5.0"})

        if (r.status_code == 429):
            embed = discord.Embed(title="Error", description="Too many requests, please try again later.")
            await cmdhelper.send_message(ctx, embed.to_dict())
            return
        
        meme = random.choice(r.json()["data"]["children"])["data"]["url"]
        await ctx.send(meme)

    @commands.command(name="dadjoke", description="Get a dad joke.", usage="")
    async def dadjoke(self, ctx):
        r = requests.get("https://icanhazdadjoke.com/", headers={"Accept": "application/json"})
        joke = r.json()["joke"]
        await ctx.send(joke)

    @commands.command(name="insult", description="Get a random insult.", usage="")
    async def insult(self, ctx):
        r = requests.get("https://evilinsult.com/generate_insult.php?lang=en&type=json")
        insult = r.json()["insult"]
        await ctx.send(insult)

    @commands.command(name="compliment", description="Get a random compliment.", usage="")
    async def compliment(self, ctx):
        r = requests.get("https://8768zwfurd.execute-api.us-east-1.amazonaws.com/v1/compliments")
        await ctx.send(r.content.replace(b'"', b'').decode("utf-8"))

    @commands.command(name="catfact", description="Get a random cat fact.", usage="")
    async def catfact(self, ctx):
        r = requests.get("https://catfact.ninja/fact")
        fact = r.json()["fact"]
        await ctx.send(fact)

    @commands.command(name="yomomma", description="Get a yo momma joke.", usage="")
    async def yomomma(self, ctx):
        r = requests.get("https://www.yomama-jokes.com/api/v1/jokes/random/")
        joke = r.json()["joke"]
        await ctx.send(joke)

    @commands.command(name="playsound", description="Play a 5 second sound.", usage="[mp3_url]")
    async def playsound(self, ctx, mp3_url):
        cfg = config.Config()
        voice_state = ctx.author.voice

        if not ctx.author.guild_permissions.administrator:
            await cmdhelper.send_message(ctx, {
                "title": "Play Sound",
                "description": f"Admin is required for this command to work",
                "colour": "#ff0000",
                "footer": cfg.get("theme")["footer"]
            })
            return
        
        if not voice_state:
            await cmdhelper.send_message(ctx, {
                "title": "Play Sound",
                "description": f"You're not in a voice channel",
                "colour": "#ff0000",
                "footer": cfg.get("theme")["footer"]
            })
            return
        
        if not str(mp3_url).endswith("mp3"):
            await cmdhelper.send_message(ctx, {
                "title": "Play Sound",
                "description": f"That file is not an MP3",
                "colour": "#ff0000",
                "footer": cfg.get("theme")["footer"]
            })
            return
        
        sound_res = requests.get(mp3_url)
        if sound_res.status_code != 200:
            await cmdhelper.send_message(ctx, {
                "title": "Play Sound",
                "description": f"404 file not found",
                "colour": "#ff0000",
                "footer": cfg.get("theme")["footer"]
            })
            return
        
        try:
            with open("data/cache/mysound.mp3", "wb") as sound_file:
                sound_file.write(sound_res.content)

            soundeffects = soundboard.Soundboard(cfg.get("token"), ctx.guild.id, voice_state.channel.id)
            sound = soundeffects.upload_sound("data/cache/mysound.mp3", "ghost_sound_player", volume=1, emoji_id=None)

            if sound.id:
                await cmdhelper.send_message(ctx, {
                    "title": "Play Sound",
                    "description": f"Sound file is being played",
                    "colour": cfg.get("theme")["colour"],
                    "footer": cfg.get("theme")["footer"]
                })
                
                soundeffects.play_sound(sound.id, source_guild_id=ctx.guild.id)
                soundeffects.delete_sound(sound.id)
                os.remove("data/cache/mysound.mp3")

            else:
                await cmdhelper.send_message(ctx, {
                    "title": "Play Sound",
                    "description": f"Sound could not be played. Possible reasons include:\n- File is too long\n- File is over 512KB",
                    "colour": "#ff0000",
                    "footer": cfg.get("theme")["footer"]
                })
                return
            
        except Exception as e:
            await cmdhelper.send_message(ctx, {
                "title": "Play Sound",
                "description": f"Sound could not be played. Possible reasons include:\n- File is too long\n- File is over 512KB",
                "colour": "#ff0000",
                "footer": cfg.get("theme")["footer"]
            })
            return            

def setup(bot):
    bot.add_cog(Fun(bot))