import discord
from discord.ext import commands

class Changeme: # Replace "Changeme" with the name of the addon
    '''
    Description
    '''
    def __init__(self, bot):
        self.bot = bot
        print('Addon "{}" loaded'.format(self.__class__.__name__))

    @commands.command(pass_context="True",brief="Short description",aliases=["alternate","names","for","command"]) # Make sure to replace those!
    async def changeme(self, ctx, arg): # Don't forget to replace "changeme" with the name of your command!
        # Do stuff here!

def setup(bot):
    bot.add_cog(Changeme(bot)) # Replace "Changeme" with the name of the addon