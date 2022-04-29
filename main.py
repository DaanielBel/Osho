from typing import ItemsView
import itertools
import discord
import random
import time
import os
import praw
import json
from discord_slash import SlashCommand
from discord.ext import commands,tasks
from dotenv import load_dotenv
from datetime import date

client = commands.Bot(
    command_prefix = "...",
    intents = discord.Intents().all()
    )
slash = SlashCommand(client, sync_commands = True)

reddit = praw.Reddit(
    client_id='Zyn3SfBbg-pLg5MIykcPOA',
    client_secret='IYCN5815OaSdm4edsa44n3l3v2seFg',
    user_agent='Osho'
    )

emojiDict = {
    1: "<:Dice1:944309381900693524>",
    2: "<:Dice2:944309652068392981>",
    3: "<:Dice3:944310694453583882>",
    4: "<:Dice4:944310694604591154>",
    5: "<:Dice5:944310694654914580>",
    6: "<:Dice6:944310694776545320>"
}

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    activity_string = '{} servers.'.format(len(client.guilds))
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=activity_string))

@slash.slash(name = "ban", description = "Bans a member")
@commands.has_permissions(ban_members = True)
async def ban(ctx, member : discord.Member, reason=None):
        await member.ban(reason=reason)
        await ctx.send("banned: <@" + str(member.id) + ">")
        await member.send("you have been banned from: - "+ctx.guild.name +" reason:"+reason)
        embed = discord.Embed(title="Ban", description=member.display_name+" was banned",color=0xfe9fcf)
        embed.add_field(name="Reason:", value=reason, inline=False)
        await ctx.send(embed=embed)          

@ban.error
async def ban_error(ctx, error):
    print(error)
    await ctx.send("Missing Permissions!")    

@slash.slash(name = "kick", description = "Kicks a member")
@commands.has_permissions(kick_members = True)
async def kick(ctx, member : discord.Member, reason=None):
        await member.kick(reason=reason)
        await ctx.send("kicked: <@" + str(member.id) + ">")

@kick.error
async def kick_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing Required argument:\nTry writing the command like told")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("Missing Premissions!")

@slash.slash(name = "cleanup", description = "Cleans up the chat")
@commands.has_permissions(manage_channels = True)
async def cleanup(ctx, size):
    await ctx.channel.purge(limit=int(size))
    embed=discord.Embed(title="Clean up!", description="Deleted "+size+" messages", color=0xfe9fcf)
    embed.set_author(name="Osho", icon_url="https://cdn.discordapp.com/avatars/826172867573579786/49fb1a7583bc93e37a20b83798176d14.png?size=128")
    msg = await ctx.send(embed=embed)
    time(1)
    await msg.delete()

@cleanup.error
async def cleanup_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Missing Premissions!")    

@slash.slash(name="memes", description="Sends a meme from r/memes")
async def memeMeUp(ctx):
    memes_submissions = reddit.subreddit('memes').hot()
    post_to_pick = random.randint(1, 10)
    for i in range(0, post_to_pick):
        submission = next(x for x in memes_submissions if not x.stickied)

    embed=discord.Embed(title=submission.title, color=0xff89f9)
    embed.set_image(url=submission.url)
    embed.set_footer(text="A post from the subreddit r/memes")
    await ctx.send(embed=embed)

@slash.slash(name = "ping", description = "Sends Osho's ping")
async def ping(ctx):
    await ctx.send(f"My ping is - {round(client.latency * 1000)}ms")

@slash.slash(name = "rollTheDice", description = "Rolls The Dice")
async def rollTheDice(ctx):
    msg = await ctx.send("<a:RollTheDiceOsho:944319581294575667>")
    num = random.randint(1,6)
    time.sleep(1)
    await msg.edit(content = emojiDict[num])

@slash.slash(name='lovecaculator', description="caculates the amout of love between two people")    
async def lovecaculator(ctx, name1, name2):
    embed=discord.Embed(title="Love caculator", description="Caculating..", color=0xfe9fcf)
    embed.set_author(name="Osho", icon_url="https://cdn.discordapp.com/avatars/826172867573579786/49fb1a7583bc93e37a20b83798176d14.png?size=128%22")
    msg = await ctx.send(embed=embed)
    love = random.randint(0,100)

    if int(love) == 100:
        description = "A perfect match!"

    elif int(love) >= 85:
        description = "My oh my... Is that a,, match!?"

    elif int(love) >= 70:
        description = "Not quite the soulmates, not to far away to try!"

    elif int(love) >= 50:
        description = "Maybe its not it"     

    elif int(love) < 50:
        description = "DON'T!"    

    embed=discord.Embed(title="Love caculator", description="Finished!", color=0xfe9fcf)
    embed.set_author(name="Osho", icon_url="https://cdn.discordapp.com/avatars/826172867573579786/49fb1a7583bc93e37a20b83798176d14.png?size=128%22")
    embed.add_field(name=name1, value="    " + str(love)+"% ❤️", inline=False)
    embed.add_field(name=name2, value="    "+description, inline=False)
    embed.set_footer(text="Osho(2022)")
    time.sleep(1)
    await msg.edit(embed=embed)




@slash.slash(name = "help", description= "Gives information on commands")
async def help(ctx):
    embedVar = discord.Embed(title="Help", description="Prefix = **!!!**(Don't use)", color=0xFFB9F9)
    #embedVar.add_field(name=server_prefix1+"fetch", value="asks Osho to bring the ball", inline=False)
    #embedVar.add_field(name=server_prefix1+"pet", value="asks Osho to pet him", inline=False)
    embedVar.add_field(name="/help", value="asks Osho for the commands", inline=False)
    embedVar.add_field(name="/memes", value="ask Osho for some *funny* memes!", inline=False)
    embedVar.add_field(name="/lovecac <name1> <name2>", value="Caculates the love between two individual", inline=False)
    embedVar.add_field(name="/rollTheDice", value="Rolls a dice", inline=False)
    embedVar.add_field(name="/ping", value="Pong!", inline=False)
    #embedVar.add_field(name=server_prefix1+"tictactoe <@player2>", value="for more info- "+server_prefix1+"help_tictactoe", inline=False)
    embedVar.add_field(name="/credits", value="asks Osho who is the creator of the bot(me)", inline=False)   
    msg = await ctx.send(embed = embedVar)
    await msg.add_reaction("⬅️")
    await msg.add_reaction("➡️")

@slash.slash(name = "adminHelp", description= "Gives information on admin commands")
async def adminHelp(ctx):
    embedVar = discord.Embed(title="Admin - help", description="Prefix = **!!!**(Don't use)", color=0xFFB9F9)
    embedVar.add_field(name="/cleanup <x>", value="asks Osho to clean up the chat!", inline=False)
    embedVar.add_field(name="/kick <user> <reason*>", value="Kick a member!", inline=False)
    embedVar.add_field(name="/ban <user> <reason*>", value="Ban a member!", inline=False)    
    await ctx.send(embed = embedVar)
##############

@slash.slash(name="balance", description = "Returns the user's balance")
async def balance(ctx):
    with open('balance.json') as f:
        data = json.load(f)
    
    if str(ctx.author.id) in data:
        await ctx.send(f"Your balance is: {data[str(ctx.author.id)]}<:OshoCoin:944730109108158554> Osho Coins!")
    else:
        with open('balance.json', 'r') as f:
            data = json.load(f)
            data[str(ctx.author.id)] = 500

            await ctx.send(f"Your balance is: {data[str(ctx.author.id)]}<:OshoCoin:944730109108158554> Osho Coins!")

        with open('balance.json', 'w') as f:
            json.dump(data, f, indent=4)

@slash.slash(name="flipACoin", description = "Flip a coin for money for all in write 'all' (1 = heads, 2 = tails)")
async def flipACoin(ctx, money, side):
    with open('balance.json') as f:
        data = json.load(f)

    if money == "all":
        money = int(data[str(ctx.author.id)])
    if int(money) > int(data[str(ctx.author.id)]):
        await ctx.send("Not enough money in balance!")

    rand = random.randint(1,2)
    if rand == 1:
        if int(side) == 1:
            data[str(ctx.author.id)] = int(data[str(ctx.author.id)]) + int(money)
        else:
            data[str(ctx.author.id)] = int(data[str(ctx.author.id)]) - int(money)

        await ctx.send(f"Heads!\n Your new balance is: {data[str(ctx.author.id)]}<:OshoCoin:944730109108158554>")
    else:
        if int(side) == 2:
            data[str(ctx.author.id)] = int(data[str(ctx.author.id)]) + int(money)
        else:
            data[str(ctx.author.id)] = int(data[str(ctx.author.id)]) - int(money)

        await ctx.send(f"Tails!\n Your new balance is: {data[str(ctx.author.id)]}<:OshoCoin:944730109108158554>")

    with open('balance.json', 'w') as f:
        json.dump(data, f, indent=4)

@slash.slash(name="blackJack", description= "Play black jack for money against osho!")
async def blackJack(ctx):
    deck = list(itertools.product(range(1,14),['♠','♥','♦','♣']))
    random.shuffle(deck)
    card1 = deck[0]
    card2 = deck[1]
    card3 = deck[2]
    card4 = deck[3]

    embedVar = discord.Embed(title="BlackJack", description="Hit  |  Stand", color=0xFFB9F9)
    embedVar.add_field(name= f"{str(card1)} {str(card2)}", value="Your cards", inline=False)
    embedVar.add_field(name= f"{str(card3)} ?", value="Dealer cards", inline=False)
    await ctx.send(embed = embedVar)  


@slash.slash(name="daily", description = "Get free Osho-Coins every 24h!")
async def daily(ctx):
    with open('daily.json') as f:
        dataDaily = json.load(f)

    today = date.today()

    if str(ctx.author.id) in dataDaily: #if user used Daily before
        if dataDaily[str(ctx.author.id)] == today.strftime("%d/%m/%Y"):
            await ctx.send("Already used daily today! try again tommorow")
        else:
            await ctx.send("Added 500<:OshoCoin:944730109108158554> to your balance!")
            with open('balance.json', 'r') as f:
                data = json.load(f)
                data[str(ctx.author.id)] = data[str(ctx.author.id)] + 500

            dataDaily[str(ctx.author.id)] = today.strftime("%d/%m/%Y") 
            with open('daily.json', 'w') as f:
                json.dump(dataDaily, f, indent=4) 
            with open('balance.json', 'w') as f:
                json.dump(data, f, indent=4)  
 
    else:
        await ctx.send("Added 500<:OshoCoin:944730109108158554> to your balance!")
        with open('balance.json', 'r') as f:
            data = json.load(f)
            data[str(ctx.author.id)] = data[str(ctx.author.id)] + 500

        dataDaily[str(ctx.author.id)] = today.strftime("%d/%m/%Y") 
        with open('daily.json', 'w') as f:
            json.dump(dataDaily, f, indent=4)    
        with open('balance.json', 'w') as f:
            json.dump(data, f, indent=4)

@slash.slash(name="shop", description = "shop")
async def shop(ctx):
    embedVar = discord.Embed(title="Shop", description="To buy- /buy <item_id>", color=0xFFB9F9)
    embedVar.add_field(name="Normal Create", value="Id = 1, Price = 50,000<:OshoCoin:944730109108158554>", inline=False)
    embedVar.add_field(name="Epic Create", value="Id = 2, Price = 100,000<:OshoCoin:944730109108158554>", inline=False)
    embedVar.add_field(name="Legendary create", value="Id = 3, Price = 500,000<:OshoCoin:944730109108158554>", inline=False)
    embedVar.add_field(name="Mythic create", value="Id = 4, Price = 1,000,000<:OshoCoin:944730109108158554>", inline=False)
    await ctx.send(embed = embedVar)   

@slash.slash(name="buy", description = "buy")
async def buy(ctx, item_id):  
    with open('balance.json') as f:
        balance = json.load(f)
    with open('creates.json') as f:
        creates = json.load(f)
    with open('items.json') as f:
        items = json.load(f)


    if int(creates[str(item_id)]["price"]) < balance[str(ctx.author.id)]:
        balance[str(ctx.author.id)] = balance[str(ctx.author.id)] - int(creates[str(item_id)]["price"])
        await ctx.send(f'Bought {creates[str(item_id)]["name"]} for {int(creates[str(item_id)]["price"])} ')
        rand = random.int(1, 100)
        #if rand == 1:
            
        #elif rand < 4:
        
        #elif rand < 10:

        #elif rand < 45

        #elif rand < 100
    else:
        await ctx.send("You can't afford that")
        await ctx.send("RATIO")

    with open('balance.json', 'w') as f:
        json.dump(balance, f, indent=4)

#@slash.slash(name = "inventory")
#async def inv(ctx):


##############

@client.event
async def on_reaction_add(reaction, user):
    if user != client.user:
        if str(reaction.emoji) == "⬅️":         
            embedVar = discord.Embed(title="Help", description="Prefix = **!!!**(Don't use)", color=0xFFB9F9)
            #embedVar.add_field(name=server_prefix1+"fetch", value="asks Osho to bring the ball", inline=False)
            #embedVar.add_field(name=server_prefix1+"pet", value="asks Osho to pet him", inline=False)
            embedVar.add_field(name="/help", value="asks Osho for the commands", inline=False)
            embedVar.add_field(name="/memes", value="ask Osho for some *funny* memes!", inline=False)
            embedVar.add_field(name="/lovecac <name1> <name2>", value="Caculates the love between two individual", inline=False)
            embedVar.add_field(name="/rollTheDice", value="Rolls a dice", inline=False)
            embedVar.add_field(name="/ping", value="Pong!", inline=False)
            embedVar.add_field(name="/credits", value="asks Osho who is the creator of the bot(me)", inline=False)      
            await reaction.message.edit(embed = embedVar)
            await reaction.remove(user)
        if str(reaction.emoji) == "➡️":
            embedVar = discord.Embed(title="help - 2", description="Prefix = **!!!**(Don't use)", color=0xFFB9F9)
            embedVar.add_field(name="/balance ", value="Check how much osho coins you have", inline=False)
            embedVar.add_field(name="/daily", value="Get daily prizes", inline=False)
            embedVar.add_field(name="/flipACoin <money> <side>", value="Flip a coin for money (1 = heads, 2 = tails)", inline=False)   
            await reaction.message.edit(embed = embedVar)  
            await reaction.remove(user)

#client.run(os.getenv['TOKEN'])
client.run("ODI2OTIyMjgxMTIwOTU2NDU3.YGThYw.mNYbKjWpEXo1ruVieuQlxvTBzhU")
