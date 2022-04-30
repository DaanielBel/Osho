from typing_extensions import Required
from venv import create
import discord
import json
import random
import time
import os
from numpy import require
import praw
from datetime import date
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option
from discord.ext import commands,tasks
from dotenv import load_dotenv
from webserver import keep_alive

client = commands.Bot(
    command_prefix = "!!!",
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

@slash.slash(name="memes", description="Sends a meme from r/memes", guild_ids=[826173511693238332])
async def memeMeUp(ctx):
    memes_submissions = reddit.subreddit('memes').hot()
    post_to_pick = random.randint(1, 10)
    for i in range(0, post_to_pick):
        submission = next(x for x in memes_submissions if not x.stickied)

    embed=discord.Embed(title=submission.title, color=0xff89f9)
    embed.set_image(url=submission.url)
    embed.set_footer(text="A post from the subreddit r/memes")
    await ctx.send(embed=embed)

@slash.slash(name = "ping", description = "Sends Osho's ping", guild_ids=[826173511693238332])
async def ping(ctx):
    await ctx.send(f"My ping is - {round(client.latency * 1000)}ms")

@slash.slash(name='lovecaculator', description="caculates the amout of love between two people", guild_ids=[826173511693238332])    
async def lovecaculator(ctx, name1, name2):
    embed=discord.Embed(title="Love caculator", description="Caculating..", color=0xfe9fcf)
    embed.set_author(name="Osho", icon_url="https://cdn.discordapp.com/avatars/826172867573579786/49fb1a7583bc93e37a20b83798176d14.png?size=128%22")
    msg = await ctx.send(embed=embed)
    love = random.randint(0,100)

    if int(love) == 100:
        description = "A perfect match!"

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
    await msg.edit(embed=embed)




@slash.slash(name = "help", description= "Gives information on commands", guild_ids=[826173511693238332])
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
          
@slash.slash(name = "rollTheDice", description = "Rolls The Dice", guild_ids=[826173511693238332])
async def rollTheDice(ctx):
    msg = await ctx.send("<a:RollTheDiceOsho:944319581294575667>", guild_ids=[826173511693238332])
    num = random.randint(1,6)
    time.sleep(1)
    await msg.edit(content = emojiDict[num])

@slash.slash(name="balance", description = "Returns the user's balance", guild_ids=[826173511693238332])
async def balance(ctx):
    with open('balance.json') as f:
        data = json.load(f)
    
    flag = False
    if str(ctx.author.id) in data:
        await ctx.send(f"Your balance is: {data[str(ctx.author.id)]}")
    else:
        with open('balance.json', 'r') as f:
            data = json.load(f)
            data[str(ctx.author.id)] = 500

            await ctx.send(f"Your balance is: {data[str(ctx.author.id)]}<:OshoCoin:944730109108158554> Osho Coins!")

        with open('balance.json', 'w') as f:
            json.dump(data, f, indent=4)

@slash.slash(
    name="flipACoin", description = "Flip a coin for money", guild_ids=[826173511693238332],
    options=[
        create_option(
            name = "money",
            description = "How much money you want to bet on (Insert 'all' for all-in)",
            required = True,
            option_type = 3
        ),
        create_option(
            name = "side",
            description = "Which side you want to bet on",
            required = True,
            option_type = 4,
            choices = [
                create_choice(
                        name = "Heads",
                        value = 1
                ),
                create_choice(
                    name = "Tails",
                    value = 2
                )
            ]
        )
    ]
)
async def flipACoin(ctx:SlashContext, money, side:int):
    with open('balance.json') as f:
        data = json.load(f)

    if money == "all":
        money = int(data[str(ctx.author.id)]);

    if int(money) > int(data[str(ctx.author.id)]):
        await ctx.send("Not enough money in balance!")

    rand = random.randint(1,2)
    print(rand)
    if rand == 1:
        if int(side) == 1:
            data[str(ctx.author.id)] = int(data[str(ctx.author.id)]) + int(money)
        else:
            data[str(ctx.author.id)] = int(data[str(ctx.author.id)]) - int(money)

        await ctx.send(f"Heads!\n Your new balance is: {data[str(ctx.author.id)]}<:OshoCoin:944730109108158554>")
    else:
        if int(side) == 2:
            print("yes money")
            data[str(ctx.author.id)] = int(data[str(ctx.author.id)]) + int(money)
        else:
            print("no money")
            data[str(ctx.author.id)] = int(data[str(ctx.author.id)]) - int(money)

        await ctx.send(f"Tails!\n Your new balance is: {data[str(ctx.author.id)]}<:OshoCoin:944730109108158554>")

    with open('balance.json', 'w') as f:
        json.dump(data, f, indent=4)

@slash.slash(name="daily", description = "Get free Osho-Coins every 24h!", guild_ids=[826173511693238332])
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

@slash.slash(name="shop", description = "shop", guild_ids=[826173511693238332])
async def shop(ctx):
    embedVar = discord.Embed(title="Shop", description="To buy- /buy <item_id>", color=0xFFB9F9)
    embedVar.add_field(name="Normal Create", value="Id = 1, Price = 10,000<:OshoCoin:944730109108158554>", inline=False)
    embedVar.add_field(name="Epic Create", value="Id = 1, Price = 10,000<:OshoCoin:944730109108158554>", inline=False)
    embedVar.add_field(name="Legendary create", value="Id = 1, Price = 10,000<:OshoCoin:944730109108158554>", inline=False)
    await ctx.send(embed = embedVar)   
    
#keep_alive()
client.run(os.environ['TOKEN'])