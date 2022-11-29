import discord
from discord.ext import commands
from discord.utils import get
import os
import random
from random import randrange
import time
import sys
from datetime import datetime
import aiohttp

#---initialize---#
TOKEN = open('token.txt', 'r').readline()
prefix = '>','<'
client = commands.Bot(command_prefix=prefix, intents=discord.Intents.all())
client.remove_command('help')
cooldown = 3


#---methods---#
def restart_program():
    python = sys.executable
    os.execl(python, python, * sys.argv)

def listToString(list):
    str1 = ""
    for ele in list:
        str1 += ele
    return str1

#------------BOT BEGIN------------#

#---event based---#
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="you >help"))
    print("we ballin'!")

#---error checking---#
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CommandNotFound):
        await ctx.channel.send(f"{ctx.author.mention} whoops! i don't have this command... type '>help' to see what i can do")
        #raise error
    elif isinstance(error, commands.errors.CommandOnCooldown):
        await ctx.channel.send(f"{ctx.author.mention} shhh! command is on cooldown... (wait "+str(cooldown)+"s)")
        #raise error
    elif isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.channel.send(f"{ctx.author.mention} you've entered no arguments... type '>help' to see what i need for it")
        #raise error
    elif isinstance(error, commands.errors.TooManyArguments):
        await ctx.channel.send(f"{ctx.author.mention} you've entered too many arguments... type '>help' to see how it works")
        #raise error
    elif isinstance(error, commands.errors.BadArgument) or isinstance(error, commands.errors.ArgumentParsingError):
        await ctx.channel.send(f"{ctx.author.mention} you've entered a bad argument... type '>help' to see what you need")
        #raise error

    else:
        await ctx.channel.send(f"{ctx.author.mention} whoops! looks like something went wrong...")
        raise error
    #if isinstance(error, commands.errors.BotMissingPermissions):
    #    await ctx.channel.send(f"{ctx.author.mention} i don't have permission to do this... i need: ".join(commands.errors.BotMissingPermissions.args))

    


#---owner commands---#
@client.command()
@commands.is_owner()
async def restart(ctx):
    await ctx.channel.send("restarting...")
    time.sleep(1)
    restart_program()

@client.command()
@commands.is_owner()
async def stop(ctx):
    await ctx.channel.send("shutting down...")
    time.sleep(1)
    exit(0)

@client.command()
@commands.is_owner()
async def info(ctx):
    embed = discord.Embed(color=discord.Color.green())
    embed.set_author(name='information about the bot')
    embed.add_field(name='botname: ', value=client.user.name, inline=False)
    embed.add_field(name='botID: ', value=str(client.user.id), inline=False)
    embed.add_field(name='connected with:\n', value=str("\n".join(guild.name for guild in client.guilds)), inline=True)
    embed.add_field(name='IDs:\n', value=str("\n".join([str(guild.id) for guild in client.guilds])), inline=True)
    await ctx.author.send(embed=embed)

@client.command()
@commands.is_owner()
async def ownerhelp(ctx):
    embed = discord.Embed(color=discord.Color.blue())
    embed.set_author(name="i see you need help...")

    file = open('ownerhelp.txt', 'r')
    ownerhelp = file.readlines()

    embed.add_field(name="here's what you (as the owner) can do:", value=listToString(ownerhelp), inline=False)
    
    await ctx.author.send(embed=embed)

@client.command()
@commands.is_owner()
async def leave(ctx, serverID : int):
    toleave = client.get_guild(serverID)
    await ctx.author.send(f"i left the server with the id: " + str(serverID))
    await discord.Guild.leave(toleave)

@client.command()
@commands.is_owner()
async def invite(ctx):
    await ctx.author.send(f"invite link https://discord.com/api/oauth2/authorize?client_id=1045966904235397130&permissions=8&scope=bot")

#---user commands---#

                                                                                
   ##   #      #####     ####   ####  #    # #    #   ##   #    # #####   ####  
  #  #  #        #      #    # #    # ##  ## ##  ##  #  #  ##   # #    # #      
 #    # #        #      #      #    # # ## # # ## # #    # # #  # #    #  ####  
 ###### #        #      #      #    # #    # #    # ###### #  # # #    #      # 
 #    # #        #      #    # #    # #    # #    # #    # #   ## #    # #    # 
 #    # ######   #       ####   ####  #    # #    # #    # #    # #####   ####  
                                                                                

#general - begin#
@client.command()
@commands.cooldown(1, cooldown, commands.BucketType.user)
async def ping(ctx):
    await ctx.channel.send("pong")

@client.command()
@commands.cooldown(1, cooldown, commands.BucketType.user)
async def help(ctx):
    embed = discord.Embed(color=discord.Color.blue())
    embed.set_author(name="i see you need help...")

    file = open('userhelp.txt', 'r')
    userhelp = file.readlines()

    embed.add_field(name="here's what you can do:", value=listToString(userhelp), inline=False)
    
    await ctx.channel.send(f"{ctx.author.mention} look at your dm's!")
    await ctx.author.send(embed=embed)

var_uptime = datetime.utcnow()
@client.command()
@commands.cooldown(1, cooldown, commands.BucketType.user)
async def uptime(ctx):
    now = datetime.utcnow()
    elapsed = now - var_uptime
    seconds = elapsed.seconds
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    await ctx.channel.send(f"{ctx.author.mention} i've been awake since {elapsed.days}d {hours}h {minutes}m {seconds}s")
#general - end#

#games/fun - begin#
@client.command()
@commands.cooldown(1, cooldown, commands.BucketType.user)
async def roll(ctx, max=100):
    if max < 0:
        max = max * -1
        num = random.randrange(0, max)
        num = num * -1
    else:
        num = random.randrange(0, max)
    if num == 69 or num == -69:
        await ctx.channel.send(f"{ctx.author.mention} you've rolled " + str(num) + " (nice)")
    else:
        await ctx.channel.send(f"{ctx.author.mention} you've rolled " + str(num))

@client.command()
@commands.cooldown(1, cooldown, commands.BucketType.user)
async def coin(ctx):
    coinside = ["heads", "tails"]
    coinflip = random.choice(coinside)
    await ctx.channel.send(f"{ctx.author.mention} it's " + coinflip + "!")

@client.command()
@commands.cooldown(1, cooldown, commands.BucketType.user)
async def rps(ctx, userchoice : str):

    if (userchoice == "rock") or (userchoice == "paper") or (userchoice == "scissors"):

        rps_choices = ["rock","paper","scissors"]
        botchoice = random.choice(rps_choices)
        await ctx.channel.send(f"i got "+botchoice)
        if botchoice == userchoice:
            await ctx.channel.send(f"{ctx.author.mention} looks like we got a tie...")

        elif (botchoice == "rock" and userchoice == "paper") or (botchoice == "paper" and userchoice == "scissors") or (botchoice == "scissors" and userchoice == "rock"):
            await ctx.channel.send(f"{ctx.author.mention} congrats you win!")

        elif (botchoice == "rock" and userchoice == "scissors") or (botchoice == "paper" and userchoice == "rock") or (botchoice == "scissors" and userchoice == "paper"):
            await ctx.channel.send(f"{ctx.author.mention} i win!")
    else:
        await ctx.channel.send(f"{ctx.author.mention} make sure you type 'rock', 'paper' or 'scissors'!")

@client.command()
@commands.cooldown(1, cooldown, commands.BucketType.user)
async def joke(ctx):
    async with aiohttp.ClientSession() as session:
        request = await session.get('https://some-random-api.ml/others/joke')       
        jokejson = await request.json()

    embed = discord.Embed(color=discord.Color.random()) 
    embed.add_field(name="wanna here a bad joke?",value=jokejson['joke'].lower(), inline=False)

    await ctx.channel.send(embed=embed)

#games/fun - end#

#animals - begin#
@client.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def dog(ctx):
    async with aiohttp.ClientSession() as session:
        request = await session.get('https://some-random-api.ml/img/dog')       
        imgjson = await request.json()

        request2 = await session.get('https://some-random-api.ml/facts/dog')
        factjson = await request2.json()

    embed = discord.Embed(title="doggo!", color=discord.Color.random()) 
    embed.set_image(url=imgjson['link'])
    embed.set_footer(text="funfact: "+factjson['fact'].lower())
    await ctx.channel.send(embed=embed) 

@client.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def cat(ctx):
    async with aiohttp.ClientSession() as session:
        request = await session.get('https://some-random-api.ml/img/cat')       
        imgjson = await request.json()

        request2 = await session.get('https://some-random-api.ml/facts/cat')
        factjson = await request2.json()

    embed = discord.Embed(title="cat!", color=discord.Color.random()) 
    embed.set_image(url=imgjson['link'])
    embed.set_footer(text="funfact: "+factjson['fact'].lower())
    await ctx.channel.send(embed=embed)

@client.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def bird(ctx):
    async with aiohttp.ClientSession() as session:
        request = await session.get('https://some-random-api.ml/img/bird')       
        imgjson = await request.json()

        request2 = await session.get('https://some-random-api.ml/facts/bird')
        factjson = await request2.json()

    embed = discord.Embed(title="birb!", color=discord.Color.random()) 
    embed.set_image(url=imgjson['link'])
    embed.set_footer(text="funfact: "+factjson['fact'].lower())
    await ctx.channel.send(embed=embed)

@client.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def fox(ctx):
    async with aiohttp.ClientSession() as session:
        request = await session.get('https://some-random-api.ml/img/fox')       
        imgjson = await request.json()

        request2 = await session.get('https://some-random-api.ml/facts/fox')
        factjson = await request2.json()

    embed = discord.Embed(title="fox!", color=discord.Color.random()) 
    embed.set_image(url=imgjson['link'])
    embed.set_footer(text="funfact: "+factjson['fact'].lower())
    await ctx.channel.send(embed=embed)

@client.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def koala(ctx):
    async with aiohttp.ClientSession() as session:
        request = await session.get('https://some-random-api.ml/img/koala')       
        imgjson = await request.json()

        request2 = await session.get('https://some-random-api.ml/facts/koala')
        factjson = await request2.json()

    embed = discord.Embed(title="koala!", color=discord.Color.random()) 
    embed.set_image(url=imgjson['link'])
    embed.set_footer(text="funfact: "+factjson['fact'].lower())
    await ctx.channel.send(embed=embed)

@client.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def panda(ctx):
    async with aiohttp.ClientSession() as session:
        request = await session.get('https://some-random-api.ml/img/panda')       
        imgjson = await request.json()

        request2 = await session.get('https://some-random-api.ml/facts/panda')
        factjson = await request2.json()

    embed = discord.Embed(title="panda!", color=discord.Color.random()) 
    embed.set_image(url=imgjson['link'])
    embed.set_footer(text="funfact: "+factjson['fact'].lower())
    await ctx.channel.send(embed=embed)

@client.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def redpanda(ctx):
    async with aiohttp.ClientSession() as session:
        request = await session.get('https://some-random-api.ml/img/red_panda')       
        imgjson = await request.json()

        request2 = await session.get('https://some-random-api.ml/facts/panda')
        factjson = await request2.json()

    embed = discord.Embed(title="panda!", color=discord.Color.random()) 
    embed.set_image(url=imgjson['link'])
    embed.set_footer(text="funfact: "+factjson['fact'].lower())
    await ctx.channel.send(embed=embed)

#animals - end#

#tools - begin#
@client.command()
@commands.cooldown(1, cooldown, commands.BucketType.user)
async def binary(ctx, number: int):
    binarynum = format(number, 'b')
    await ctx.channel.send(f"{ctx.author.mention} i converted your number to binary! it's '" + binarynum + "'")

@client.command()
@commands.cooldown(1, cooldown, commands.BucketType.user)
async def hex(ctx, number: int):
    hexnum = '{0:x}'.format(number)
    hexnum_formated = hexnum.title()
    await ctx.channel.send(f"{ctx.author.mention} i converted your number to hexadecimal! it's '" + hexnum_formated + "'")

@client.command()
@commands.cooldown(1, cooldown, commands.BucketType.user)
async def helloworld(ctx, lang:str):
    if lang == "c":
        file = open('helloworld/c.txt', 'r')
        code = file.readlines()
        await ctx.channel.send(f"{ctx.author.mention} here's your code:\n" + listToString(code))
    elif lang == "c++":
        file = open('helloworld/c++.txt', 'r')
        code = file.readlines()
        await ctx.channel.send(f"{ctx.author.mention} here's your code:\n" + listToString(code))
    elif lang == "c#":
        file = open('helloworld/c#.txt', 'r')
        code = file.readlines()
        await ctx.channel.send(f"{ctx.author.mention} here's your code:\n" + listToString(code))
    elif lang == "java":
        file = open('helloworld/java.txt', 'r')
        code = file.readlines()
        await ctx.channel.send(f"{ctx.author.mention} here's your code:\n" + listToString(code))
    elif lang == "js":
        file = open('helloworld/js.txt', 'r')
        code = file.readlines()
        await ctx.channel.send(f"{ctx.author.mention} here's your code:\n" + listToString(code))
    elif lang == "py":
        file = open('helloworld/py.txt', 'r')
        code = file.readlines()
        await ctx.channel.send(f"{ctx.author.mention} here's your code:\n" + listToString(code))
    elif lang == "bfq":
        file = open('helloworld/bfq.txt', 'r')
        code = file.readlines()
        await ctx.channel.send(f"{ctx.author.mention} here's your code:\n" + listToString(code))
    elif lang == "rust":
        file = open('helloworld/rust.txt', 'r')
        code = file.readlines()
        await ctx.channel.send(f"{ctx.author.mention} here's your code:\n" + listToString(code))
    elif lang == "go":
        file = open('helloworld/go.txt', 'r')
        code = file.readlines()
        await ctx.channel.send(f"{ctx.author.mention} here's your code:\n" + listToString(code))
    elif lang == "asm":
        file = open('helloworld/asm.txt', 'r')
        code = file.readlines()
        await ctx.channel.send(f"{ctx.author.mention} here's your code:\n" + listToString(code))
    
    elif lang == "list":
        file = open('helloworld/list.txt', 'r')
        code = file.readlines()
        await ctx.channel.send(f"{ctx.author.mention} here's what i currently support:\n" + listToString(code))

    else:
        await ctx.channel.send(f"{ctx.author.mention} whoops! looks like i don't have that language yet... type '>helloworld list' to see what i got")

#tools - end#

                                                                                               
  ####  #        ##    ####  #    #     ####   ####  #    # #    #   ##   #    # #####   ####  
 #      #       #  #  #      #    #    #    # #    # ##  ## ##  ##  #  #  ##   # #    # #      
  ####  #      #    #  ####  ######    #      #    # # ## # # ## # #    # # #  # #    #  ####  
      # #      ######      # #    #    #      #    # #    # #    # ###### #  # # #    #      # 
 #    # #      #    # #    # #    #    #    # #    # #    # #    # #    # #   ## #    # #    # 
  ####  ###### #    #  ####  #    #     ####   ####  #    # #    # #    # #    # #####   ####  
                                                                                               


#------------SLASH COMMANDS--------------#

#general - begin#
@client.slash_command(name="ping", description="see if i'm up")
@commands.cooldown(1, cooldown, commands.BucketType.user)
async def slash_ping(ctx):
    await ctx.respond("pong")

@client.slash_command(name="help", description="look what i can do")
@commands.cooldown(1, cooldown, commands.BucketType.user)
async def slash_help(ctx):
    embed = discord.Embed(color=discord.Color.blue())
    embed.set_author(name="i see you need help...")

    file = open('userhelp.txt', 'r')
    userhelp = file.readlines()

    embed.add_field(name="here's what you can do:", value=listToString(userhelp), inline=False)
    
    await ctx.respond(f"look at your dm's!")
    await ctx.author.send(embed=embed)

@client.slash_command(name="uptime", description="see how long i've been awake")
@commands.cooldown(1, cooldown, commands.BucketType.user)
async def slash_uptime(ctx):
    now = datetime.utcnow()
    elapsed = now - var_uptime
    seconds = elapsed.seconds
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    await ctx.respond(f"i've been awake since {elapsed.days}d {hours}h {minutes}m {seconds}s")
#general - end#

#games/fun - begin#
@client.slash_command(name="roll", description="i roll the dice. if no limit is set the default limit will be 100")
@commands.cooldown(1, cooldown, commands.BucketType.user)
async def slash_roll(ctx, max=100):
    max_int = 0
    roll_error = False
    try:
        max_int = int(max)
    except:
        await ctx.respond(f"i can't roll text... give me a number!")
        roll_error = True

    if roll_error == False:
        if max_int < 0:
            max_int = max_int * -1
            num = random.randrange(0, max_int)
            num = num * -1
        else:
            num = random.randrange(0, max_int)
        if num == 69 or num == -69:
            await ctx.respond(f"you've rolled " + str(num) + " (nice)")
        else:
            await ctx.respond(f"you've rolled " + str(num))
    else:
        return

    

@client.slash_command(name="coin", description="i flip a coin. it's either heads or tails!")
@commands.cooldown(1, cooldown, commands.BucketType.user)
async def slash_coin(ctx):
    coinside = ["heads", "tails"]
    coinflip = random.choice(coinside)
    await ctx.respond(f"it's " + coinflip + "!")

@client.slash_command(name="rps", description="play rock, paper, scissors with me! pick yours and see who wins...")
@commands.cooldown(1, cooldown, commands.BucketType.user)
async def slash_rps(ctx, userchoice : str):

    if (userchoice == "rock") or (userchoice == "paper") or (userchoice == "scissors"):

        rps_choices = ["rock","paper","scissors"]
        botchoice = random.choice(rps_choices)
        if botchoice == userchoice:
            await ctx.respond(f""+botchoice+"!\n"+"looks like we got a tie...")

        elif (botchoice == "rock" and userchoice == "paper") or (botchoice == "paper" and userchoice == "scissors") or (botchoice == "scissors" and userchoice == "rock"):
            await ctx.respond(f""+botchoice+"!\n"+"congrats you win!")

        elif (botchoice == "rock" and userchoice == "scissors") or (botchoice == "paper" and userchoice == "rock") or (botchoice == "scissors" and userchoice == "paper"):
            await ctx.respond(f""+botchoice+"!\n"+"i win!")
    else:
        await ctx.respond(f"make sure you type 'rock', 'paper' or 'scissors'!")
        

@client.slash_command(name="joke", description="i tell you a bad joke")
@commands.cooldown(1, cooldown, commands.BucketType.user)
async def slash_joke(ctx):
    async with aiohttp.ClientSession() as session:
        request = await session.get('https://some-random-api.ml/others/joke')       
        jokejson = await request.json()

    embed = discord.Embed(color=discord.Color.random()) 
    embed.add_field(name="wanna here a bad joke?",value=jokejson['joke'].lower(), inline=False)

    await ctx.respond(embed=embed)

#games/fun - end#

#animals - begin#
@client.slash_command(name="dog", description="get a random dog image and fact!")
@commands.cooldown(1, 5, commands.BucketType.user)
async def slash_dog(ctx):
    async with aiohttp.ClientSession() as session:
        request = await session.get('https://some-random-api.ml/img/dog')       
        imgjson = await request.json()

        request2 = await session.get('https://some-random-api.ml/facts/dog')
        factjson = await request2.json()

    embed = discord.Embed(title="doggo!", color=discord.Color.random()) 
    embed.set_image(url=imgjson['link'])
    embed.set_footer(text="funfact: "+factjson['fact'].lower())
    await ctx.respond(embed=embed) 

@client.slash_command(name="cat", description="get a random cat image and fact!")
@commands.cooldown(1, 5, commands.BucketType.user)
async def slash_cat(ctx):
    async with aiohttp.ClientSession() as session:
        request = await session.get('https://some-random-api.ml/img/cat')       
        imgjson = await request.json()

        request2 = await session.get('https://some-random-api.ml/facts/cat')
        factjson = await request2.json()

    embed = discord.Embed(title="cat!", color=discord.Color.random()) 
    embed.set_image(url=imgjson['link'])
    embed.set_footer(text="funfact: "+factjson['fact'].lower())
    await ctx.respond(embed=embed)

@client.slash_command(name="bird", description="get a random bird image and fact!")
@commands.cooldown(1, 5, commands.BucketType.user)
async def slash_bird(ctx):
    async with aiohttp.ClientSession() as session:
        request = await session.get('https://some-random-api.ml/img/bird')       
        imgjson = await request.json()

        request2 = await session.get('https://some-random-api.ml/facts/bird')
        factjson = await request2.json()

    embed = discord.Embed(title="birb!", color=discord.Color.random()) 
    embed.set_image(url=imgjson['link'])
    embed.set_footer(text="funfact: "+factjson['fact'].lower())
    await ctx.respond(embed=embed)

@client.slash_command(name="fox", description="get a random fox image and fact!")
@commands.cooldown(1, 5, commands.BucketType.user)
async def slash_fox(ctx):
    async with aiohttp.ClientSession() as session:
        request = await session.get('https://some-random-api.ml/img/fox')       
        imgjson = await request.json()

        request2 = await session.get('https://some-random-api.ml/facts/fox')
        factjson = await request2.json()

    embed = discord.Embed(title="fox!", color=discord.Color.random()) 
    embed.set_image(url=imgjson['link'])
    embed.set_footer(text="funfact: "+factjson['fact'].lower())
    await ctx.respond(embed=embed)

@client.slash_command(name="koala", description="get a random koala image and fact!")
@commands.cooldown(1, 5, commands.BucketType.user)
async def slash_koala(ctx):
    async with aiohttp.ClientSession() as session:
        request = await session.get('https://some-random-api.ml/img/koala')       
        imgjson = await request.json()

        request2 = await session.get('https://some-random-api.ml/facts/koala')
        factjson = await request2.json()

    embed = discord.Embed(title="koala!", color=discord.Color.random()) 
    embed.set_image(url=imgjson['link'])
    embed.set_footer(text="funfact: "+factjson['fact'].lower())
    await ctx.respond(embed=embed)

@client.slash_command(name="panda", description="get a random panda image and fact!")
@commands.cooldown(1, 5, commands.BucketType.user)
async def slash_panda(ctx):
    async with aiohttp.ClientSession() as session:
        request = await session.get('https://some-random-api.ml/img/panda')       
        imgjson = await request.json()

        request2 = await session.get('https://some-random-api.ml/facts/panda')
        factjson = await request2.json()

    embed = discord.Embed(title="panda!", color=discord.Color.random()) 
    embed.set_image(url=imgjson['link'])
    embed.set_footer(text="funfact: "+factjson['fact'].lower())
    await ctx.respond(embed=embed)

@client.slash_command(name="redpanda", description="get a random red panda image and fact!")
@commands.cooldown(1, 5, commands.BucketType.user)
async def slash_redpanda(ctx):
    async with aiohttp.ClientSession() as session:
        request = await session.get('https://some-random-api.ml/img/red_panda')       
        imgjson = await request.json()

        request2 = await session.get('https://some-random-api.ml/facts/panda')
        factjson = await request2.json()

    embed = discord.Embed(title="red panda!", color=discord.Color.random()) 
    embed.set_image(url=imgjson['link'])
    embed.set_footer(text="funfact: "+factjson['fact'].lower())
    await ctx.respond(embed=embed)

#animals - end#

#tools - begin#
@client.slash_command(name="binary", description="i'm gonna convert your number to binary")
@commands.cooldown(1, cooldown, commands.BucketType.user)
async def slash_binary(ctx, number: int):
    binarynum = format(number, 'b')
    await ctx.respond(f"i converted your number to binary! it's '" + binarynum + "'")

@client.slash_command(name="hex", description="i'm gonna convert your number to hexadecimal")
@commands.cooldown(1, cooldown, commands.BucketType.user)
async def slash_hex(ctx, number: int):
    hexnum = '{0:x}'.format(number)
    hexnum_formated = hexnum.title()
    await ctx.respond(f"i converted your number to hexadecimal! it's '" + hexnum_formated + "'")

@client.slash_command(name="helloworld", description="see how the classic helloworld program looks in different languages")
@commands.cooldown(1, cooldown, commands.BucketType.user)
async def slash_helloworld(ctx, lang:str):
    if lang == "c":
        file = open('helloworld/c.txt', 'r')
        code = file.readlines()
        await ctx.respond(f"here's your code:\n" + listToString(code))
    elif lang == "c++":
        file = open('helloworld/c++.txt', 'r')
        code = file.readlines()
        await ctx.respond(f"here's your code:\n" + listToString(code))
    elif lang == "c#":
        file = open('helloworld/c#.txt', 'r')
        code = file.readlines()
        await ctx.respond(f"here's your code:\n" + listToString(code))
    elif lang == "java":
        file = open('helloworld/java.txt', 'r')
        code = file.readlines()
        await ctx.respond(f"here's your code:\n" + listToString(code))
    elif lang == "js":
        file = open('helloworld/js.txt', 'r')
        code = file.readlines()
        await ctx.respond(f"here's your code:\n" + listToString(code))
    elif lang == "py":
        file = open('helloworld/py.txt', 'r')
        code = file.readlines()
        await ctx.respond(f"here's your code:\n" + listToString(code))
    elif lang == "bfq":
        file = open('helloworld/bfq.txt', 'r')
        code = file.readlines()
        await ctx.respond(f"here's your code:\n" + listToString(code))
    elif lang == "rust":
        file = open('helloworld/rust.txt', 'r')
        code = file.readlines()
        await ctx.respond(f"here's your code:\n" + listToString(code))
    elif lang == "go":
        file = open('helloworld/go.txt', 'r')
        code = file.readlines()
        await ctx.respond(f"here's your code:\n" + listToString(code))
    elif lang == "asm":
        file = open('helloworld/asm.txt', 'r')
        code = file.readlines()
        await ctx.respond(f"here's your code:\n" + listToString(code))
    
    elif lang == "list":
        file = open('helloworld/list.txt', 'r')
        code = file.readlines()
        await ctx.respond(f"here's what i currently support:\n" + listToString(code))

    else:
        await ctx.respond(f"whoops! looks like i don't have that language yet... type '/helloworld list' to see what i got")

#tools - end#


#------------BOT END--------------#
client.run(TOKEN)
