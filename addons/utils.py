import discord
from discord.ext import commands
from configparser import SafeConfigParser
import datetime

class Utils:
    '''
    User utilities. Anyone can use.
    '''
    def __init__(self, bot):
        self.bot = bot
        print('Addon "{}" loaded'.format(self.__class__.__name__))

    @commands.command(pass_context="True",brief="Gets user information.")
    async def userinfo(self, ctx, user: discord.Member):
        """
        Allows you to get information on a user simply by tagging them.
        """
        embed = discord.Embed(title='User Information Panel', description='User information for {}:'.format(user.name), color=0x00FF99)
        embed.set_thumbnail(url=user.avatar_url)
        embed.add_field(name='Name', value=user.name, inline=True)
        embed.add_field(name='ID', value=user.id, inline=True)
        embed.add_field(name='Status', value=user.status, inline=True)
        embed.add_field(name='Highest Role', value=user.top_role, inline=True)
        embed.add_field(name='Join Date', value=user.joined_at, inline=True)
        await self.bot.say(embed=embed)

    @commands.command(pass_context="True",brief="Adds 150 to your currency count. Can be used once every 24 hours.", aliases=['money','coin','wallet'])
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

            embed = discord.Embed(title='Added Balance', description='Your balance has been updated successfully!', color=0xFFD000)
            embed.add_field(name='Balance', value='Your balance is now {}.'.format(balance), inline=True)
            embed.set_thumbnail(url='https://i.imgur.com/akZqYz8.png')
            await self.bot.say(embed=embed)

        else:
            config.add_section('{}'.format(user))
            config.set('{}'.format(user), 'lastused', '{}'.format(currenttime))
            config.set('{}'.format(user), 'balance', '150')
            with open('wallet.ini', 'w') as f:
                config.write(f)

            embed = discord.Embed(title='Created Wallet', description='Your wallet has been created successfully!', color=0xFFD000)
            embed.add_field(name='Balance', value='Your balance is now 150.', inline=True)
            embed.set_thumbnail(url='https://i.imgur.com/akZqYz8.png')
            await self.bot.say(embed=embed)

    @commands.command(pass_context="True",brief="Posts a reaction gif",aliases=["reaction","reactiongif","gif","jif"])
    async def react(self, ctx, arg):
        """
        Posts a reaction image or copypasta from a keyword specified.
        """
        config = SafeConfigParser()
        config.read('reactions.ini')
        gif = config.get('gifs','{}'.format(arg))
        if gif.startswith('http'):
            embed = discord.Embed(title=None, description=None, color=0x00FF99)
            embed.set_image(url=gif)
            await self.bot.say(embed=embed)
        else:
            embed = discord.Embed(title=None, description=None, color=0x00FF99)
            embed.add_field(name=gif, value='Requested by {}'.format(ctx.message.author), inline=True)
            await self.bot.say(embed=embed)

    @commands.command(pass_context=True, brief='Displays server information')
    async def serverinfo(self, ctx):
        embed = discord.Embed(name='Server Information Panel', description='Here you go!', color=0x00FF99)
        embed.set_author(name='{}'.format(ctx.message.author.name) + '\'s Info Request')
        embed.add_field(name='Name', value=ctx.message.server.name, inline=True)
        embed.add_field(name='ID', value=ctx.message.server.id, inline=True)
        embed.add_field(name='Roles', value=len(ctx.message.server.roles), inline=True)
        embed.add_field(name='Members', value=len(ctx.message.server.members), inline=True)
        embed.set_thumbnail(url=ctx.message.server.icon_url)
        await self.bot.say(embed=embed)

def setup(bot):
    bot.add_cog(Utils(bot))