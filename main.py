import os
import requests
import asyncio
import discord
from discord.ext import commands

client = commands.Bot(command_prefix='!')

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

def get_text(id):
    url = f"https://npayapi-in.herokuapp.com/get?id={id}"
    req = requests.get(url)
    if req.status_code == 200:
        data = req.json()
        if data["status"] == True:
            text = f"|--**Here The Details Of {id}**--\n|->**Name**: `{data['name']}`\n|->**Father Name**: `{data['father_name']}`\n|->**Admin No**: `{data['id_no']}`\n|->**Class**: `{data['class_n']}`\n|->**Branch**: `{data['branch']}`\n|->**Due Amount**: `{data['due_amount']}`\n|->**Mobile Number**: || `{data['mobile']}` ||\nCreated By [Seshu Sai](https://www.instagram.com/_yarra.s.s_/)"
            return text
        else:
            return f"**No Details Found For {id}**\nCreated By [Seshu Sai](https://www.instagram.com/_yarra.s.s_/)"
    else:
        return f"**No Details Found For {id}**\nCreated By [Seshu Sai](https://www.instagram.com/_yarra.s.s_/)"



@client.command()
async def ping(ctx):
    await ctx.send('Pong!')

@client.event
async def on_message(message):
    if message.content.startswith('!info'):
        text = message.content.replace('!info ','')
        if len(text) == 7:
            tex = get_text(int(text))
            await message.channel.send(tex)
        else:
            await message.channel.send("**Invalid ID**\nCreated By [Seshu Sai](https://www.instagram.com/_yarra.s.s_/")
    elif message.content.startswith('!help'):
        await message.channel.send("I'll Get Information of Narayana Student Using Admission Number\nTo Get Information Use /info\n Your Admission Number Must Me 7 Digits And Number\nI'm Created By [Seshu Sai](https://www.instagram.com/_yarra.s.s_/)")

TOKEN = os.environ.get('BOT_TOKEN')

client.run(TOKEN)
