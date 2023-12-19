@ghost.command(name="example", description="An example for the script system", usage="", aliases=["examplescript"])
async def examplescript_cmd(ctx):
    cfg = config.Config()

    if cfg.get("message_settings")["style"] == "codeblock":
        msg = codeblock.Codeblock(title=f"example", extra_title=f"This is an example script.")
        await ctx.send(msg, delete_after=cfg.get("message_settings")["auto_delete_delay"])

    else:
        embed = imgembed.Embed(title="Example", description=f"This is an example script.", colour=cfg.get("theme")["colour"])
        embed.set_footer(text=cfg.get("theme")["footer"])
        embed_file = embed.save()

        await ctx.send(file=discord.File(embed_file, filename="embed.png"), delete_after=cfg.get("message_settings")["auto_delete_delay"])
        os.remove(embed_file)