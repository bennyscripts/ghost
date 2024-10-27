import discord
import os

from discord.ext import commands
from utils import config
from utils import codeblock
from utils import cmdhelper
from utils import imgembed

class Sniper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.description = cmdhelper.cog_desc("sniper", "Sniper commands")
        self.cfg = config.Config()

    @commands.command(name="sniper", description="Sniper commands.", usage="")
    async def sniper(self, ctx, selected_page: int = 1):
        cfg = config.Config()
        pages = cmdhelper.generate_help_pages(self.bot, "Sniper")

        if cfg.get("message_settings")["style"] == "codeblock":
            msg = codeblock.Codeblock(
                f"{cfg.get('theme')['emoji']} sniper commands",
                description=pages["codeblock"][selected_page - 1],
                extra_title=f"Page {selected_page}/{len(pages['codeblock'])}"
            )

            await ctx.send(msg, delete_after=cfg.get("message_settings")["auto_delete_delay"])

        else:
            embed = imgembed.Embed(title="Sniper Commands", description=pages["image"][selected_page - 1], colour=cfg.get("theme")["colour"])
            embed.set_footer(text=f"Page {selected_page}/{len(pages['image'])}")
            embed.set_thumbnail(url=cfg.get("theme")["image"])
            embed_file = embed.save()

            await ctx.send(file=discord.File(embed_file, filename="embed.png"), delete_after=cfg.get("message_settings")["auto_delete_delay"])
            os.remove(embed_file)

    @commands.command(name="snipers", description="List all snipers.", usage="")
    async def snipers(self, ctx):
        cfg = config.Config()
        snipers = cfg.get_snipers()

        await cmdhelper.send_message(ctx, {
            "title": "Snipers",
            "description": "\n".join([f"- {sniper.capitalize()}: {'Enabled' if cfg.get_sniper_status(sniper) else 'Disabled'}" for sniper in snipers]),
            "colour": cfg.get("theme")["colour"]
        })

    @commands.command(name="sniperstatus", description="Check the status of a sniper.", usage="[sniper]")
    async def sniperstatus(self, ctx, sniper: str = None):
        cfg = config.Config()

        if sniper is None:
            return await cmdhelper.send_message(ctx, {
                "title": "Error",
                "description": "Please provide a sniper to check the status of.",
                "colour": "#ff0000"
            })

        if sniper.lower() not in cfg.get_snipers():
            return await cmdhelper.send_message(ctx, {
                "title": "Error",
                "description": "Invalid sniper, please use `nitro`.",
                "colour": "#ff0000"
            })

        sniper_status = cfg.get_sniper_status(sniper.lower())
        sniper_ignore_invalid = cfg.snipers_ignore_invalid(sniper.lower())

        await cmdhelper.send_message(ctx, {
            "title": f"{sniper.capitalize()} Sniper",
            "description": f"{sniper.capitalize()} Sniper is currently {'enabled' if sniper_status else 'disabled'}\nIgnore invalid codes: {sniper_ignore_invalid}",
            "colour": "#00ff00" if sniper_status else "#ff0000"
        })

    @commands.command(name="ignoreinvalidcodes", description="Toggle ignoring invalid codes for a sniper.", usage="[sniper]", aliases=["sniperignore"])
    async def ignoreinvalidcodes(self, ctx, sniper: str = None):
        cfg = config.Config()

        if sniper is None:
            return await cmdhelper.send_message(ctx, {
                "title": "Error",
                "description": "Please provide a sniper to toggle ignoring invalid codes for.",
                "colour": "#ff0000"
            })

        if sniper.lower() not in cfg.get_snipers():
            return await cmdhelper.send_message(ctx, {
                "title": "Error",
                "description": "Invalid sniper, please use `nitro`.",
                "colour": "#ff0000"
            })

        ignore_state = cfg.toggle_snipers_ignore_invalid(sniper.lower())
        state = "on" if ignore_state else "off"

        await cmdhelper.send_message(ctx, {
            "title": f"{sniper.capitalize()} Sniper",
            "description": f"{sniper.capitalize()} Sniper will now be {'ignoring' if ignore_state else 'checking'} invalid codes."
        })

    @commands.command(name="nitrosniper", description="Toggle the Nitro sniper.", usage="[on/off]")
    async def nitrosniper(self, ctx, state: str = None):
        cfg = config.Config()
        
        if state is None:
            sniper_state = cfg.toggle_sniper("nitro")
            state = "on" if sniper_state else "off"

        else:
            if state.lower() not in ["on", "off"]:
                return await cmdhelper.send_message(ctx, {
                    "title": "Error",
                    "description": "Invalid state, please use `on` or `off`.",
                    "colour": "#ff0000"
                })

            if state.lower() == "on":
                cfg.enable_sniper("nitro")

            elif state.lower() == "off":
                cfg.disable_sniper("nitro")

            else:
                return await cmdhelper.send_message(ctx, {
                    "title": "Error",
                    "description": "Invalid state, please use `on` or `off`.",
                    "colour": "#ff0000"
                })

        await cmdhelper.send_message(ctx, {
            "title": "Nitro Sniper",
            "description": f"Nitro sniper has been turned {state}\nGhost will now restart to apply changes.",
            "colour": "#00ff00" if sniper_state else "#ff0000"
        })

        await self.bot.get_cog("Util").restart(ctx)

def setup(bot):
    bot.add_cog(Sniper(bot))