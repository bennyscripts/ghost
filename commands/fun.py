import discord
import requests
import asyncio
import random
import faker
import datetime
import os

from PIL import Image, ImageDraw, ImageFont
from discord.ext import commands
from utils import config
from utils import codeblock
from utils import cmdhelper
from utils import imgembed
from utils import soundboard

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
        lyrics = requests.get("https://gist.githubusercontent.com/bentettmar/c8f9a62542174cdfb45499fdf8719723/raw/2f6a8245c64c0ea3249814ad8e016ceac45473e0/rickroll.txt").text    
        for line in lyrics.splitlines():
            await ctx.send(line)
            await asyncio.sleep(1)

    @commands.command(name="coinflip", description="Flip a coin.", aliases=["cf"])
    async def coinflip(self, ctx):
        sides = ["heads", "tails"]
        msg = await ctx.send("> Flipping the coin...")

        await asyncio.sleep(1)
        for i in range(random.randint(len(sides), 5)):
            if i % len(sides) == 0:
                i = 0

            await msg.edit(content="> " + sides[i].capitalize() + "...")
            await asyncio.sleep(1)

        await msg.edit(content=f"> The coin landed on `{random.choice(sides)}`!")

    @commands.command(name="iq", description="Get the IQ of a user.", usage="[user]", aliases=["howsmart", "iqrating"])
    async def iq(self, ctx, *, user: discord.User):
        cfg = config.Config()
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

        if cfg.get("message_settings")["style"] == "codeblock":
            msg = codeblock.Codeblock("iq", extra_title=f"{user.name}'s IQ is {iq}. {smart_text}")
            await ctx.send(msg, delete_after=cfg.get("message_settings")["auto_delete_delay"])

        else:
            embed = imgembed.Embed(title=f"{user.name}'s iq", description=f"{user.name}'s IQ is {iq}. {smart_text}", colour=cfg.get("theme")["colour"])
            embed.set_footer(text=cfg.get("theme")["footer"])
            embed_file = embed.save()

            await ctx.send(file=discord.File(embed_file, filename="embed.png"), delete_after=cfg.get("message_settings")["auto_delete_delay"])
            os.remove(embed_file)

    @commands.command(name="howgay", description="Get the gayness of a user.", usage="[user]", aliases=["gay", "gayrating"])
    async def howgay(self, ctx, *, user: discord.User):
        cfg = config.Config()
        gay_percentage = random.randint(0, 100)
        msg = codeblock.Codeblock("how gay", extra_title=f"{user.name} is {gay_percentage}% gay.")

        if cfg.get("message_settings")["style"] == "codeblock":
            msg = codeblock.Codeblock("how gay", extra_title=f"{user.name} is {gay_percentage}% gay.")
            await ctx.send(msg, delete_after=cfg.get("message_settings")["auto_delete_delay"])

        else:
            embed = imgembed.Embed(title=f"how gay is {user.name}?!", description=f"{user.name} is {gay_percentage}% gay.", colour=cfg.get("theme")["colour"])
            embed.set_footer(text=cfg.get("theme")["footer"])
            embed_file = embed.save()

            await ctx.send(file=discord.File(embed_file, filename="embed.png"), delete_after=cfg.get("message_settings")["auto_delete_delay"])
            os.remove(embed_file)

    @commands.command(name="howblack", description="Get the blackness of a user.", usage="[user]", aliases=["black", "blackrating"])
    async def howblack(self, ctx, *, user: discord.User):
        cfg = config.Config()
        black_percentage = random.randint(0, 100)

        if cfg.get("message_settings")["style"] == "codeblock":
            msg = codeblock.Codeblock("how black", extra_title=f"{user.name} is {black_percentage}% black.")
            await ctx.send(msg, delete_after=cfg.get("message_settings")["auto_delete_delay"])

        else:
            embed = imgembed.Embed(title=f"how black is {user.name}?!", description=f"{user.name} is {black_percentage}% black.", colour=cfg.get("theme")["colour"])
            embed.set_footer(text=cfg.get("theme")["footer"])
            embed_file = embed.save()

            await ctx.send(file=discord.File(embed_file, filename="embed.png"), delete_after=cfg.get("message_settings")["auto_delete_delay"])
            os.remove(embed_file)

    @commands.command(name="pp", description="Get the size of a user's dick.", usage="[user]", aliases=["dick", "dicksize", "penis"])
    async def pp(self, ctx, *, user: discord.User):
        cfg = config.Config()
        penis = "8" + ("=" * random.randint(0, 12)) + "D"
        inches = str(len(penis)) + "\""

        if cfg.get("message_settings")["style"] == "codeblock":
            msg = codeblock.Codeblock("pp", extra_title=f"{user.name} has a {inches} dick.", description=penis)
            await ctx.send(msg, delete_after=cfg.get("message_settings")["auto_delete_delay"])

        else:
            embed = imgembed.Embed(title=f"{user.name}'s dick size", description=f"{user.name} has a {inches} dick.\n{penis}", colour=cfg.get("theme")["colour"])
            embed.set_footer(text=cfg.get("theme")["footer"])
            embed_file = embed.save()

            await ctx.send(file=discord.File(embed_file, filename="embed.png"), delete_after=cfg.get("message_settings")["auto_delete_delay"])
            os.remove(embed_file)

    @commands.command(name="blocksend", description="Send a message to a blocked user.", usage="[user] [message]")
    async def blocksend(self, ctx, user: discord.User, *, message: str):
        cfg = config.Config()
        
        await user.unblock()
        await user.send(message)
        await user.block()

        if cfg.get("message_settings")["style"] == "codeblock":
            msg = codeblock.Codeblock("block send", extra_title=f"Sent a message to {user.name} ({user.id})", description=f"Message :: {message}")
            await ctx.send(msg, delete_after=cfg.get("message_settings")["auto_delete_delay"])

        else:
            embed = imgembed.Embed(title=f"block send", description=f"Sent a message to {user.name} ({user.id}).\n**Message:** {message}", colour=cfg.get("theme")["colour"])
            embed.set_footer(text=cfg.get("theme")["footer"])
            embed_file = embed.save()

            await ctx.send(file=discord.File(embed_file, filename="embed.png"), delete_after=cfg.get("message_settings")["auto_delete_delay"])
            os.remove(embed_file)

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
        cfg = config.Config()
        resp = requests.get("https://api.kanye.rest/")

        if resp.status_code == 200:
            data = resp.json()

            if cfg.get("message_settings")["style"] == "codeblock":
                msg = codeblock.Codeblock("kanye", extra_title=data["quote"])
                await ctx.send(msg, delete_after=cfg.get("message_settings")["auto_delete_delay"])

            else:
                embed = imgembed.Embed(title=f"Kanye Quote", description=data["quote"], colour=cfg.get("theme")["colour"])
                embed.set_footer(text=cfg.get("theme")["footer"])
                embed_file = embed.save()

                await ctx.send(file=discord.File(embed_file, filename="embed.png"), delete_after=cfg.get("message_settings")["auto_delete_delay"])
                os.remove(embed_file)

        else:
            if cfg.get("message_settings")["style"] == "codeblock":
                msg = codeblock.Codeblock("error", extra_title="Failed to get data.")
                await ctx.send(msg, delete_after=cfg.get("message_settings")["auto_delete_delay"])

            else:
                embed = imgembed.Embed(title=f"Error", description="Failed to get data.", colour=cfg.get("theme")["colour"])
                embed.set_footer(text=cfg.get("theme")["footer"])
                embed_file = embed.save()

                await ctx.send(file=discord.File(embed_file, filename="embed.png"), delete_after=cfg.get("message_settings")["auto_delete_delay"])
                os.remove(embed_file)

    @commands.command(name="socialcredit", description="Get a user's social credit score.", usage="[user]", aliases=["socialcreditscore", "socialcreditrating", "socialcredits", "socialrating", "socialscore"])
    async def socialcredit(self, ctx, *, user: discord.User):
        cfg = config.Config()
        score = random.randint(-5000000, 10000000)

        if cfg.get("message_settings")["style"] == "codeblock":
            msg = codeblock.Codeblock("social credit", extra_title=f"{user.name}'s social credit score is {score}.")
            await ctx.send(msg, delete_after=cfg.get("message_settings")["auto_delete_delay"])

        else:
            embed = imgembed.Embed(title=f"Social Credit", description=f"{user.name}'s social credit score is {score}.", colour=cfg.get("theme")["colour"])
            embed.set_footer(text=cfg.get("theme")["footer"])
            embed_file = embed.save()

            await ctx.send(file=discord.File(embed_file, filename="embed.png"), delete_after=cfg.get("message_settings")["auto_delete_delay"])
            os.remove(embed_file)

    @commands.command(name="dice", description="Roll a dice with a specific side count.", usage="[sides]", aliases=["roll"])
    async def dice(self, ctx, sides: int = 6):
        cfg = config.Config()
        number = random.randint(1, sides)

        if cfg.get("message_settings")["style"] == "codeblock":
            msg = codeblock.Codeblock(f"{sides} side dice", extra_title=f"You rolled a {number}.")
            await ctx.send(msg, delete_after=cfg.get("message_settings")["auto_delete_delay"])

        else:
            embed = imgembed.Embed(title=f"{sides} side dice", description=f"You rolled a {number}.", colour=cfg.get("theme")["colour"])
            embed.set_footer(text=cfg.get("theme")["footer"])
            embed_file = embed.save()

            await ctx.send(file=discord.File(embed_file, filename="embed.png"), delete_after=cfg.get("message_settings")["auto_delete_delay"])
            os.remove(embed_file)

    @commands.command(name="rainbow", description="Create rainbow text.", usage="[text]", aliases=["rainbowtext"])
    async def rainbow(self, ctx, *, text: str):
        colours = {"red": {"codeblock": "diff", "prefix": "-", "suffix": ""},
            "orange": {"codeblock": "cs", "prefix": "#", "suffix": ""},
            "yellow": {"codeblock": "fix", "prefix": "", "suffix": ""},
            "green": {"codeblock": "cs", "prefix": "'", "suffix": "'",},
            "blue": {"codeblock": "md", "prefix": "#", "suffix": ""}}
        
        message = await ctx.send(text)

        for _ in range(3):
            for colour in colours:
                colour = colours[colour]
                await message.edit(content=f"""> ```{colour['codeblock']}\n> {colour['prefix']}{text}{colour['suffix']}```""")
                await asyncio.sleep(1)

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

            await ctx.send(msg, delete_after=cfg.get("message_settings")["auto_delete_delay"])

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

            await ctx.send(file=discord.File(embed_file, filename="embed.png"), delete_after=cfg.get("message_settings")["auto_delete_delay"])
            os.remove(embed_file)


    # @commands.command(name="creditcard", description="Generate a users credit card.", usage="[user]", aliases=["cc"])
    # async def creditcard(self, ctx, *, user: discord.User):
    #     card_number = random.randint(1000000000000000, 9999999999999999)
    #     card_number = " ".join([str(card_number)[i:i+4] for i in range(0, len(str(card_number)), 4)])

    #     background = Image.open("data/cc-template.png")
    #     draw = ImageDraw.Draw(background)

    #     draw.text((100, 340), user.name, (255, 255, 255), font=ImageFont.truetype("data/fonts/comicsans.ttf", 36), stroke_width=8, stroke_fill=(207, 131, 0))
    #     draw.text((100, 250), card_number, (255, 255, 255), font=ImageFont.truetype("data/fonts/comicsans.ttf", 50), stroke_width=8, stroke_fill=(207, 131, 0))

    #     background.save("cc-edited.png")

    #     await ctx.send(file=discord.File("cc-edited.png"))
    #     os.remove("cc-edited.png")

    @commands.command(name="meme", description="Gets a random meme.", aliases=["getmeme", "randommeme"], usage="")
    async def meme(self, ctx):
        cfg = config.Config()
        r = requests.get("https://www.reddit.com/r/memes.json?sort=top&t=week", headers={"User-agent": "Mozilla/5.0"})
        if (r.status_code == 429):
            if cfg.get("message_settings")["style"] == "codeblock":
                await ctx.send(f"```ini\n[ error ] Too many requests, please try again later.\n```", delete_after=cfg.get("message_settings")["auto_delete_delay"])
            else:
                embed = imgembed.Embed(title="Error", description=f"Too many requests, please try again later.")
                embed_file = embed.save()

                await ctx.send(file=discord.File(embed_file, filename="embed.png"), delete_after=cfg.get("message_settings")["auto_delete_delay"])
                os.remove(embed_file)
            return
        meme = random.choice(r.json()["data"]["children"])["data"]["url"]
        await ctx.send(meme)

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