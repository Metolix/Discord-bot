import disnake as discord
from disnake.ext import commands

client = commands.InteractionBot()

@client.event
async def on_ready():
    print("Ready!")


@client.slash_command(name="ping", description="Get the latency of bot.")
async def ping(ctx):
    latency = round(client.latency * 1000)
    await ctx.send(f"Pong! The ping is `{latency}` ms", ephemeral=False)

@client.slash_command(name="echo", description="Send a text message through the bot")
@commands.has_permissions(Administrator = True)
async def echo(ctx, text:str):
    await ctx.send("Text Sent!", ephemeral=True)
    await ctx.send(text, ephemeral=False)
@echo.error()
async def error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.reply("**__Missing Required Permissions__**. The command you tried to use requires permission you do not have, What a fool... (~~DM the dev if there is a mistake~~)")


client.run("OTY1MjU0MzI1MzM5Mjk5ODgw.GTBjJt.GldLB-EHPl3E7SXGnaZMo1q-yVGcd7kUrBmW7k")