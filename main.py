import discord
import random
import time
import os
import praw
from discord_slash import SlashCommand
from discord.ext import commands,tasks
from dotenv import load_dotenv
from webserver import keep_alive

MY_GUILD_ID = discord.Object(826173511693238332)

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

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    activity_string = '{} servers.'.format(len(client.guilds))
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=activity_string))

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

@slash.slash(name='lovecaculator', description="caculates the amout of love between two people")    
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




@slash.slash(name = "help", description= "Gives information on commands", guild_ids= [826173511693238332])
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
          
#keep_alive()
client.run(os.environ['TOKEN'])