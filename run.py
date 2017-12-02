import os
import configparser
from configparser import SafeConfigParser
import asyncio
from subprocess import call
import random
from discord.ext import commands
import traceback
import sys
import datetime

config = SafeConfigParser()
config.read('settings.ini')
token = config.get('main', 'token')
prefix = config.get('main', 'prefix')
description = config.get('main', 'desc')

bot = commands.Bot(command_prefix=prefix, description=description)

@bot.event
async def on_ready():
    print("------------------")
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("------------------")

@bot.command(pass_context="True",brief="Hello World!",aliases=['hi','hey'])
async def hello(ctx):
    """
    Will reply \"Hello <name>\".
    """
    await bot.say("Hello {}!".format(ctx.message.author.name))

@bot.command(pass_context="True",brief="Adds 500 to your currency count. Can be used once every 24 hours.",aliases=['money','coins'])
@commands.cooldown(1, 86400.0, commands.BucketType.user)
async def daily(ctx):
    """
    This command adds 500 coins to your wallet. Can only be used once per day. These coins are currently useless, and the command is still a WIP.
    """
    try:
        config = SafeConfigParser()
        currenttime = datetime.datetime.now()
        user = ctx.message.author
        config.read('money.ini')
        if config.has_section('{}'.format(user)):
            balance = int(config.get('{}'.format(user), 'balance'))
            balance = balance + 500
            balance = str(balance)
            config.set('{}'.format(user), 'balance', "{}".format(balance))
            config.set('{}'.format(user), 'lastused', '{}'.format(currenttime))
            with open('money.ini', 'w') as f:
                config.write(f)

            await bot.say('Balance updated! Current balance: `{}`.\nYou must wait 24hrs before using this command again. Until then, no output will be shown.'.format(balance))

        else:
            config.add_section('{}'.format(user))
            config.set('{}'.format(user), 'lastused', '{}'.format(currenttime))
            config.set('{}'.format(user), 'balance', '500')
            with open('money.ini', 'w') as f:
                config.write(f)

            await bot.say('User wallet created! Current balance: `500`\nYou must wait 24hrs before using this command again. Until then, no output will be shown.')

    except CommandOnCooldown as e:
            await bot.say(str(e))

@bot.command(pass_context="True",brief="Posts a reaction gif",aliases=["reaction","reactiongif","gif"])
async def react(ctx, arg):
    """
    Posts a reaction gif. Usage: \"sudo react [reaction]\"
    """
    try:
        config = SafeConfigParser()
        config.read('reactions.ini')
        gif = config.get('gifs','{}'.format(arg))
        await bot.say(gif)
    except Exception as e:
        s = str(e)
        bot.say(e)

@bot.command(pass_context="true",brief="Adds a reaction gif",aliases=['addreact','addreaction'])
async def addgif(ctx, arg1, arg2):
    """
    Adds a reaction image or reaction text.
    Only admins should be able to do this.
    """
    if "hallo mod" in [y.name.lower() for y in ctx.message.author.roles]:
        config = SafeConfigParser()
        config.read('reactions.ini')
        config.set('gifs', '{}'.format(arg1), '{}'.format(arg2))

        with open('reactions.ini', 'w') as f:
            config.write(f)

        await bot.say("Reaction added!")
    else:
    	await bot.say("Only admins can do that")

bot.run(token)