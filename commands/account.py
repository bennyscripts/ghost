import requests
import discord
import os

from discord.ext import commands

from utils import config
from utils import codeblock
from utils import cmdhelper
from utils import imgembed

class Account(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.description = cmdhelper.cog_desc("account", "Account commands")
        self.cfg = config.Config()

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
            if cfg.get("message_settings")["style"] == "codeblock":
                await ctx.send(str(codeblock.Codeblock("Error", extra_title=f"Failed to get friend's list.")))
            else:
                embed = imgembed.Embed(title="Error", description="Failed to get friend's list.", colour=cfg.get("theme")["colour"])
                embed_file = embed.save()

                await ctx.send(file=discord.File(embed_file, filename="embed.png"))
                os.remove(embed_file)

            return

        friends = resp.json()
        friend_list = ["# friends\n"]

        for friend in friends:
            if friend["type"] == 1:
                friend_list.append(f"{friend['user']['username']}#{friend['user']['discriminator']}:{friend['user']['id']}")

        with open("friends.txt", "w") as f:
            f.write("\n".join(friend_list))
        
        if cfg.get("message_settings")["style"] == "codeblock":
            await ctx.send(str(codeblock.Codeblock("friends backup", extra_title=f"Saved {len(friend_list) - 1} friends to friends.txt")))
        else:
            embed = imgembed.Embed(title="Friends Backup", description=f"Saved {len(friend_list) - 1} friends to friends.txt", colour=cfg.get("theme")["colour"])
            embed_file = embed.save()

            await ctx.send(file=discord.File(embed_file, filename="embed.png"))
            os.remove(embed_file)

    @backup.command(name="guilds", description="Backup your guilds.", usage="", aliases=["servers"])
    async def guilds(self, ctx):
        cfg = config.Config()
        guilds = ["# guilds\n"]

        for guild in self.bot.guilds:
            guilds.append(F"{guild.name}:{guild.id}")

        with open("guilds.txt", "w") as f:
            f.write("\n".join(guilds))

        if cfg.get("message_settings")["style"] == "codeblock":
            await ctx.send(str(codeblock.Codeblock("guilds backup", extra_title=f"Saved {len(self.bot.guilds)} guilds to guilds.txt")))
        else:
            embed = imgembed.Embed(title="Guilds Backup", description=f"Saved {len(self.bot.guilds)} guilds to guilds.txt", colour=cfg.get("theme")["colour"])
            embed_file = embed.save()

            await ctx.send(file=discord.File(embed_file, filename="embed.png"))
            os.remove(embed_file)

    @backup.command(name="restore", description="Restore a backup.", usage="[backup file]")
    async def restore(self, ctx, backup_file: str):
        cfg = config.Config()
        
        if not os.path.exists(backup_file):
            if cfg.get("message_settings")["style"] == "codeblock":
                await ctx.send(str(codeblock.Codeblock("Error", extra_title=f"Backup {backup_file} doesn't exist.")))
            else:
                embed = imgembed.Embed(title="Error", description=f"Backup {backup_file} doesn't exist.", colour=cfg.get("theme")["colour"])
                embed_file = embed.save()

                await ctx.send(file=discord.File(embed_file, filename="embed.png"))
                os.remove(embed_file)
            
            return

        backup_type = ""
        backup = []

        with open(backup_file, "r") as f:
            lines = f.readlines()
            backup_type = lines[0].replace("# ", "").replace("\n", "")
            for line in lines[2:]:
                line = line.replace("\n", "").split(":")
                backup.append([line[0], line[-1]])

        print(f"{backup_type=}")
        print(f"{backup=}")

        if cfg.get("message_settings")["style"] == "codeblock":
            await ctx.send(str(codeblock.Codeblock("restore backup", extra_title=f"Restore backup is currenting a WIP feature.")))
        else:
            embed = imgembed.Embed(title="Restore Backup", description=f"Restore backup is currenting a WIP feature.", colour=cfg.get("theme")["colour"])
            embed_file = embed.save()

            await ctx.send(file=discord.File(embed_file, filename="embed.png"))
            os.remove(embed_file)

def setup(bot):
    bot.add_cog(Account(bot))