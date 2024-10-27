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

class Abuse(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cfg = config.Config()
        self.fake = faker.Faker()
        self.description = cmdhelper.cog_desc("abuse", "Abusive commands")

    @commands.command(name="abuse", description="Abusive commands.", usage="")
    async def abuse(self, ctx, selected_page: int = 1):
        cfg = config.Config()
        pages = cmdhelper.generate_help_pages(self.bot, "Abuse")

        if cfg.get("message_settings")["style"] == "codeblock":
            msg = codeblock.Codeblock(
                f"{cfg.get('theme')['emoji']} abuse commands",
                description=pages["codeblock"][selected_page - 1],
                extra_title=f"Page {selected_page}/{len(pages['codeblock'])}"
            )

            await ctx.send(msg, delete_after=cfg.get("message_settings")["auto_delete_delay"])

        else:
            embed = imgembed.Embed(title="Abuse Commands", description=pages["image"][selected_page - 1], colour=cfg.get("theme")["colour"])
            embed.set_footer(text=f"Page {selected_page}/{len(pages['image'])}")
            embed.set_thumbnail(url=cfg.get("theme")["image"])
            embed_file = embed.save()

            await ctx.send(file=discord.File(embed_file, filename="embed.png"), delete_after=cfg.get("message_settings")["auto_delete_delay"])
            os.remove(embed_file)

    @commands.command(name="servernuke", description="Nuke a server.", usage="", aliases=["nukeserver"])
    async def servernuke(self, ctx):
        if ctx.author.guild_permissions.administrator:
            for channel in ctx.guild.channels:
                try:
                    await channel.delete()
                    await asyncio.sleep(.25)
                except:
                    pass

            for role in ctx.guild.roles:
                try:
                    await role.delete()
                    await asyncio.sleep(.25)
                except:
                    pass

            try:
                await ctx.guild.edit(name="Nuked by " + ctx.author.name)
            except:
                pass

            for _ in range(250):
                await ctx.guild.create_text_channel(name="Nuked by " + ctx.author.name)
                await asyncio.sleep(.25)

    @commands.command(name="channelspam", description="Flood a channel with a message of your choosing.", usage="[msg amount] [message]")
    async def channelspam(self, ctx, msg_amount: int, *, message: str):
        for _ in range(msg_amount):
            await ctx.send(f"> ** **\n> # {message}\n> ** **")
            await asyncio.sleep(.5)

    @commands.command(name="channelping", description="Ping a user in every available channel.", usage=["[user] [ping amount]"])
    async def channelping(self, ctx, users: str, ping_amount: int = 1, threaded: bool = False):
        headers  = {"Authorization": self.cfg.get("token"), "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"}
        base_url = "https://discord.com/api"

        async def delete_message(channel_id, message_id):
            try:
                resp = requests.delete(f"{base_url}/channels/{channel_id}/messages/{message_id}", headers=headers)

                while "retry_after" in resp.json() or resp.status_code == 429:
                    await asyncio.sleep(resp.json()["retry_after"])
                    resp = requests.delete(f"{base_url}/channels/{channel_id}/messages/{message_id}", headers=headers)
                
                return resp
            except Exception as e:
                return e

        async def channelping_thread(channel, user, ping_amount, delay):
            for _ in range(ping_amount):  
                resp = requests.post(f"{base_url}/channels/{channel.id}/messages", json={"content": f"{users}"}, headers=headers)

                if "retry_after" in resp.json():
                    console.print_warning(f"Rated limited in #{channel.name}")
                else:
                    console.print_info(f"Sent ping to #{channel.name}!")

                await delete_message(channel.id, resp.json()["id"])
                await asyncio.sleep(1)

                if ping_amount > 1:
                    if delay > 2:
                        console.print_info(f"Waiting {delay} seconds...")
                    await asyncio.sleep(delay)

        def channelping_thread_middleman(channel, user, ping_amount, delay):
            asyncio.run(channelping_thread(channel, user, ping_amount, delay))

        channels         = []
        threads          = []
        default_delay    = 2

        for channel in ctx.guild.channels:
            if str(channel.type) == "text":
                if channel.permissions_for(ctx.guild.me).send_messages:
                    channels.append(channel)
                    
        console.print_info(f"Sending {len(channels) * ping_amount} pings...")

        if threaded:
            for channel in channels:
                _thread = threading.Thread(
                    target=channelping_thread_middleman, 
                    args=(
                        channel, 
                        users, 
                        ping_amount, 
                        channel.slowmode_delay if channel.slowmode_delay > default_delay else default_delay, 
                        ), 
                    daemon=True
                )
                
                threads.append(_thread)

            for thread in threads:
                thread.start()
                # await asyncio.sleep(2)

            for thread in threads:
                thread.join()
                # await asyncio.sleep(2)
        else:
            for channel in channels:
                await channelping_thread(channel, users, ping_amount, channel.slowmode_delay if channel.slowmode_delay > default_delay else default_delay)

        print()
        console.print_info("All pings done! Clearing console in 15 seconds...")
        await asyncio.sleep(15)
        os.system("clear")
        print()
        console.print_banner()

def setup(bot):
    bot.add_cog(Abuse(bot))