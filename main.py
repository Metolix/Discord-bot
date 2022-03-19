import nextcord as discord
from nextcord.ext import commands
import os
import random
import DiscordEconomy

TOKEN = os.getenv('TOKEN')

client = commands.Bot(command_prefix='??')

@client.event
async def on_ready():
    print('------')
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('Prefix is ??')
    print('------')

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('**__Command Not Found__**. Use ??help to see all commands.')
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('**__Missing Permissions__**. You do not have permission to use this command.')
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('**__Missing Required Argument__**. You are missing a required argument.')
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"**__Command On Cooldown__**. You are on cooldown for this command. Please try again in {error.retry_after:.2f}s")
    else:
        raise error


@client.command()
async def ping(ctx):    
    print(f"Ping requested by {ctx.author}.")
    latency = round(client.latency * 1000)
    print(f"Latency = {latency}ms")
    await ctx.reply(f"Pong! The ping is `{latency}`ms")
    print("Command successfully executed.")

@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    if member.bot:
        await ctx.reply("You cannot warn a bot")
    else:
        print(f"Ban requested by {ctx.author}.")
        await member.ban(reason=reason)
        await ctx.reply(f"{member} has been banned.")
        print("Command successfully executed.")

@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    if member.bot:
        await ctx.reply("You cannot warn a bot")
    else:
        print(f"Kick requested by {ctx.author}.")
        await member.kick(reason=reason)
        await ctx.reply(f"{member} has been kicked.")
        print("Command successfully executed.")

@client.command()
@commands.has_permissions(manage_messages=True)
async def warn(ctx, member: discord.Member, *, reason=None):
    if member.bot:
        await ctx.reply("You cannot warn a bot")
    else:
        print(f"Warn requested by {ctx.author}.")
        await member.send(f"You have been warned in {ctx.guild.name} for {reason}")
        await ctx.reply(f"{member} has been warned..")
        print("Command successfully executed.")


player1 = ""
player2 = ""
turn = ""
gameOver = True

board = []

winningConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]

@client.command()
async def tictactoe(ctx, p1: discord.Member, p2: discord.Member):
    global count
    global player1
    global player2
    global turn
    global gameOver

    if gameOver:
        global board
        board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:"]
        turn = ""
        gameOver = False
        count = 0

        player1 = p1
        player2 = p2

        # print the board
        line = ""
        for x in range(len(board)):
            if x == 2 or x == 5 or x == 8:
                line += " " + board[x]
                await ctx.send(line)
                line = ""
            else:
                line += " " + board[x]

        # determine who goes first
        num = random.randint(1, 2)
        if num == 1:
            turn = player1
            await ctx.send("It is <@" + str(player1.id) + ">'s turn.")
        elif num == 2:
            turn = player2
            await ctx.send("It is <@" + str(player2.id) + ">'s turn.")
    else:
        await ctx.send("A game is already in progress! Finish it before starting a new one.")

@client.command()
async def place(ctx, pos: int):
    global turn
    global player1
    global player2
    global board
    global count
    global gameOver

    if not gameOver:
        mark = ""
        if turn == ctx.author:
            if turn == player1:
                mark = ":regional_indicator_x:"
            elif turn == player2:
                mark = ":o2:"
            if 0 < pos < 10 and board[pos - 1] == ":white_large_square:" :
                board[pos - 1] = mark
                count += 1

                # print the board
                line = ""
                for x in range(len(board)):
                    if x == 2 or x == 5 or x == 8:
                        line += " " + board[x]
                        await ctx.send(line)
                        line = ""
                    else:
                        line += " " + board[x]

                checkWinner(winningConditions, mark)
                print(count)
                if gameOver == True:
                    await ctx.send(mark + " wins!")
                elif count >= 9:
                    gameOver = True
                    await ctx.send("It's a tie!")

                # switch turns
                if turn == player1:
                    turn = player2
                elif turn == player2:
                    turn = player1
            else:
                await ctx.send("Be sure to choose an integer between 1 and 9 (inclusive) and an unmarked tile.")
        else:
            await ctx.send("It is not your turn.")
    else:
        await ctx.send("Please start a new game using the !tictactoe command.")


def checkWinner(winningConditions, mark):
    global gameOver
    for condition in winningConditions:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            gameOver = True

@tictactoe.error
async def tictactoe_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please mention 2 players for this command.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to mention/ping players (ie. <@688534433879556134>).")

@place.error
async def place_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please enter a position you would like to mark.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to enter an integer.")

@client.command()
async def slap(ctx, member: discord.Member):
    if member.id == 807146991179399178:
        await ctx.reply("NO!")
    else:
        things = ["Bat", "Hand", "Dogs poop", "100 Pound hand"]
        await ctx.reply(f"{ctx.author.name} Slaped {member.name} with {random.choice(things)}!")
        
async def is_registered(ctx):
    r = await economy.is_registered(ctx.message.author.id)
    return r


economy = DiscordEconomy.Economy()

is_registered = commands.check(is_registered)

items_list = {
    "Items": {
        "Car": {
            "available": False,
            "price": 300,
            "description": "Drive long distances with this car.",
        },
        "fishing rod": {
            "available": False,
            "price": 1200,
            "description": "FISH FISH!"
        },
        "pickaxe": {
            "available": False,
            "price": 1500,
            "description": "Mine!"
        },
        "sword": {
            "available": False,
            "price": 700,
            "description": "Hunt"
        }
    }}



@client.command()
@is_registered
async def balance(ctx: commands.Context, member: discord.Member = None):
    if not member:
        member = ctx.message.author

    user_account = await economy.get_user(member.id)

    embed = discord.Embed(
        colour=discord.Color.from_rgb(244, 182, 89)
    )
    embed.add_field(name=f"{member.display_name}'s balance", value=f"""Bank: **{user_account.bank}**
                                                                     Wallet: **{user_account.wallet}**
                                                                     Items: **{user_account.items}**""")
    embed.set_footer(text=f"Invoked by {ctx.message.author.name}")
    await ctx.send(embed=embed)


@client.command()
@commands.cooldown(1, 3600, commands.BucketType.user)
@is_registered
async def reward(ctx: commands.Context):
    random_amount = random.randint(50, 150)
    await economy.add_money(ctx.message.author.id, "wallet", random_amount)
    embed = discord.Embed(
        colour=discord.Color.from_rgb(244, 182, 89)
    )
    embed.add_field(name=f"Reward", value=f"Successfully claimed reward!")
    embed.set_footer(text=f"Invoked by {ctx.message.author.name}")
    await ctx.send(embed=embed)


@client.command()
@is_registered
async def coinflip(ctx: commands.Context, money: int, arg: str):
    arg = arg.lower()
    random_arg = random.choice(["tails", "heads"])
    multi_money = money * 2
    r = await economy.get_user(ctx.message.author.id)
    embed = discord.Embed(
        colour=discord.Color.from_rgb(244, 182, 89)
    )
    if r.bank >= money:
        if arg == random_arg:
            await economy.add_money(ctx.message.author.id, "bank", multi_money)

            embed.add_field(name="Coinflip", value=f"You won coinflip! - {random_arg}")
            embed.set_footer(text=f"Invoked by {ctx.message.author.name}")
            await ctx.send(embed=embed)
        else:
            await economy.remove_money(ctx.message.author.id, "bank", money)

            embed.add_field(name="Coinflip", value=f"You lost coinflip! - {random_arg}")
            embed.set_footer(text=f"Invoked by {ctx.message.author.name}")
            await ctx.send(embed=embed)

    else:
        embed.add_field(name="Coinflip", value=f"You don't have enough money!")
        embed.set_footer(text=f"Invoked by {ctx.message.author.name}")
        await ctx.send(embed=embed)


@client.command()
@is_registered
async def slots(ctx: commands.Context, money: int):
    money_multi = money * 2
    random_slots_data = ["", "", "",
                         "", "", "",
                         "", "", ""]
    i = 0
    for _ in random_slots_data:
        random_slots_data[i] = random.choice([":tada:", ":cookie:", ":large_blue_diamond:",
                                              ":money_with_wings:", ":moneybag:", ":cherries:"])

        i += 1
        if i == len(random_slots_data):
            break
    r = await economy.get_user(ctx.message.author.id)
    embed = discord.Embed(
        colour=discord.Color.from_rgb(244, 182, 89)
    )
    if r.bank >= money:

        embed.add_field(name="Slots", value=f"""{random_slots_data[0]} | {random_slots_data[1]} | {random_slots_data[2]}
                                                {random_slots_data[3]} | {random_slots_data[4]} | {random_slots_data[5]}
                                                {random_slots_data[6]} | {random_slots_data[7]} | {random_slots_data[8]}
                                            """)
        embed.set_footer(text=f"Invoked by {ctx.message.author.name}")
        await ctx.send(embed=embed)
        if random_slots_data[3] == random_slots_data[4] and random_slots_data[5] == random_slots_data[3]:
            await economy.add_money(ctx.message.author.id, "bank", money_multi)
            await ctx.send("You won!")
        else:
            await economy.remove_money(ctx.message.author.id, "bank", money)
            await ctx.send("You loss!")

    else:
        embed.add_field(name="Slots", value=f"You don't have enough money!")
        embed.set_footer(text=f"Invoked by {ctx.message.author.name}")
        await ctx.send(embed=embed)


@client.command()
@is_registered
async def withdraw(ctx: commands.Context, money: int):
    r = await economy.get_user(ctx.message.author.id)
    embed = discord.Embed(
        colour=discord.Color.from_rgb(244, 182, 89)
    )

    if r.bank >= money:
        await economy.add_money(ctx.message.author.id, "wallet", money)
        await economy.remove_money(ctx.message.author.id, "bank", money)

        embed.add_field(name="Withdraw", value=f"Successfully withdrawn {money} money!")
        embed.set_footer(text=f"Invoked by {ctx.message.author.name}")
        await ctx.send(embed=embed)

    else:

        embed.add_field(name="Withdraw", value=f"You don't have enough money to withdraw!")
        embed.set_footer(text=f"Invoked by {ctx.message.author.name}")
        await ctx.send(embed=embed)


@client.command()
@is_registered
async def deposit(ctx: commands.Context, money: int):
    r = await economy.get_user(ctx.message.author.id)
    embed = discord.Embed(
        colour=discord.Color.from_rgb(244, 182, 89)
    )

    if r.wallet >= money:
        await economy.add_money(ctx.message.author.id, "bank", money)
        await economy.remove_money(ctx.message.author.id, "wallet", money)

        embed.add_field(name="Deposit", value=f"Successfully deposited {money} money!")
        embed.set_footer(text=f"Invoked by {ctx.message.author.name}")
        await ctx.send(embed=embed)

    else:

        embed.add_field(name="Deposit", value=f"You don't have enough money to deposit!")
        embed.set_footer(text=f"Invoked by {ctx.message.author.name}")
        await ctx.send(embed=embed)


@client.group(invoke_without_command=True)
@is_registered
async def shop(ctx: commands.Context):
    embed = discord.Embed(
        colour=discord.Color.from_rgb(244, 182, 89)
    )

    embed.add_field(name="Shop", value=f"In the shop you can buy and sell items!", inline=False)
    embed.add_field(name="Available commands", value=f"""?shop buy <item>
                                                         ?shop sell <item>
                                                         ?shop items""", inline=False)
    embed.set_footer(text=f"Invoked by {ctx.message.author.name}")
    await ctx.send(embed=embed)


@shop.command()
@is_registered
async def items(ctx: commands.Context):
    embed = discord.Embed(
        colour=discord.Color.from_rgb(244, 182, 89)
    )
    embed.set_author(name="Items")
    for item in items_list["Items"].items():
        embed.add_field(name=item[0].capitalize(), value=item[1]["description"] + "\n_ _" + "\n" +
                                                         f"Price: **{item[1]['price']}**" + "\n"
                                                         + f"Available: **{item[1]['available']}**")

        embed.set_footer(text=f"Invoked by {ctx.message.author.name}")
    await ctx.send(embed=embed)


@shop.command()
@is_registered
async def buy(ctx: commands.Context, *, _item: str):
    _item = _item.lower()
    _cache = []
    embed = discord.Embed(
        colour=discord.Color.from_rgb(244, 182, 89)
    )

    for item in items_list["Items"].items():
        if item[0] == _item:
            _cache.append(item[0])

            r = await economy.get_user(ctx.message.author.id)

            if item[0] in r.items:
                embed.add_field(name="Error", value=f"You already have that item!")
                embed.set_footer(text=f"Invoked by {ctx.message.author.name}")
                await ctx.send(embed=embed)

                return

            if r.bank >= item[1]["price"]:
                await economy.add_item(ctx.message.author.id, item[0])
                await economy.remove_money(ctx.message.author.id, "bank", item[1]["price"])

                embed.add_field(name="Success", value=f"Successfully bought **{item[0]}**!")
                embed.set_footer(text=f"Invoked by {ctx.message.author.name}",
                            )
                await ctx.send(embed=embed)

            else:

                embed.add_field(name="Error", value=f"You don't have enought money to buy this item!")
                embed.set_footer(text=f"Invoked by {ctx.message.author.name}",
                            )
                await ctx.send(embed=embed)
            break

    if len(_cache) <= 0:
        embed.add_field(name="Error", value="Item with that name does not exists!")
        await ctx.send(embed=embed)


@shop.command()
@is_registered
async def sell(ctx: commands.Context, *, _item: str):
    r = await economy.get_user(ctx.message.author.id)

    _item = _item.lower()

    embed = discord.Embed(
        colour=discord.Color.from_rgb(244, 182, 89)
    )

    if _item in r.items:
        for item in items_list["Items"].items():
            if item[0] == _item:
                item_prc = item[1]["price"] / 2

                await economy.add_money(ctx.message.author.id, "bank", item_prc)
                await economy.remove_item(ctx.message.author.id, item[0])

                embed.add_field(name="Success", value=f"Successfully sold **{item[0]}**!")
                await ctx.send(embed=embed)
                break
    else:

        embed.add_field(name="Error", value=f"You don't have this item!")
        await ctx.send(embed=embed)

client.run("OTUxMzU3NjM1MzQzNTQ4NDE2.YimS1w.MK2pi4PKgUmcw8riWU4tZwG-Fy8")