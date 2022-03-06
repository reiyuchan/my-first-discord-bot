import discord
import json

from operator import index
from discord import activity
from discord import member
from discord.ext import commands

with open("config/config.json") as f:
        configData = json.load(f)

token = configData["TKN"]

client = discord.Client()
client = commands.Bot(command_prefix = '$')

@client.event
async def on_ready():
    print('{0.user}'.format(client), 'is up and running')
    #todo: custom status for bot you can change watching to playing.. Ex: discord.ActivityType.playing, name = "a Game"
    botActivity = discord.Activity(type = discord.ActivityType.watching, name = "Anime") #change it to expression you would like.. Ex: instead of "Anime" put "Movies" ..etc
    await client.change_presence(activity = botActivity, status=discord.Status.online)

@client.event
async def on_message(message):

    if message.author == client.user:
        return

    if message.content.startswith('%invite'):
        await message.channel.send("Here is my invite link: \n 'paste your invite link here' \nThanks for inviting me!")

    if message.content.startswith('%hello'):
        await message.channel.send("Hello! please report any bugs to my creator i'm still fairly new and under development so go easy on me..!! 'paste your discord server here'")
    
    #for filtering some bad words
    word_list = [''] #example word_list = ['stupid','stinky',...etc] 

    messageContent = message.content
    if len(messageContent) > 0:
        for word in word_list:
            if word in messageContent:
                await message.delete()
                await message.channel.send('Please, be more respectful towards the other members!')

    #mod-mail to forward dms to specific channel as well as reply in dm
    if str(message.channel.type) == 'private':
        modmail_channel = discord.utils.get(client.get_all_channels(), name = 'creator-san')
        await modmail_channel.send(message.author.display_name + ' : ' + message.content)
    elif str(message.channel) == 'creator-san' and message.content.startswith('<'):
        member_mail_reply = message.mentions[0]
        index = message.content.index(" ")
        string = message.content
        mod_message = string[index:]
        await member_mail_reply.send(message.author.display_name + ' : ' + mod_message)

#welcome new members to the server
@client.command
async def joined(ctx, member: discord.Member):
    await ctx.send('Everybody welcome :\n', '{0.name} joined in {0.joined_at}'.format(member))


client.run(token)