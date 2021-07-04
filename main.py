import discord
import os

from discord.message import Message

client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message: Message):
    if message.author == client.user:
        return

    if message.content.startswith("$test"):
        await message.channel.send("Hello you little sh*t")

TOKEN = os.getenv('TOKEN')
client.run(TOKEN)
