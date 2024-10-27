import discord
import os

from discord.ext import commands
from utils import config
from utils import codeblock
from utils import cmdhelper
from utils import imgembed

class Mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.description = cmdhelper.cog_desc("mod", "Moderation commands")
        self.cfg = config.Config()

    @commands.command(name="mod", description="Moderation commands.", aliases=["moderation"], usage="")
    async def mod(self, ctx, selected_page: int = 1):
        cfg = config.Config()
        pages = cmdhelper.generate_help_pages(self.bot, "Mod")

        if cfg.get("message_settings")["style"] == "codeblock":
            msg = codeblock.Codeblock(
                f"{cfg.get('theme')['emoji']} mod commands",
                description=pages["codeblock"][selected_page - 1],
                extra_title=f"Page {selected_page}/{len(pages['codeblock'])}"
            )

            await ctx.send(msg, delete_after=cfg.get("message_settings")["auto_delete_delay"])

        else:
            embed = imgembed.Embed(title="Moderation Commands", description=pages["image"][selected_page - 1], colour=cfg.get("theme")["colour"])
            embed.set_footer(text=f"Page {selected_page}/{len(pages['image'])}")
            embed.set_thumbnail(url=cfg.get("theme")["image"])
            embed_file = embed.save()

            await ctx.send(file=discord.File(embed_file, filename="embed.png"), delete_after=cfg.get("message_settings")["auto_delete_delay"])
            os.remove(embed_file)

    @commands.command(name="clear", description="Clear a number of messages.", aliases=["purge"], usage="[number]")
    async def clear(self, ctx, number: int):
        def is_me(m):
            if ctx.channel.permissions_for(m.author).manage_messages:
                return True
            else:
                return m.author == self.bot.user

        deleted = await ctx.channel.purge(limit=number + 1, check=is_me)
        await cmdhelper.send_message(ctx, {
            "title": "Clear",
            "description": f"Cleared {len(deleted) - 1} messages."
        })

    @commands.command(name="purgechat", description="Purge the entire chat.", usage="")
    async def purgechat(self, ctx):
        def is_me(m):
            if ctx.channel.permissions_for(m.author).manage_messages:
                return True
            else:
                return m.author == self.bot.user

        delete = await ctx.channel.purge(check=is_me)
        await cmdhelper.send_message(ctx, {
            "title": "Chat Purge",
            "description": f"Purged {len(delete)} messages."
        })

    @commands.command(name="banlist", description="List all banned members.", usage="")
    async def banlist(self, ctx):
        if not ctx.message.author.guild_permissions.administrator:
            await cmdhelper.send_message(ctx, {
                "title": "Error",
                "description": "You do not have permission to use this command.",
                "colour": "ff0000"
            })
            return

        bans = [entry async for entry in ctx.guild.bans(limit=2000)]

        if len(bans) == 0:
            await cmdhelper.send_message(ctx, {
                "title": "Banlist",
                "description": "No members are banned."
            })

        else:
            description = ""

            for ban in bans:
                description += f"{ban.user.name}\n"

            await cmdhelper.send_message(ctx, {
                "title": "Banlist",
                "description": description
            })

    @commands.command(name="ban", description="Ban a member from the command server.", usage="[member]")
    async def ban(self, ctx, member: discord.Member):

        try:
            await member.ban()
            await cmdhelper.send_message(ctx, {
                "title": "Ban",
                "description": f"Banned {member.name}#{member.discriminator}"
            })
            
        except Exception as e:
            await cmdhelper.send_message(ctx, {
                "title": "Error",
                "description": f"{e}",
                "colour": "ff0000"
            })

    @commands.command(name="kick", description="Kick a member from the command server.", usage="[member]")
    async def kick(self, ctx, member: discord.Member):
        try:
            await member.kick()
            await cmdhelper.send_message(ctx, {
                "title": "Kick",
                "description": f"Kicked {member.name}#{member.discriminator}"
            })
            
        except Exception as e:
            await cmdhelper.send_message(ctx, {
                "title": "Error",
                "description": f"{e}",
                "colour": "ff0000"
            })

def setup(bot):
    bot.add_cog(Mod(bot))