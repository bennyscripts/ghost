import discord
import requests
import time

from discord.ext import commands

from utils import console
from utils import config
from utils import notifier

class NitroSniper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cfg = config.Config()
        self.cfg.check()
        self.notifier = notifier.Notifier()
        self.headers = {
            "Authorization": f"{self.cfg.get('token')}",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    async def validate(self, code):
        cfg = config.Config()

        if cfg.check_sniped_code(code):
            return False, "Code has already been sniped."

        if len(code) != 16:
            return False, "Invalid code length."

        return True, None
    
    async def claim(self, code, validate=False):
        if validate is True:
            success, error = await self.validate(code)

            if success is False:
                return False, error

        r = requests.post(
            f"https://discord.com/api/v8/entitlements/gift-codes/{code}/redeem",
            headers=self.headers
        )

        if r.status_code == 400:
            return False, r.json()["message"]

        return True, r.json()

    async def snipe(self, message, sent_time):
        cfg = config.Config()

        if cfg.get_sniper_status("nitro") is False:
            return

        if message.author.id == self.bot.user.id:
            return

        if "discord.gift/" in message.content:
            code = message.content.split("discord.gift/")[1].split(" ")[0]

            valid, error = await self.validate(code)
            if valid is False:
                if cfg.snipers_ignore_invalid("nitro"):
                    return
                
                console.print_sniper("Nitro", f"Failed to validate nitro gift", {
                    "Code": code,
                    "Error": error,
                    "Hint": "You can hide this message in config.json"
                }, success=False)

            else:            
                success, resp = await self.claim(code)
                snipe_time = time.time()
                snipe_delta = (snipe_time - sent_time) * 1000

                if "redeemed already" in resp.lower():
                    if cfg.snipers_ignore_invalid("nitro"):
                        return
                    
                    console.print_sniper("Nitro", "Failed to claim nitro gift", {
                        "Code": code,
                        "Error": resp,
                        "Hint": "You can hide this message in config.json"
                    }, success=False)

                else:
                    console.print_sniper("Nitro", "Failed to claim nitro." if not success else "Successfully claimed nitro code!", {
                        "Code": code,
                        "Author": message.author,
                        "Content": message.content,
                        "Nitro Type": resp["subscription_plan"]["name"] if success else "N/A",
                        "Time": f"{snipe_delta:.2f}ms"
                    }, success=success)

            cfg.add_nitro_snipe(code)

    @commands.Cog.listener()
    async def on_message(self, message):
        await self.snipe(message, time.time())

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        await self.snipe(after, time.time())

def setup(bot):
    bot.add_cog(NitroSniper(bot))