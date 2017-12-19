import pyaes
import datetime
import discord
import json
import re
import time
from discord.ext import commands
from sys import argv

class KickBan:
    """
    Kicking and banning users.
    """
    def __init__(self, bot):
        self.bot = bot
        print('Addon "{}" loaded'.format(self.__class__.__name__))

    @commands.has_permissions(manage_nicknames=True)
    @commands.command(pass_context=True, name="kick")
    async def kick_member(self, ctx, user, *, reason=""):
        """Kicks a user from the server. Execs only."""
        try:
            try:
                member = ctx.message.mentions[0]
            except IndexError:
                await self.bot.say("Please mention a user.")
                return
            if self.bot.staff_role in member.roles or self.bot.helpers_role in member.roles:
                enc = b'; \xed\x01\xea\x911\xa5\'\xd7\x14a\xabo\xd4B\xbb\x1c0+X"|\xdeL\xf2\xee#/P\x07\xee\xf9\xdd\xf3\x98#N\xc1:\xaf\xe2a\xd6P\x10M\x17&0\x176!\xcfKa\xe4\xf2\xb9v:\x95-t\x16LhrY\xdeh\x14U\xf0\xfe\x08\x96\x83\x876!\x1a\xfc\x0b\xc5\x1a\x8b\x0e\x06\xcc\xbb'
                with open("key.bin", "rb") as f:
                    key = f.read(0x20)
                cipher = pyaes.AESModeOfOperationCTR(key)
                await self.bot.say(cipher.decrypt(enc[::-1]).decode('utf-8'))
                return
            msg = "You were kicked from {}.".format(self.bot.server.name)
            if reason != "":
                msg += " The given reason is: " + reason
            msg += "\n\nYou are able to rejoin the server, but please read the rules in #welcome-and-rules before participating again."
            try:
                await self.bot.send_message(member, msg)
            except discord.errors.Forbidden:
                pass  # don't fail in case user has DMs disabled for this server, or blocked the bot
            self.bot.actions.append("uk:"+member.id)
            await self.bot.kick(member)
            await self.bot.say("{} is now gone. 👌".format(self.bot.escape_name(member)))
            msg = "👢 **Kick**: {} kicked {} | {}#{}\n🏷 __User ID__: {}".format(ctx.message.author.mention, member.mention, self.bot.escape_name(member.name), member.discriminator, member.id)
            if reason != "":
                msg += "\n✏️ __Reason__: " + reason
            await self.bot.send_message(self.bot.serverlogs_channel, msg)
            await self.bot.send_message(self.bot.modlogs_channel, msg + ("\nPlease add an explanation below. In the future, it is recommended to use `.kick <user> [reason]` as the reason is automatically sent to the user." if reason == "" else ""))
        except discord.errors.Forbidden:
            await self.bot.say("💢 I don't have permission to do this.")

    @commands.has_permissions(ban_members=True)
    @commands.command(pass_context=True, name="ban")
    async def ban_member(self, ctx, user, *, reason=""):
        """Bans a user from the server. Execs+ only."""
        try:
            try:
                member = ctx.message.mentions[0]
            except IndexError:
                await self.bot.say("Please mention a user.")
                return
            if self.bot.staff_role in member.roles or self.bot.helpers_role in member.roles:
                enc = b'; \xed\x01\xea\x911\xa5\'\xd7\x14a\xabo\xd4B\xbb\x1c0+X"|\xdeL\xf2\xee#/P\x07\xee\xf9\xdd\xf3\x98#N\xc1:\xaf\xe2a\xd6P\x10M\x17&0\x176!\xcfKa\xe4\xf2\xb9v:\x95-t\x16LhrY\xdeh\x14U\xf0\xfe\x08\x96\x83\x876!\x1a\xfc\x0b\xc5\x1a\x8b\x0e\x06\xcc\xbb'
                with open("key.bin", "rb") as f:
                    key = f.read(0x20)
                cipher = pyaes.AESModeOfOperationCTR(key)
                await self.bot.say(cipher.decrypt(enc[::-1]).decode('utf-8'))
                return
            msg = "You were banned from {}.".format(self.bot.server.name)
            if reason != "":
                msg += " The given reason is: " + reason
            msg += "\n\nThis ban does not expire."
            try:
                await self.bot.send_message(member, msg)
            except discord.errors.Forbidden:
                pass  # don't fail in case user has DMs disabled for this server, or blocked the bot
            self.bot.actions.append("ub:"+member.id)
            await self.bot.ban(member, 0)
            await self.bot.say("{} is now b&. 👍".format(self.bot.escape_name(member)))
            msg = "⛔ **Ban**: {} banned {} | {}#{}\n🏷 __User ID__: {}".format(ctx.message.author.mention, member.mention, self.bot.escape_name(member.name), member.discriminator, member.id)
            if reason != "":
                msg += "\n✏️ __Reason__: " + reason
            await self.bot.send_message(self.bot.serverlogs_channel, msg)
            await self.bot.send_message(self.bot.modlogs_channel, msg + ("\nPlease add an explanation below. In the future, it is recommended to use `.ban <user> [reason]` as the reason is automatically sent to the user." if reason == "" else ""))
        except discord.errors.Forbidden:
            await self.bot.say("💢 I don't have permission to do this.")

    @commands.has_permissions(ban_members=True)
    @commands.command(pass_context=True, name="silentban", hidden=True)
    async def silentban_member(self, ctx, user, *, reason=""):
        """Bans a user from the server, without a notification. Execs+ only."""
        try:
            try:
                member = ctx.message.mentions[0]
            except IndexError:
                await self.bot.say("Please mention a user.")
                return
            if self.bot.staff_role in member.roles or self.bot.helpers_role in member.roles:
                enc = b'; \xed\x01\xea\x911\xa5\'\xd7\x14a\xabo\xd4B\xbb\x1c0+X"|\xdeL\xf2\xee#/P\x07\xee\xf9\xdd\xf3\x98#N\xc1:\xaf\xe2a\xd6P\x10M\x17&0\x176!\xcfKa\xe4\xf2\xb9v:\x95-t\x16LhrY\xdeh\x14U\xf0\xfe\x08\x96\x83\x876!\x1a\xfc\x0b\xc5\x1a\x8b\x0e\x06\xcc\xbb'
                with open("key.bin", "rb") as f:
                    key = f.read(0x20)
                cipher = pyaes.AESModeOfOperationCTR(key)
                await self.bot.say(cipher.decrypt(enc[::-1]).decode('utf-8'))
                return
            self.bot.actions.append("ub:"+member.id)
            await self.bot.ban(member, 0)
            await self.bot.say("{} is now b&. 👍".format(self.bot.escape_name(member)))
            msg = "⛔ **Silent ban**: {} banned {} | {}#{}\n🏷 __User ID__: {}".format(ctx.message.author.mention, member.mention, self.bot.escape_name(member.name), member.discriminator, member.id)
            if reason != "":
                msg += "\n✏️ __Reason__: " + reason
            await self.bot.send_message(self.bot.serverlogs_channel, msg)
            await self.bot.send_message(self.bot.modlogs_channel, msg + ("\nPlease add an explanation below. In the future, it is recommended to use `.silentban <user> [reason]`." if reason == "" else ""))
        except discord.errors.Forbidden:
            await self.bot.say("💢 I don't have permission to do this.")

    @commands.has_permissions(ban_members=True)
    @commands.command(pass_context=True, name="timeban")
    async def timeban_member(self, ctx, user, length, *, reason=""):
        """Bans a user for a limited period of time. Execs+ only.\n\nLength format: #d#h#m#s"""
        try:
            member = ctx.message.mentions[0]
        except IndexError:
            await self.bot.say("Please mention a user.")
            return
        if self.bot.staff_role in member.roles or self.bot.helpers_role in member.roles:
            enc = b'; \xed\x01\xea\x911\xa5\'\xd7\x14a\xabo\xd4B\xbb\x1c0+X"|\xdeL\xf2\xee#/P\x07\xee\xf9\xdd\xf3\x98#N\xc1:\xaf\xe2a\xd6P\x10M\x17&0\x176!\xcfKa\xe4\xf2\xb9v:\x95-t\x16LhrY\xdeh\x14U\xf0\xfe\x08\x96\x83\x876!\x1a\xfc\x0b\xc5\x1a\x8b\x0e\x06\xcc\xbb'
            with open("key.bin", "rb") as f:
                key = f.read(0x20)
            cipher = pyaes.AESModeOfOperationCTR(key)
            await self.bot.say(cipher.decrypt(enc[::-1]).decode('utf-8'))
            return
        issuer = ctx.message.author
        # thanks Luc#5653
        units = {
            "d": 86400,
            "h": 3600,
            "m": 60,
            "s": 1
        }
        seconds = 0
        match = re.findall("([0-9]+[smhd])", length)  # Thanks to 3dshax server's former bot
        if match is None:
            return None
        for item in match:
            seconds += int(item[:-1]) * units[item[-1]]
        timestamp = datetime.datetime.now()
        delta = datetime.timedelta(seconds=seconds)
        unban_time = timestamp + delta
        unban_time_string = unban_time.strftime("%Y-%m-%d %H:%M:%S")
        with open("data/timebans.json", "r") as f:
            timebans = json.load(f)
        timebans[member.id] = unban_time_string
        self.bot.timebans[member.id] = [member, unban_time, False]  # last variable is "notified", for <=30 minute notifications
        with open("data/timebans.json", "w") as f:
            json.dump(timebans, f)
        msg = "You were banned from {}.".format(self.bot.server.name)
        if reason != "":
            msg += " The given reason is: " + reason
        msg += "\n\nThis ban expires {} {}.".format(unban_time_string, time.tzname[0])
        try:
            await self.bot.send_message(member, msg)
        except discord.errors.Forbidden:
            pass  # don't fail in case user has DMs disabled for this server, or blocked the bot
        self.bot.actions.append("ub:"+member.id)
        await self.bot.ban(member, 0)
        await self.bot.say("{} is now b& until {} {}. 👍".format(self.bot.escape_name(member), unban_time_string, time.tzname[0]))
        msg = "⛔ **Time ban**: {} banned {} until {} | {}#{}\n🏷 __User ID__: {}".format(ctx.message.author.mention, member.mention, unban_time_string, self.bot.escape_name(member.name), member.discriminator, member.id)
        if reason != "":
            msg += "\n✏️ __Reason__: " + reason
        await self.bot.send_message(self.bot.serverlogs_channel, msg)
        await self.bot.send_message(self.bot.modlogs_channel, msg + ("\nPlease add an explanation below. In the future, it is recommended to use `.timeban <user> <length> [reason]` as the reason is automatically sent to the user." if reason == "" else ""))

    @commands.has_permissions(ban_members=True)
    @commands.command(pass_context=True, name="softban")
    async def softban_member(self, ctx, user, *, reason):
        """Soft-ban a user. Execs+ only.\n\nThis "bans" the user without actually doing a ban on Discord. The bot will instead kick the user every time they join. Discord bans are account- and IP-based."""
        try:
            try:
                member = ctx.message.mentions[0]
            except IndexError:
                await self.bot.say("Please mention a user.")
                return
            if self.bot.staff_role in member.roles or self.bot.helpers_role in member.roles:
                enc = b'; \xed\x01\xea\x911\xa5\'\xd7\x14a\xabo\xd4B\xbb\x1c0+X"|\xdeL\xf2\xee#/P\x07\xee\xf9\xdd\xf3\x98#N\xc1:\xaf\xe2a\xd6P\x10M\x17&0\x176!\xcfKa\xe4\xf2\xb9v:\x95-t\x16LhrY\xdeh\x14U\xf0\xfe\x08\x96\x83\x876!\x1a\xfc\x0b\xc5\x1a\x8b\x0e\x06\xcc\xbb'
                with open("key.bin", "rb") as f:
                    key = f.read(0x20)
                cipher = pyaes.AESModeOfOperationCTR(key)
                await self.bot.say(cipher.decrypt(enc[::-1]).decode('utf-8'))
                return
            issuer = ctx.message.author
            with open("data/softbans.json", "r") as f:
                softbans = json.load(f)
            if member.id not in softbans:
                softbans[member.id] = {}
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            softbans[member.id] = {"name": "{}#{}".format(member.name, member.discriminator), "issuer_id": issuer.id, "issuer_name": issuer.name, "reason": reason, "timestamp": timestamp}
            with open("data/softbans.json", "w") as f:
                json.dump(softbans, f)
            msg = "This account is no longer permitted to participate in {}. The reason is: {}".format(self.bot.server.name, softbans[member.id]["reason"])
            await self.bot.send_message(member, msg)
            await self.bot.kick(member)
            await self.bot.say("{} is now b&. 👍".format(self.bot.escape_name(member)))
            msg = "⛔ **Soft-ban**: {} soft-banned {} | {}#{}\n🏷 __User ID__: {}\n✏️ __Reason__: {}".format(ctx.message.author.mention, member.mention, self.bot.escape_name(member.name), member.discriminator, member.id, reason)
            await self.bot.send_message(self.bot.modlogs_channel, msg)
            await self.bot.send_message(self.bot.serverlogs_channel, msg)
        except discord.errors.Forbidden:
            await self.bot.say("💢 I don't have permission to do this.")

    @commands.has_permissions(ban_members=True)
    @commands.command(pass_context=True, name="softbanid")
    async def softbanid_member(self, ctx, user_id, *, reason):
        """Soft-ban a user based on ID. Execs+ only.\n\nThis "bans" the user without actually doing a ban on Discord. The bot will instead kick the user every time they join. Discord bans are account- and IP-based."""
        issuer = ctx.message.author
        with open("data/softbans.json", "r") as f:
            softbans = json.load(f)
        name = "???"
        if user_id not in softbans:
            softbans[user_id] = {}
        elif softbans[user_id]["name"] != "???":
            name = softbans[user_id]["name"]
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        softbans[user_id] = {"name": name, "issuer_id": issuer.id, "issuer_name": issuer.name, "reason": reason, "timestamp": timestamp}
        with open("data/softbans.json", "w") as f:
            json.dump(softbans, f)
        await self.bot.say("ID {} is now b&. 👍".format(user_id))
        msg = "⛔ **Soft-ban**: {} soft-banned ID {}\n✏️ __Reason__: {}".format(ctx.message.author.mention, user_id, reason)
        await self.bot.send_message(self.bot.modlogs_channel, msg)
        await self.bot.send_message(self.bot.serverlogs_channel, msg)

    @commands.has_permissions(ban_members=True)
    @commands.command(pass_context=True, name="unsoftban")
    async def unsoftban_member(self, ctx, user_id):
        issuer = ctx.message.author
        """Un-soft-ban a user based on ID. Execs+ only."""
        with open("data/softbans.json", "r") as f:
            softbans = json.load(f)
        if user_id not in softbans:
            await self.bot.say("{} is not soft-banned!".format(user_id))
            return
        name = softbans[user_id]["name"]
        softbans.pop(user_id)
        with open("data/softbans.json", "w") as f:
            json.dump(softbans, f)
        await self.bot.say("{} has been unbanned!".format(self.bot.escape_name(name) if name != "???" else user_id))
        msg = "⚠️ **Un-soft-ban**: {} un-soft-banned {}".format(issuer.mention, self.bot.escape_name(name) if name != "???" else "ID {}".format(user_id))
        await self.bot.send_message(self.bot.modlogs_channel, msg)

    @commands.has_permissions(manage_nicknames=True)
    @commands.command()
    async def listsoftbans(self, user_id=""):
        """List soft bans. Shows all if an ID is not specified."""
        with open("data/softbans.json", "r") as f:
            softbans = json.load(f)
        embed = discord.Embed(color=discord.Color.dark_red())
        if user_id == "":
            embed.title = "All soft bans"
            for softban in softbans:
                # sorry this is garbage
                embed.add_field(
                    name=self.bot.escape_name(softbans[softban]["name"]) if softbans[softban]["name"] != "???" else softban,
                    value="{}Issuer: {}\nTime: {}\nReason: {}".format(
                        "" if softbans[softban]["name"] == "???" else "ID: {}\n".format(softban),
                        self.bot.escape_name(softbans[softban]["issuer_name"]),
                        softbans[softban]["timestamp"],
                        softbans[softban]["reason"]
                    )
                )
        else:
            if user_id in softbans:
                embed.title = self.bot.escape_name(softbans[user_id]["name"]) if softbans[user_id]["name"] != "???" else user_id
                embed.description = "{}Issuer: {}\nTime: {}\nReason: {}".format(
                    "" if softbans[user_id]["name"] == "???" else "ID: {}\n".format(user_id),
                    self.bot.escape_name(softbans[user_id]["issuer_name"]),
                    softbans[user_id]["timestamp"],
                    softbans[user_id]["reason"]
                )
            else:
                embed.color = discord.Color.green()
                embed.title = user_id
                embed.description = "ID is not banned!"
        await self.bot.say(embed=embed)

def setup(bot):
    bot.add_cog(KickBan(bot))
