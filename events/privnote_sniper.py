import discord
import requests
import time

from discord.ext import commands

from utils import console
from utils import config
from utils import notifier
from utils import privnote as privnote_client

class PrivnoteSniper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cfg = config.Config()
        self.privnote = privnote_client.Privnote()
        self.notifier = notifier.Notifier()

    async def send_webhook(self, message, sniper, success, resp):
        webhook = sniper.get_webhook()
        embed = discord.Embed(
            title="Privnote Sniper",
            colour=0x00ff00 if success else 0xff0000
        )

        if success is False:
            if sniper.ignore_invalid:
                return
            
            embed.description = f"Privnote found in {message.channel.mention} by {message.author.mention} failed to validate."
            embed.add_field(name="Reason", value=f"```{resp}```", inline=True)
        else:
            embed.description = f"Successfully read privnote found in {message.channel.mention} sent by {message.author.mention}."
            embed.add_field(name="Note", value=f"```{resp}```", inline=False)
            embed.add_field(name="OG Message", value=f"```{message.content}```", inline=False)

        embed.set_thumbnail(url=self.cfg.get("theme")["image"])
        webhook.send(embed=embed.to_dict())

    async def validate(self, code):
        full_code = code
        code, password = full_code.split("#")

        if self.privnote.read_already(code):
            return False, "Code has already been sniped."

        if len(full_code) != 18:
            return False, "Invalid code length."

        return True, None
    
    async def claim(self, code, validate=False):
        if validate is True:
            success, error = await self.validate(code)

            if success is False:
                return False, error

        try:
            success, note = self.privnote.read("https://privnote.com/" + code)
            return success, note
        except Exception as e:
            return False, str(e)

    async def snipe(self, message, sent_time):
        cfg = config.Config()
        sniper = cfg.get_sniper("privnote")

        if sniper.enabled is False:
            return

        if message.author.id == self.bot.user.id:
            return

        if "privnote.com/" in message.content:
            code = message.content.split("privnote.com/")[1].split(" ")[0]

            valid, error = await self.validate(code)
            if valid is False:
                if sniper.ignore_invalid:
                    return
                
                console.print_sniper("Privnote", f"Failed to validate privnote", {
                    "Code": code,
                    "Error": error,
                    "Hint": "You can hide this message in config.json"
                }, success=False)

            else:            
                success, resp = await self.claim(code)

                if success is False:
                    if not sniper.ignore_invalid:
                        return
                    
                    console.print_sniper("Privnote", f"Failed to claim privnote", {
                        "Code": code,
                        "Error": resp,
                        "Hint": "You can hide this message in config.json"
                    }, success=False)

                else:
                    snipe_time = time.time()
                    snipe_delta = (snipe_time - sent_time) * 1000

                    console.print_sniper("Privnote", f"Sniped privnote", {
                        "Code": code,
                        "Note": resp,
                        "Save": code.split("#")[0],
                        "Time": f"{snipe_delta:.2f}ms"
                    })

                    self.notifier.send("Privnote", f"Sniped a privnote. See console for details.")

                if sniper.webhook is not None:
                    await self.send_webhook(message, sniper, success, resp)

                self.privnote.save(resp, "https://privnote.com/" + code)

    @commands.Cog.listener()
    async def on_message(self, message):
        await self.snipe(message, time.time())

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        await self.snipe(after, time.time())

def setup(bot):
    bot.add_cog(PrivnoteSniper(bot))