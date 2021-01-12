import discord
from discord.ext import commands
import json


class Moderation(commands.Cog):

    def __init__(self, client):
        self.client = client

    @staticmethod
    def get_welcome_id(member):
        """Gets chosen welcome message channel ID for guild"""
        with open('welcome_id.json') as f:
            channel = json.load(f)

        return channel[str(member.guild.id)]

    @staticmethod
    def get_welcome_msg(member):
        """Gets chosen welcome message for guild"""
        with open('welcome_msg.json') as f:
            msg = json.load(f)

        return msg[str(member.guild.id)]

    @commands.command()
    async def join(self, ctx):
        """Simulates an on_member_join event"""
        await self.on_member_join(ctx.author)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Sends a welcome message to server chosen"""

        channel_s = self.client.get_channel(self.get_welcome_id(member))
        msg = self.get_welcome_msg(member)

        await channel_s.send(f'{msg}')

    @commands.command(aliases=['changeprefix', 'setprefix'])
    @commands.has_permissions(manage_guild=True)
    async def change_prefix(self, ctx, *, new_pre):
        """Changes the server prefix for Soyeon Bot. Default is '^'.
        Aliases: changeprefix, setprefix"""
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)

        prefixes[str(ctx.guild.id)] = new_pre

        with open('prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)

        await ctx.send(f'Prefix changed to `{new_pre}`')

    @commands.command(aliases=['setwelcome'])
    @commands.has_permissions(manage_guild=True)
    async def set_welcome(self, ctx, channel, *, text):
        """Sets a welcome message for your server. Format: ^setwelcome [channel] [message]"""
        with open('welcome_msg.json', 'r') as f:
            setwelcome = json.load(f)

            setwelcome[str(ctx.guild.id)] = text

        with open('welcome_msg.json', 'w') as f:
            json.dump(setwelcome, f, indent=4)

        with open('welcome_id.json', 'r') as f:
            channelname = json.load(f)

            channel_id = discord.utils.get(ctx.guild.channels, name=channel).id
            channelname[str(ctx.guild.id)] = channel_id

        with open('welcome_id.json', 'w') as f:
            json.dump(channelname, f, indent=4)

        await ctx.send(f'Welcome message set to: \n{text}\nIt will be sent in the #{channel} channel')

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        """Kicks a member from the server. Format: ^kick [member] [reason]"""
        if reason is None:
            await member.send("You have been kicked")
        else:
            await member.send(f"You have been kicked for {reason}")
        await member.kick(reason=reason)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        """Bans a member from the server. Format: ^ban [member] [reason]"""
        await member.send(f'You have been banned for {reason}')
        await member.ban(reason=reason)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        """Unbans a member from the server. Format: ^unban [member]"""
        banned_users = await ctx.guild.bans()
        member_n, member_dis = member.split("#")
        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_n, member_dis):
                await ctx.guild.unban(user)
                return

    @commands.command()
    async def clear(self, ctx, amount=5):
        """Clears a given number of messages. Format: ^clear [number]"""
        await ctx.channel.purge(limit=amount)


def setup(client):
    client.add_cog(Moderation(client))
