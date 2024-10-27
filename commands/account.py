import requests
import discord
import os
import json
import asyncio
import time

from discord.ext import commands
from discord.utils import get

from utils import config
from utils import codeblock
from utils import cmdhelper
from utils import imgembed
from utils import console

class Account(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.description = cmdhelper.cog_desc("account", "Account commands")
        self.cfg = config.Config()
        self.headers = {
            "Authorization": f"{self.cfg.get('token')}",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    @commands.command(name="account", description="Account commands.", aliases=["acc"], usage="")
    async def account(self, ctx, selected_page: int = 1):
        cfg = config.Config()
        pages = cmdhelper.generate_help_pages(self.bot, "Account")

        if cfg.get("message_settings")["style"] == "codeblock":
            msg = codeblock.Codeblock(
                f"{cfg.get('theme')['emoji']} account commands",
                description=pages["codeblock"][selected_page - 1],
                extra_title=f"Page {selected_page}/{len(pages['codeblock'])}"
            )

            await ctx.send(msg, delete_after=cfg.get("message_settings")["auto_delete_delay"])

        else:
            embed = imgembed.Embed(title="Account Commands", description=pages["image"][selected_page - 1], colour=cfg.get("theme")["colour"])
            embed.set_footer(text=f"Page {selected_page}/{len(pages['image'])}")
            embed.set_thumbnail(url=cfg.get("theme")["image"])
            embed_file = embed.save()

            await ctx.send(file=discord.File(embed_file, filename="embed.png"), delete_after=cfg.get("message_settings")["auto_delete_delay"])
            os.remove(embed_file)

    @commands.command(name="hypesquad", description="Change your hypesquad.", usage="[hypesquad]", aliases=["changehypesquad"])
    async def hypesquad(self, ctx, house: str):
        houses = {
            "bravery": "1",
            "brilliance": "2",
            "balance": "3"
        }
        house = house.lower()

        if house not in houses:
            await cmdhelper.send_message(ctx, {"title": "Error", "description": f"Invalid house. Please choose from Bravery, Brilliance and Balance.", "colour": "ff0000"})
            return
        
        resp = requests.post("https://discord.com/api/v9/hypesquad/online", headers=self.headers, json={"house_id": houses[house]})

        if resp.status_code != 204:
            await cmdhelper.send_message(ctx, {"title": "Error", "description": f"Failed to change hypesquad. {resp.status_code} {resp.text}", "colour": "ff0000"})
            return
        
        await cmdhelper.send_message(ctx, {"title": "Hypesquad", "description": f"Changed hypesquad to {house}."})

    @commands.command(name="status", description="Change your status.", usage="[status]", aliases=["changestatus"])
    async def status(self, ctx, status: str):
        statuses = {
            "online": "online",
            "idle": "idle",
            "dnd": "dnd",
            "invisible": "invisible"
        }
        status = status.lower()

        if status not in statuses:
            await cmdhelper.send_message(ctx, {"title": "Error", "description": f"Invalid status. Please choose from Online, Idle, DND and Invisible.", "colour": "ff0000"})
            return
        
        await self.bot.change_presence(status=discord.Status.try_value(status))
        await cmdhelper.send_message(ctx, {"title": "Status", "description": f"Changed status to {status}."})

    @commands.command(name="customstatus", description="Change your custom status.", usage="[status]", aliases=["changecustomstatus"])
    async def customstatus(self, ctx, *, status: str):
        status = discord.CustomActivity(name=status)
        await self.bot.change_presence(activity=status)
        await cmdhelper.send_message(ctx, {"title": "Custom Status", "description": f"Changed custom status to {status}."})

    @commands.command(name="clearstatus", description="Clear your custom status.", usage="")
    async def clearstatus(self, ctx):
        await self.bot.change_presence(activity=None)
        await cmdhelper.send_message(ctx, {"title": "Clear Status", "description": "Cleared custom status."})

    @commands.command(name="playing", description="Change your playing status.", usage="[status]", aliases=["changeplaying"])
    async def playing(self, ctx, *, status: str):
        game = discord.Game(status)
        await self.bot.change_presence(activity=game)
        await cmdhelper.send_message(ctx, {"title": "Playing Status", "description": f"Changed playing status to {status}."})

    @commands.command(name="streaming", description="Change your streaming status.", usage="[status]", aliases=["changestreaming"])
    async def streaming(self, ctx, *, status: str):
        stream = discord.Streaming(name=status, url="https://twitch.tv/ghost")
        await self.bot.change_presence(activity=stream)
        await cmdhelper.send_message(ctx, {"title": "Streaming Status", "description": f"Changed streaming status to {status}."})

    @commands.command(name="backups", description="List your backups.", usage="")
    async def backups(self, ctx):
        if not os.path.exists("backups/"):
            os.mkdir("backups/")

        backups = os.listdir("backups/")

        if len(backups) == 0:
            await cmdhelper.send_message(ctx, {"title": "Backups", "description": "No backups found.", "colour": "ff0000"})
            return
        
        description = ""
        for backup in backups:
            if backup.endswith(".json"):
                description += f"{backup}\n"

        await cmdhelper.send_message(ctx, {"title": "Backups", "description": description})
            
    @commands.group(name="backup", description="Backup commands.", usage="")
    async def backup(self, ctx):
        cfg = config.Config()

        if ctx.invoked_subcommand is None:
            description = ""
            for sub_command in self.backup.commands:
                if cfg.get("message_settings")["style"] == "codeblock":
                    description += f"backup {sub_command.name} :: {sub_command.description}\n"
                else:
                    description += f"**{self.bot.command_prefix}backup {sub_command.name}** {sub_command.description}\n"
            
            if cfg.get("message_settings")["style"] == "codeblock":
                msg = codeblock.Codeblock(
                    f"{cfg.get('theme')['emoji']} backup commands",
                    description=description
                )

                await ctx.send(msg, delete_after=cfg.get("message_settings")["auto_delete_delay"])

            else:
                embed = imgembed.Embed(title="Backup Commands", description=description, colour=cfg.get("theme")["colour"])
                embed.set_thumbnail(url=cfg.get("theme")["image"])
                embed_file = embed.save()

                await ctx.send(file=discord.File(embed_file, filename="embed.png"), delete_after=cfg.get("message_settings")["auto_delete_delay"])
                os.remove(embed_file)

    @backup.command(name="friends", description="Backup your friends.", usage="")
    async def friends(self, ctx):
        cfg = config.Config()
        resp = requests.get("https://discord.com/api/users/@me/relationships", headers={
            "Authorization": f"{cfg.get('token')}",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        })

        if resp.status_code != 200:
            await cmdhelper.send_message(ctx, {"title": "Error", "description": f"Failed to get friends. {resp.status_code} {resp.text}"})
            return

        friends = resp.json()
        backup = {
            "created_at": time.time(),
            "type": "friends",
            "list": []
        }

        for friend in friends:
            if friend["type"] == 1:
                backup["list"].append({
                    "username": friend['user']['username'],
                    "id": friend['user']['id']
                })

        if not os.path.exists("backups/"):
            os.mkdir("backups/")

        with open("backups/friends.json", "w") as f:
            f.write(json.dumps(backup))
        
        await cmdhelper.send_message(ctx, {"title": "Friends Backup", "description": f"Saved {len(friends)} friends to friends.json"})

    @backup.command(name="guilds", description="Backup your guilds.", usage="", aliases=["servers"])
    async def guilds(self, ctx):
        cfg = config.Config()
        backup = {
            "created_at": time.time(),
            "type": "guilds",
            "list": []
        }

        for guild in self.bot.guilds:
            invite = None

            for channel in guild.channels:
                if channel.type == discord.ChannelType.text:
                    try:
                        invite = await channel.create_invite(max_age=0, max_uses=1, unique=True, validate=False, reason="sharing to a friend")
                        console.print_success(f"Created and saved an invite for {guild.name}")
                    except Exception as e:
                        invite = None
                        console.print_error(f"Failed to create invite for {guild.name}")
                    break

            backup["list"].append({
                "name": guild.name,
                "id": guild.id,
                "invite": str(invite)
            })
            
            await asyncio.sleep(1)

        if not os.path.exists("backups/"):
            os.mkdir("backups/")

        with open("backups/guilds.json", "w") as f:
            f.write(json.dumps(backup))

        await cmdhelper.send_message(ctx, {"title": "Guilds Backup", "description": f"Saved {len(self.bot.guilds)} guilds to guilds.json"})

    @backup.command(name="restore", description="Restore a backup.", usage="[backup]")
    async def restore(self, ctx, backup: str):
        if not os.path.exists("backups/"):
            os.mkdir("backups/")
        backup_path = f"backups/{backup}.json"
        cfg = config.Config()
        headers = {
                    "Authorization": f"{cfg.get('token')}",
                    "Content-Type": "application/json",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
                }

        if not os.path.exists(backup_path):
            await cmdhelper.send_message(ctx, {"title": "Error", "description": f"Backup {backup} doesn't exist.", "colour": "ff0000"})
            return
            
        # if not backup.endswith(".json"):
        #     await cmdhelper.send_message(ctx, {"title": "Error", "description": f"Backup {backup} is not a JSON file.", "colour": "ff00000"})
        #     return
        
        await cmdhelper.send_message(ctx, {"title": "WARNING", "description": f"Restore backup is currenting a WIP feature. This could also result in your account getting banned! Please use with caution. Look at the console for backup progress.", "colour": "ebde34"})
        
        with open(backup_path, "r") as f:
            backup = json.loads(f.read())

        if backup["type"] == "friends":
            for friend in backup["list"]:
                user_resp = requests.get(f"https://discord.com/api/v9/users/{friend['id']}", headers=headers)
                if user_resp.status_code != 200:
                    console.print_error(f"Failed to get {friend['username']}.")
                    return

                user = discord.User(state=self.bot._connection, data=user_resp.json())
                
                try:
                    user.send_friend_request()
                except Exception as e:
                    console.print_error(f"Failed to add {friend['username']}.")
                    console.print_error(e)
                    return
                
                console.print_success(f"Added {friend['username']}!")
                await asyncio.sleep(1)

            await cmdhelper.send_message(ctx, {"title": "Restore Backup", "description": f"Restored {len(backup['list'])} friends. They have been sent a friend request."})

        elif backup["type"] == "guilds":
            invites = [guild["invite"] for guild in backup["list"]]
            invites = [invite for invite in invites if invite != "None"]
            await cmdhelper.send_message(ctx, {"title": "Restore Backup", "description": f"I'm unable to automatically join guilds. Please manually join the following guilds. This will delete in {cfg.get('message_settings')['auto_delete_delay']} seconds."})
            await ctx.send("\n".join(invites), delete_after=cfg.get("message_settings")["auto_delete_delay"])

        else:
            await cmdhelper.send_message(ctx, {"title": "Error", "description": f"Unknown backup type {backup['type']}. Ghost backup restore only supports backups made using Ghost.", "colour": "ff0000"})

def setup(bot):
    bot.add_cog(Account(bot))