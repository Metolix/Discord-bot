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

@client.slash_command(name="echo", description="Send a message through the bot!")
async def echo(ctx, text: str):
    await ctx.send("Your text has been sent.", ephemeral=True)
    await ctx.send(text, ephemeral=False)

    
    


client.run("OTY1MjU0MzI1MzM5Mjk5ODgw.GTBjJt.GldLB-EHPl3E7SXGnaZMo1q-yVGcd7kUrBmW7k")