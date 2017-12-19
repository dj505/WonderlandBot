import datetime
import discord
import os
import random
import re
import string
from discord.ext import commands
from sys import argv

class Extras:
    """
    Extra things.
    """
    def __init__(self, bot):
        self.bot = bot
        print('Addon "{}" loaded'.format(self.__class__.__name__))

    prune_key = "nokey"

    @commands.command()
    async def membercount(self):
        """Prints the member count of the server."""
        await self.bot.say("{} has {:,} members!".format(self.bot.server.name, self.bot.server.member_count))

    @commands.has_permissions(ban_members=True)
    @commands.command(hidden=True)
    async def embedtext(self, *, text):
        """Embed content."""
        await self.bot.say(embed=discord.Embed(description=text))

    @commands.has_permissions(manage_nicknames=True)
    @commands.command()
    async def estprune(self, days=30):
        """Estimate count of members that would be pruned based on the amount of days. Execs only."""
        if days > 30:
            await self.bot.say("Maximum 30 days")
            return
        if days < 1:
            await self.bot.say("Minimum 1 day")
            return
        msg = await self.bot.say("I'm figuring this out!".format(self.bot.server.name))
        count = await self.bot.estimate_pruned_members(server=self.bot.server, days=days)
        await self.bot.edit_message(msg, "{:,} members inactive for {} day(s) would be kicked from {}!".format(count, days, self.bot.server.name))

    @commands.has_permissions(manage_nicknames=True)
    @commands.command()
    async def activecount(self, days=30):
        """Shows the number of members active in the past amount of days. Execs only."""
        if days > 30:
            await self.bot.say("Maximum 30 days")
            return
        if days < 1:
            await self.bot.say("Minimum 1 day")
            return
        msg = await self.bot.say("I'm figuring this out!".format(self.bot.server.name))
        count = await self.bot.estimate_pruned_members(server=self.bot.server, days=days)
        if days == 1:
            await self.bot.edit_message(msg, "{:,} members were active today in {}!".format(self.bot.server.member_count-count, self.bot.server.name))
        else:
            await self.bot.edit_message(msg, "{:,} members were active in the past {} days in {}!".format(self.bot.server.member_count-count, days, self.bot.server.name))


    @commands.has_permissions(manage_nicknames=True)
    @commands.command(pass_context=True)
    async def prune30(self, ctx, key=""):
        """Prune members that are inactive for 30 days. Execs only."""
        if self.bot.pruning > 0:
            await self.bot.say("Pruning is already in progress.")
            return
        if key != self.prune_key:
            if key != "":
                await self.bot.say("That's not the correct key.")
            self.prune_key = ''.join(random.sample(string.ascii_letters, 8))
            await self.bot.say("Are you sure you want to prune members inactive for 30 days?\nTo see how many members get kicked, use `k!estprune`.\nTo confirm the prune, use the command `k!prune30 {}`.".format(self.prune_key))
            return
        self.prune_key = ''.join(random.sample(string.ascii_letters, 8))
        await self.bot.say("Starting pruning!")
        count = await self.bot.prune_members(self.bot.server, days=30)
        self.bot.pruning = count
        await self.bot.send_message(self.bot.mods_channel, "{:,} are currently being kicked from {}!".format(count, self.bot.server.name))
        msg = "👢 **Prune**: {} pruned {:,} members".format(ctx.message.author.mention, count)
        await self.bot.send_message(self.bot.modlogs_channel, msg)

    @commands.command()
    async def de(self):
        invalid()

    @commands.has_permissions(administrator=True)
    @commands.command(pass_context=True, hidden=True)
    async def dumpchannel(self, ctx, channel_name, limit=100):
        """Dump 100 messages from a channel to a file."""
        channel = ctx.message.channel_mentions[0]
        await self.bot.say("Dumping {} messages from {}".format(limit, channel.mention))
        os.makedirs("#{}-{}".format(channel.name, channel.id), exist_ok=True)
        async for message in self.bot.logs_from(channel, limit=limit):
            with open("#{}-{}/{}.txt".format(channel.name, channel.id, message.id), "w") as f:
                f.write(message.content)
        await self.bot.say("Done!")

def setup(bot):
    bot.add_cog(Extras(bot))
