import disnake as discord
from disnake.ext import commands

client = commands.Bot(command_prefix="?")

@client.event
async def on_ready():
    print("Ready!")


@client.slash_command(name="ping",description="E")
async def ping(ctx):
    await ctx.send("lol", ephemeral=False)

@client.slash_command(name="echo")
async def echo(ctx,* ,text):
    await ctx.send("Your text has been sent.", ephemeral=True)
    await ctx.send(text, ephemeral=False)

    
    


client.run("OTY1MjU0MzI1MzM5Mjk5ODgw.GTBjJt.GldLB-EHPl3E7SXGnaZMo1q-yVGcd7kUrBmW7k")