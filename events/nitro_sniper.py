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
        self.notifier = notifier.Notifier()
        self.headers = {
            "Authorization": f"{self.cfg.get('token')}",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    async def save_code(self, code):
        if await self.check_code(code):
            return
        
        with open("data/sniped_codes.txt", "a") as f:
            f.write(f"{code}\n")

    async def check_code(self, code):
        with open("data/sniped_codes.txt", "r") as f:
            return code in f.read()
        
    async def send_webhook(self, message, sniper, code, success, resp, snipe_delta):
        webhook = sniper.get_webhook()
        embed = discord.Embed(
            title="Nitro Sniper",
            colour=0x00ff00 if success else 0xff0000
        )

        if success is False:
            if sniper.ignore_invalid:
                return
            
            # embed.add_field(name="Error", value=f"```{resp}```", inline=False)
            embed.description = f"Nitro code found in {message.channel.mention} by {message.author.mention} failed to validate."
            embed.add_field(name="Reason", value=f"```{resp['message']}```", inline=True)
        else:
            embed.description = f"Successfully claimed nitro code found in {message.channel.mention} sent by {message.author.mention}."
            embed.add_field(name="Time", value=f"```{snipe_delta:.2f}ms```", inline=True)
            embed.add_field(name="Code", value=f"```{code}```", inline=True)
            embed.add_field(name="Type", value=f"```{resp['subscription_plan']['name']}```", inline=False)
            embed.add_field(name="Content", value=f"```{message.content}```", inline=False)

        embed.set_thumbnail(url=self.cfg.get("theme")["image"])
        webhook.send(embed=embed.to_dict())

    async def validate(self, code):
        if await self.check_code(code):
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
            return False, r.json()

        return True, r.json()

    async def snipe(self, message, sent_time):
        cfg = config.Config()
        sniper = cfg.get_sniper("nitro")

        if sniper.enabled is False:
            return

        if message.author.id == self.bot.user.id:
            return

        if "discord.gift/" in message.content:
            code = message.content.split("discord.gift/")[1].split(" ")[0]
            valid, error = await self.validate(code)
            
            if valid is False:
                if sniper.ignore_invalid:
                    return await self.save_code(code)
                
                console.print_sniper("Nitro", f"Failed to validate nitro gift", {
                    "Code": code,
                    "Error": error,
                    "Hint": "You can hide this message in config.json"
                }, success=False)

            else:            
                success, resp = await self.claim(code)
                snipe_time = time.time()
                snipe_delta = (snipe_time - sent_time) * 1000
                subscription_plan = "N/A"

                if "subscription_plan" in resp:
                    subscription_plan = resp["subscription_plan"]["name"]
                else:
                    resp["subscription_plan"] = {"name": "N/A"}

                if "redeemed already" in str(resp).lower() or "unknown gift code" in str(resp).lower():
                    if not sniper.ignore_invalid:                    
                        console.print_sniper("Nitro", "Failed to claim nitro gift", {
                            "Code": code,
                            "Error": resp["message"],
                            "Hint": "You can hide this message in config.json"
                        }, success=False)

                    success=False

                else:
                    console.print_sniper("Nitro", "Failed to claim nitro." if not success else "Successfully claimed nitro code!", {
                        "Code": code,
                        "Author": message.author,
                        "Content": message.content,
                        "Nitro Type": subscription_plan,
                        "Time": f"{snipe_delta:.2f}ms"
                    }, success=success)

                    if success:
                        self.notifier.send("Nitro", f"Sniped a nitro gift. See console for details.")

                if sniper.webhook is not None:
                    await self.send_webhook(message, sniper, code, success, resp, snipe_delta)

            await self.save_code(code)

    @commands.Cog.listener()
    async def on_message(self, message):
        await self.snipe(message, time.time())

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        await self.snipe(after, time.time())

def setup(bot):
    bot.add_cog(NitroSniper(bot))