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
        cfg = config.Config()
        deleted = await ctx.channel.purge(limit=number + 1)

        if cfg.get("message_settings")["style"] == "codeblock":
            await ctx.send(codeblock.Codeblock(f"clear", extra_title=f"Purged {len(deleted) - 1} messages."), delete_after=cfg.get("message_settings")["auto_delete_delay"])

        else:
            embed = imgembed.Embed(title=f"Clear", description=f"Purged {len(deleted) - 1} messages.", colour=cfg.get("theme")["colour"])
            embed.set_footer(text=cfg.get("theme")["footer"])
            embed_file = embed.save()

            await ctx.send(file=discord.File(embed_file, filename="embed.png"), delete_after=cfg.get("message_settings")["auto_delete_delay"])
            os.remove(embed_file)

    @commands.command(name="ban", description="Ban a member from the command server.", usage="[member]")
    async def ban(self, ctx, member: discord.Member):
        cfg = config.Config()

        try:
            await member.ban()

            if cfg.get("message_settings")["style"] == "codeblock":
                await ctx.send(codeblock.Codeblock(f"ban", extra_title=f"Banned {member.name}#{member.discriminator}"), delete_after=cfg.get("message_settings")["auto_delete_delay"])

            else:
                embed = imgembed.Embed(title=f"Banned User", description=f"Banned {member.name}#{member.discriminator} from the server.", colour=cfg.get("theme")["colour"])
                embed.set_footer(text=cfg.get("theme")["footer"])
                embed_file = embed.save()

                await ctx.send(file=discord.File(embed_file, filename="embed.png"), delete_after=cfg.get("message_settings")["auto_delete_delay"])
                os.remove(embed_file)
            
        except Exception as e:
            if cfg.get("message_settings")["style"] == "codeblock":
                await ctx.send(codeblock.Codeblock(f"error", extra_title=str(e)), delete_after=cfg.get("message_settings")["auto_delete_delay"])

            else:
                embed = imgembed.Embed(title=f"Error", description=f"{e}", colour=cfg.get("theme")["colour"])
                embed.set_footer(text=cfg.get("theme")["footer"])
                embed_file = embed.save()

                await ctx.send(file=discord.File(embed_file, filename="embed.png"), delete_after=cfg.get("message_settings")["auto_delete_delay"])
                os.remove(embed_file)

    @commands.command(name="kick", description="Kick a member from the command server.", usage="[member]")
    async def kick(self, ctx, member: discord.Member):
        cfg = config.Config()

        try:
            await member.kick()

            if cfg.get("message_settings")["style"] == "codeblock":
                await ctx.send(codeblock.Codeblock(f"kick", extra_title=f"Kicked {member.name}#{member.discriminator}"), delete_after=cfg.get("message_settings")["auto_delete_delay"])

            else:
                embed = imgembed.Embed(title=f"Kicked User", description=f"Kicked {member.name}#{member.discriminator} from the server.", colour=cfg.get("theme")["colour"])
                embed.set_footer(text=cfg.get("theme")["footer"])
                embed_file = embed.save()

                await ctx.send(file=discord.File(embed_file, filename="embed.png"), delete_after=cfg.get("message_settings")["auto_delete_delay"])
                os.remove(embed_file)
            
        except Exception as e:
            if cfg.get("message_settings")["style"] == "codeblock":
                await ctx.send(codeblock.Codeblock(f"error", extra_title=str(e)), delete_after=cfg.get("message_settings")["auto_delete_delay"])

            else:
                embed = imgembed.Embed(title=f"Error", description=f"{e}", colour=cfg.get("theme")["colour"])
                embed.set_footer(text=cfg.get("theme")["footer"])
                embed_file = embed.save()

                await ctx.send(file=discord.File(embed_file, filename="embed.png"), delete_after=cfg.get("message_settings")["auto_delete_delay"])
                os.remove(embed_file)

def setup(bot):
    bot.add_cog(Mod(bot))