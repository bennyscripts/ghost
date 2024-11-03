@ghost.command(name="example", description="An example for the script system", usage="", aliases=["examplescript"])
async def examplescript_cmd(ctx):
    await cmdhelper.send_message(ctx, {
        "title": "Example Script",
        "description": "This is an example of a script.",
        "footer": "Example"
    })