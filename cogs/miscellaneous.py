import discord
from discord.ext import commands
import random


class Miscellaneous(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def test(self, ctx):
        await ctx.send('test passed')

    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.change_presence(status=discord.Status.online, activity=discord.Game('I burn'))
        print("Bot is online")

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round(self.client.latency * 1000)}ms')

    @commands.command()
    async def users(self, ctx):
        """Shows number of members in server"""
        await ctx.send(f"""# of Members is {len(ctx.guild.members)}""")

    @commands.command(aliases=['8ball'])
    async def _8ball(self, ctx, *, question):
        """Responds either affirming or refuting input statement. Format: ^8ball [yes/no statement]"""
        responses = ["It is certain.",
                     "It is decidedly so.",
                     "Without a doubt.",
                     "Yes - definitely.",
                     "You may rely on it.",
                     "As I see it, yes.",
                     "Most likely.",
                     "Outlook good.",
                     "Yes.",
                     "Signs point to yes.",
                     "Don't count on it.",
                     "My reply is no.",
                     "My sources say no.",
                     "Outlook not so good.",
                     "Very doubtful.",
                     "Absolutely not",
                     "You should know this you pabo",
                     "Figure it out yourself",
                     "Probably not"]
        await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

    @commands.command()
    async def say(self, ctx, *, message):
        """Commands bot to say a message. Format: ^say [message]"""
        await ctx.channel.purge(limit=1)
        await ctx.channel.send(message)


def setup(client):
    client.add_cog(Miscellaneous(client))
