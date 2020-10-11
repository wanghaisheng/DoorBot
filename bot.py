#!/usr/bin/python3

import os, time, asyncio, requests, sys
import config, logging
import discord
from discord.ext import commands

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


# initialize bot and set prefix
bot = commands.Bot(command_prefix = ('D!', 'd!'))

# System variables
BOT_TOKEN = os.getenv('BOT_TOKEN')

path = os.path.dirname(sys.argv[0])
for filename in os.listdir('extensions'):
    print(filename)
    if filename.endswith('.py'):
        bot.load_extension(f'extensions.{filename[:-3]}')

# What bot should do once fully booted
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

    # Discord Acitivity
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="for 'd!'"))


try:
    bot.run(BOT_TOKEN)
except KeyboardInterrupt:
    exit
