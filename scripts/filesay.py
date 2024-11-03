@ghost.command(name="filesay", description="Sends a message for each line in a file", usage="[path]", aliases=["sayfile"])
async def filesay_cmd(ctx, path: str):
    with open(path, "r") as f:
        lines = f.readlines()

    for line in lines:
        await ctx.send(line)
        await asyncio.sleep(.84)