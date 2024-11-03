import discord
import os

from discord.ext import commands
from utils import config
from utils import codeblock
from utils import cmdhelper
from utils import imgembed
from utils import webhook as webhook_client
from utils import console

class Sniper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.description = cmdhelper.cog_desc("sniper", "Sniper commands")
        self.cfg = config.Config()

    @commands.command(name="sniper", description="Sniper commands.", usage="")
    async def sniper(self, ctx, selected_page: int = 1):
        cfg = config.Config()
        pages = cmdhelper.generate_help_pages(self.bot, "Sniper")

        await cmdhelper.send_message(ctx, {
            "title": f"{cfg.theme.emoji} sniper commands",
            "description": pages["image"][selected_page - 1],
            "footer": f"Page {selected_page}/{len(pages['image'])}",
            "codeblock_desc": pages["codeblock"][selected_page - 1]
        }, extra_title=f"Page {selected_page}/{len(pages['image'])}")

    @commands.command(name="snipers", description="List all snipers.", usage="")
    async def snipers(self, ctx):
        cfg = config.Config()
        snipers = cfg.get_snipers()
        snipers_str = "\n".join([f"- {sniper.name.capitalize()}: {'Enabled' if sniper.enabled else 'Disabled'}" for sniper in snipers])

        await cmdhelper.send_message(ctx, {
            "title": "Snipers",
            "description": snipers_str
        })

    @commands.command(name="sniperstatus", description="Check the status of a sniper.", usage="[sniper]")
    async def sniperstatus(self, ctx, sniper_str: str = None):
        cfg = config.Config()
        sniper = cfg.get_sniper(sniper_str.lower())

        if sniper is None:
            return await cmdhelper.send_message(ctx, {
                "title": "Error",
                "description": "Please provide a sniper to check the status.",
                "colour": "#ff0000"
            })

        await cmdhelper.send_message(ctx, {
            "title": f"{sniper.name.capitalize()} Sniper",
            "description": f"{sniper.name.capitalize()} Sniper is currently {'enabled' if sniper.enabled else 'disabled'}\nIgnore invalid codes: {sniper.ignore_invalid}",
            "colour": "#00ff00" if sniper.enabled else "#ff0000"
        })

    @commands.command(name="ignoreinvalidcodes", description="Toggle ignoring invalid codes for a sniper.", usage="[sniper]", aliases=["sniperignore", "ignoreinvalid"])
    async def ignoreinvalidcodes(self, ctx, sniper_str: str = None):
        cfg = config.Config()
        sniper = cfg.get_sniper(sniper_str.lower())

        if sniper is None:
            return await cmdhelper.send_message(ctx, {
                "title": "Error",
                "description": "Please provide a sniper to toggle ignoring invalid codes for.",
                "colour": "#ff0000"
            })
        
        sniper.toggle_ignore_invalid()
        ignore_state = sniper.ignore_invalid

        await cmdhelper.send_message(ctx, {
            "title": f"{sniper.name.capitalize()} Sniper",
            "description": f"{sniper.name.capitalize()} Sniper will now be {'ignoring' if not ignore_state else 'checking'} invalid codes."
        })

    @commands.command(name="nitrosniper", description="Toggle the Nitro sniper.", usage="[on/off]")
    async def nitrosniper(self, ctx, state: str = None):
        cfg = config.Config()
        sniper = cfg.get_sniper("nitro")
        sniper_state = sniper.enabled
        
        if state is None:
            if sniper.enabled:
                sniper.disable()
                sniper_state = False
            else:
                sniper.enable()
                sniper_state = True

            state = "on" if sniper_state else "off"

        else:
            if state.lower() not in ["on", "off"]:
                return await cmdhelper.send_message(ctx, {
                    "title": "Error",
                    "description": "Invalid state, please use `on` or `off`.",
                    "colour": "#ff0000"
                })

            if state.lower() == "on":
                sniper.enable()

            elif state.lower() == "off":
                sniper.disable()

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

    @commands.command(name="privnotesniper", description="Toggle the Privnote sniper.", usage="[on/off]")
    async def privnotesniper(self, ctx, state: str = None):
        cfg = config.Config()
        sniper = cfg.get_sniper("privnote")
        sniper_state = sniper.enabled
        
        if state is None:
            if sniper.enabled:
                sniper.disable()
                sniper_state = False
            else:
                sniper.enable()
                sniper_state = True

            state = "on" if sniper_state else "off"

        else:
            if state.lower() not in ["on", "off"]:
                return await cmdhelper.send_message(ctx, {
                    "title": "Error",
                    "description": "Invalid state, please use `on` or `off`.",
                    "colour": "#ff0000"
                })

            if state.lower() == "on":
                sniper.enable()

            elif state.lower() == "off":
                sniper.disable()

            else:
                return await cmdhelper.send_message(ctx, {
                    "title": "Error",
                    "description": "Invalid state, please use `on` or `off`.",
                    "colour": "#ff0000"
                })

        await cmdhelper.send_message(ctx, {
            "title": "Privnote Sniper",
            "description": f"Privnote sniper has been turned {state}\nGhost will now restart to apply changes.",
            "colour": "#00ff00" if sniper_state else "#ff0000"
        })

    @commands.command(name="webhooksetup", description="Setup webhooks for all snipers.", usage="", aliases=["setupwebhooks"])
    async def webhooksetup(self, ctx):
        cfg = config.Config()
        snipers = cfg.get_snipers()

        msg = await cmdhelper.send_message(ctx, {
            "title": "Webhook Setup",
            "description": "Please create a new server using the link below.",
        })
        await ctx.send("https://discord.new/sFPj3UpwJaPh", delete_after=cfg.get("message_settings")["auto_delete_delay"])
        console.print_info("Waiting for new server to be created...")

        try:
            response = await self.bot.wait_for("guild_join", timeout=30)
        except Exception as e:
            await cmdhelper.send_message(ctx, {
                "title": "Error",
                "description": "Couldn't find a new server made within the given time.",
                "colour": "#ff0000"
            })
            console.print_error("Couldn't find a new server made within the given time.")
            return
        
        if response is None:
            return await cmdhelper.send_message(ctx, {
                "title": "Error",
                "description": "Guild couldn't be found.",
                "colour": "#ff0000"
            })

        try:
            with open("ghost.png", "rb") as f:
                icon = f.read()
        except Exception as e:
            icon = None

        console.print_success("New server has been created.")
        await msg.delete()
        await response.edit(name="Ghost Webhooks", icon=icon)

        console.print_info("Setting up server...")
        for channel in response.channels:
            await channel.delete()

        main_channel = await response.create_text_channel("general")
        webhook_category = await response.create_category("Webhooks")

        for sniper in snipers:
            channel = await webhook_category.create_text_channel(sniper.name.capitalize())
            webhook = webhook_client.create_webhook(channel.id, sniper.name.capitalize())
            sniper.set_webhook(webhook)

        console.print_success("Webhooks have been setup.")
        await cmdhelper.send_message(main_channel, {
            "title": "Webhook Setup",
            "description": "Webhooks have been successfully setup.\nYou may need to restart Ghost to make sure all changes have been applied.",
            "colour": "#00ff00"
        }, delete_after=100000)

def setup(bot):
    bot.add_cog(Sniper(bot))