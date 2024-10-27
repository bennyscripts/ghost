import discord
import os
import requests

from discord.ext import commands
from utils import config
from utils import codeblock
from utils import cmdhelper
from utils import shortener
from utils import imgembed

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.description = cmdhelper.cog_desc("info", "Info commands")
        self.cfg = config.Config()

    @commands.command(name="info", description="Information commands.", aliases=["information"], usage="")
    async def info(self, ctx, selected_page: int = 1):
        cfg = config.Config()
        pages = cmdhelper.generate_help_pages(self.bot, "Info")

        if cfg.get("message_settings")["style"] == "codeblock":
            msg = codeblock.Codeblock(
                f"{cfg.get('theme')['emoji']} info commands",
                description=pages["codeblock"][selected_page - 1],
                extra_title=f"Page {selected_page}/{len(pages['codeblock'])}"
            )

            await ctx.send(msg, delete_after=cfg.get("message_settings")["auto_delete_delay"])

        else:
            embed = imgembed.Embed(title="Info Commands", description=pages["image"][selected_page - 1], colour=cfg.get("theme")["colour"])
            embed.set_footer(text=f"Page {selected_page}/{len(pages['image'])}")
            embed.set_thumbnail(url=cfg.get("theme")["image"])
            embed_file = embed.save()

            await ctx.send(file=discord.File(embed_file, filename="embed.png"), delete_after=cfg.get("message_settings")["auto_delete_delay"])
            os.remove(embed_file)

    @commands.command(name="iplookup", description="Look up an IP address.", usage="[ip]", aliases=["ipinfo"])
    async def iplookup(self, ctx, ip):
        response = requests.get(f"https://ipapi.co/{ip}/json/").json()

        info = {
            "IP": response["ip"],
            "City": response["city"],
            "Region": response["region"],
            "Country": response["country"],
            "Postal": response["postal"],
            "Latitude": response["latitude"],
            "Longitude": response["longitude"],
            "Timezone": response["timezone"],
            "Org": response["org"]
        }

        longest_key = max([len(key) for key in info.keys()])

        await cmdhelper.send_message(ctx, {
            "title": "IP Lookup",
            "description": "\n".join([f"**{key}:** {value}" for key, value in info.items()]),
            "codeblock_desc": "\n".join([f"{key}{' ' * (longest_key - len(key))} :: {value}" for key, value in info.items()])
        })

    @commands.command(name="userinfo", description="Get information about a user.", aliases=["ui"], usage="[user]")
    async def userinfo(self, ctx, user: discord.User = None):
        if user is None: user = ctx.author

        info = {
            "ID": user.id,
            "Username": user.name,
            "Bot": user.bot,
            "System": user.system,
            "Created at": user.created_at
        }

        if ctx.guild is not None:
            user = ctx.guild.get_member(user.id)
            info["Nickname"] = user.nick
            info["Joined at"] = user.joined_at
            # info["Desktop status"] = user.desktop_status
            # info["Mobile status"] = user.mobile_status
            # info["Web status"] = user.web_status
            info["Status"] = user.status
            info["In VC"] = user.voice
            # info["Premium"] = user.premium

        longest_key = max([len(key) for key in info.keys()])

        await cmdhelper.send_message(ctx, {
            "title": "User Info",
            "description": "\n".join([f"**{key}:** {value}" for key, value in info.items()]),
            "codeblock_desc": "\n".join([f"{key}{' ' * (longest_key - len(key))} :: {value}" for key, value in info.items()]),
            "thumbnail": user.avatar.url
        })

    @commands.command(name="serverinfo", description="Get information about the server.", aliases=["si"], usage="")
    async def serverinfo(self, ctx):
        info = {
            "ID": ctx.guild.id,
            "Name": ctx.guild.name,
            "Owner": ctx.guild.owner,
            # "Region": ctx.guild.region,
            "Members": len(ctx.guild.members),
            "Roles": len(ctx.guild.roles),
            "Channels": len(ctx.guild.channels),
            "Created at": ctx.guild.created_at
        }

        await cmdhelper.send_message(ctx, {
            "title": "Server Info",
            "description": "\n".join([f"**{key}:** {value}" for key, value in info.items()]),
            "codeblock_desc": "\n".join([f"{key}{' ' * (10 - len(key))} :: {value}" for key, value in info.items()]),
            "thumbnail": ctx.guild.icon.url
        })

    @commands.command(name="webhookinfo", description="Get information about a webhook.", aliases=["wi"], usage="[webhook url]")
    async def webhookinfo(self, ctx, webhook_url):
        try:
            webhook = discord.Webhook.from_url(webhook_url, session=self.bot._connection)
        except:
            await cmdhelper.send_message(ctx, {
                "title": "Error",
                "description": "Invalid webhook URL.",
                "colour": "#ff0000"
            })
            return

        info = {
            "ID": webhook.id,
            "Name": webhook.name,
            "Channel": webhook.source_channel,
            "Guild": webhook.source_guild,
            "Token": "Attached below"
        }

        await cmdhelper.send_message(ctx, {
            "title": "Webhook Info",
            "description": "\n".join([f"**{key}:** {value}" for key, value in info.items()]),
            "thumbnail": ""
        }, extra_message="```" + webhook.token + "```")

    @commands.command(name="avatar", description="Get the avatar of a user.", aliases=["av"], usage="[user]")
    async def avatar(self, ctx, user: discord.User = None):
        cfg = config.Config()

        if user is None:
            user = ctx.author

        if cfg.get("message_settings")["style"] == "codeblock":
            await ctx.send(str(codeblock.Codeblock(title="avatar", extra_title=str(user))) + user.avatar.url, delete_after=cfg.get("message_settings")["auto_delete_delay"])

        else:
            embed = imgembed.Embed(title=f"{user.name}'s avatar", description="The link has been added above for a higher quality image.", colour=cfg.get("theme")["colour"])
            embed.set_thumbnail(url=str(user.avatar.url))
            embed.set_footer(text=cfg.get("theme")["footer"])
            embed_file = embed.save()

            await ctx.send(content=f"<{user.avatar.url}>", file=discord.File(embed_file, filename="embed.png"), delete_after=cfg.get("message_settings")["auto_delete_delay"])
            os.remove(embed_file)

    @commands.command(name="tickets", description="Get a list of all tickets available in the server.")
    async def tickets(self, ctx):
        tickets = []

        for channel in ctx.guild.channels:
            if str(channel.type) == "text":
                if "ticket" in channel.name.lower():
                    tickets.append(f"#{channel.name}")
        
        await cmdhelper.send_message(ctx, {
            "title": "Tickets",
            "description": "\n".join(tickets) if tickets else "There were no tickets found."
        })

    @commands.command(name="hiddenchannels", description="List all hidden channels.", aliases=["privchannels", "privatechannels"])
    async def hiddenchannels(self, ctx):
        channels = []

        for channel in ctx.guild.channels:
            if str(channel.type) == "text":
                if channel.overwrites_for(ctx.author.top_role).read_messages == False:
                    channels.append(f"#{channel.name}")

        await cmdhelper.send_message(ctx, {
            "title": "Hidden Channels",
            "description": "\n".join(channels) if channels else "There were no hidden channels found."
        })

def setup(bot):
    bot.add_cog(Info(bot))