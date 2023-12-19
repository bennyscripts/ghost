@ghost.command(name="filesay", description="Sends a message for each line in a file", usage="[path]", aliases=["sayfile"])
async def filesay_cmd(ctx, path: str):
    cfg = config.Config()

    if not os.path.isfile(path):
        if cfg.get("message_settings")["style"] == "codeblock":
            msg = codeblock.Codeblock(title=f"filesay", extra_title=f"File {path} not found.")
            await ctx.send(msg, delete_after=cfg.get("message_settings")["auto_delete_delay"])

        else:
            embed = imgembed.Embed(title="", description=f"File **{path}** not found.", colour=cfg.get("theme")["colour"])
            embed.set_footer(text=cfg.get("theme")["footer"])
            embed_file = embed.save()

            await ctx.send(file=discord.File(embed_file, filename="embed.png"), delete_after=cfg.get("message_settings")["auto_delete_delay"])
            os.remove(embed_file)

    else:
        with open(path, "r") as f:
            for line in f:
                await ctx.send(line)