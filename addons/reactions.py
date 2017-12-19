import discord
from discord.ext import commands
from configparser import SafeConfigParser

class Reactions:
    '''
    Reaction gifs and text. Only Execs or higher can add entries.
    '''
    def __init__(self, bot):
        self.bot = bot
        print('Addon "{}" loaded'.format(self.__class__.__name__))

    @commands.command(pass_context="True",brief="Posts a reaction gif",aliases=["reaction","reactiongif","gif"])
    async def react(self, ctx, arg):
        """
        Posts a reaction gif. Usage: \"k!react [reaction]\"
        """
        config = SafeConfigParser()
        config.read('reactions.ini')
        gif = config.get('gifs','{}'.format(arg))
        await self.bot.say(gif)

    @commands.command(pass_context="true",brief="Adds a reaction gif",aliases=['addreact','addreaction'])
    async def addgif(self, ctx, arg1, arg2):
        """
        Adds a reaction gif.
        Only executives should be able to do this.
        """
        if "executives" in [y.name.lower() for y in ctx.message.author.roles]:
            config = SafeConfigParser()
            config.read('reactions.ini')
            config.set('gifs', '{}'.format(arg1), str('{}'.format(arg2)))

            with open('reactions.ini', 'w') as f:
                config.write(f)

            await self.bot.say("Config updated successfully")
        else:
            await self.bot.say("Only Executives can do that")

def setup(bot):
    bot.add_cog(Reactions(bot))