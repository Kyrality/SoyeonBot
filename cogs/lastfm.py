import requests
import discord
from discord.ext import commands
import json
from keys import lastfm_api_key, lastfm_root_url


class Lastfm(commands.Cog):

    def __init__(self, client):
        self.client = client

    @staticmethod
    def get_user(ctx):
        with open('lastfm_user.json') as f:
            lastfm_usernames = json.load(f)
            member_username = lastfm_usernames[str(ctx.author)]
        return member_username

    @staticmethod
    def time_period(period):
        week = ["7day", "7 days", "7days", "7 day", "week"]
        month = ["1month", "month"]
        three_months = ["3month", "3 months"]
        six_months = ["6month", "6 months"]
        year = ["12month", "12months", "year", "12 months"]
        if period in week:
            return week[0]
        elif period in month:
            return month[0]
        elif period in three_months:
            return three_months[0]
        elif period in six_months:
            return six_months[0]
        elif period in year:
            return year[0]
        else:
            return "overall"

    @commands.command(aliases=['setuser'])
    async def set_user(self, ctx, username):
        with open('lastfm_user.json') as f:
            lastfm_usernames = json.load(f)

        if lastfm_usernames[str(ctx.author)] == username:
            await ctx.channel.send("Username already set!")

        else:
            lastfm_usernames[str(ctx.author)] = username
            with open('lastfm_user.json', 'w') as f:
                json.dump(lastfm_usernames, f, indent=4)
            await ctx.channel.send(f'{ctx.author.mention}, your lastfm account, {username}, has been set')

    @commands.command(aliases=['toptracks', 'tt'])
    async def top_tracks(self, ctx, period='overall'):

        tt_params = {
            "user": self.get_user(ctx),
            "period": self.time_period(period),
            "api_key": lastfm_api_key,
            "method": "user.getTopTracks",
            "format": "json",
            "limit": "10"
        }

        response = requests.get(lastfm_root_url, params=tt_params).json()

        track = discord.Embed(title=f"{self.get_user(ctx)}'s top tracks", description=f"({period})")
        for data in response["toptracks"]["track"]:
            rank = data["@attr"]["rank"]
            artist_name = data["artist"]["name"]
            song_name = data["name"]
            number = data["playcount"]
            track.add_field(name=f"{rank}. ({number} plays)", value=f"{song_name} by {artist_name}", inline=False)

        await ctx.channel.send(embed=track)


def setup(client):
    client.add_cog(Lastfm(client))
