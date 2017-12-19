import discord
from discord.ext import commands
from configparser import SafeConfigParser
import datetime

class Currency:
    '''
    Currency system!
    '''
    def __init__(self, bot):
        self.bot = bot
        print('Addon "{}" loaded'.format(self.__class__.__name__))

    @commands.command(pass_context="True",brief="Adds 150 to your currency count. Can be used once every 24 hours.", aliases=['money','coins'])
    @commands.cooldown(1, 86400.0, commands.BucketType.user)
    async def daily(self, ctx):
        """
        This command adds 150 credits to your wallet. Can only be used once per day. This command is still a WIP.
        """
        config = SafeConfigParser()
        currenttime = datetime.datetime.now()
        user = ctx.message.author.id
        config.read('wallet.ini')
        if config.has_section('{}'.format(user)):
            balance = int(config.get('{}'.format(user), 'balance'))
            balance = balance + 150
            balance = str(balance)
            config.set('{}'.format(user), 'balance', "{}".format(balance))
            config.set('{}'.format(user), 'lastused', '{}'.format(currenttime))
            with open('wallet.ini', 'w') as f:
                config.write(f)

            await self.bot.say('Balance updated! Current balance: `{}`.'.format(balance))

        else:
            config.add_section('{}'.format(user))
            config.set('{}'.format(user), 'lastused', '{}'.format(currenttime))
            config.set('{}'.format(user), 'balance', '150')
            with open('wallet.ini', 'w') as f:
                config.write(f)

            await self.bot.say('User wallet created! Current balance: `150`')

def setup(bot):
    bot.add_cog(Currency(bot))