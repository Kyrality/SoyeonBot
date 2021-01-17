import discord
from discord.ext import commands
import json
from keys import lastfm_api_key, lastfm_root_url, client_session


class Lastfm(commands.Cog):

    def __init__(self, client):
        self.client = client

    @staticmethod
    def get_user(ctx):
        """Gets LastFM Username associated with user"""
        with open('lastfm_user.json') as f:
            lastfm_usernames = json.load(f)
            member_username = lastfm_usernames[str(ctx.author)]
        return member_username

    @staticmethod
    def get_time_period(period_in):
        """Converts period input into response format"""
        period_lower = period_in.lower()
        period = period_lower.replace(" ", "")

        _1week = ["7day", "7days", "week"]
        month = ["1month", "month"]
        three_months = ["3month", "3months"]
        six_months = ["6month", "6months"]
        _1year = ["12month", "12months", "year"]
        if period in _1week:
            return _1week[0]
        elif period in month:
            return month[0]
        elif period in three_months:
            return three_months[0]
        elif period in six_months:
            return six_months[0]
        elif period in _1year:
            return _1year[0]
        else:
            return "overall"

    @staticmethod
    def get_params(method, user, period=None, limit=10, page=1):
        """Formats paramaters for LastFM API request"""
        params = {
            "api_key": lastfm_api_key,
            "format": "json",
        }
        if period:
            params['period'] = period
        if user:
            params['user'] = user
        if method:
            params['method'] = method
        if limit:
            params['limit'] = limit
        if page:
            params['page'] = page
        return params

    @staticmethod
    async def get_fm_response(params):
        """Recieves a LastFM Response"""
        async with client_session.get(lastfm_root_url, params=params) as r:
            return await r.json()

    @commands.command(aliases=['setuser'])
    async def set_user(self, ctx, username):
        """Sets a LastFM account with user. Format: ^setuser [lastfm username]"""

        with open('lastfm_user.json') as f:
            lastfm_usernames = json.load(f)

        lastfm_usernames[str(ctx.author)] = username

        with open('lastfm_user.json', 'w') as f:
            json.dump(lastfm_usernames, f, indent=4)
        await ctx.channel.send(f'{ctx.author.mention}, your lastfm account, {username}, has been set')

    @commands.command(aliases=['nowplaying', 'np'])
    async def now_playing(self, ctx):
        """Shows currently playing track. Format: ^nowplaying
        Aliases: np"""

        method = "user.getRecentTracks"
        user = self.get_user(ctx)

        rt_params = self.get_params(method, user, period=None)

        response = await self.get_fm_response(rt_params)
        data = response["recenttracks"]["track"][0]

        artists = discord.Embed(title=f"{self.get_user(ctx)}'s last listened", color=0x3DFFBE)

        try:
            time_in = f'Listened on {data["date"]["#text"]}'
            time = time_in.replace(",", " at")
        except:
            time = "Currently Listening"
        artist_name = data["artist"]["#text"]
        album_name = data["album"]["#text"]
        song_name = data["name"]
        artists.add_field(name=f"{song_name}", value=f"On {album_name} by {artist_name}\n{time}", inline=False)

        await ctx.channel.send(embed=artists)

    @commands.command(aliases=['toptracks', 'tt'])
    async def top_tracks(self, ctx, *, period='overall'):
        """Shows top 10 tracks for associated LastFM Account. Format: ^toptracks [time period]
        Aliases: tt
        Time periods: week, month, 2 months, 6 months, year. Defaults to overall."""

        method = "user.getTopTracks"
        user = self.get_user(ctx)
        time_period = self.get_time_period(period)

        tt_params = self.get_params(method, user, time_period)

        response = await self.get_fm_response(tt_params)

        tracks = discord.Embed(title=f"{self.get_user(ctx)}'s top tracks", description=f"({time_period})", color=0x3DFFBE)

        for data in response["toptracks"]["track"]:
            rank = data["@attr"]["rank"]
            artist_name = data["artist"]["name"]
            song_name = data["name"]
            number = data["playcount"]
            tracks.add_field(name=f"{rank}. ({number} plays)", value=f"{song_name} by {artist_name}", inline=False)

        await ctx.channel.send(embed=tracks)

    @commands.command(aliases=['topartists', 'ta'])
    async def top_artists(self, ctx, *, period='overall'):
        """Shows top 10 artists for associated LastFM Account. Format: ^topartists [time period]
        Aliases: ta
        Time periods: week, month, 2 months, 6 months, year. Defaults to overall."""

        method = 'user.getTopArtists'
        user = self.get_user(ctx)
        time_period = self.get_time_period(period)

        ta_params = self.get_params(method, user, time_period)

        response = await self.get_fm_response(ta_params)

        artists = discord.Embed(title=f"{self.get_user(ctx)}'s top artis", description=f"({time_period})", color=0x3DFFBE)

        for data in response["topartists"]["artist"]:
            rank = data["@attr"]["rank"]
            artist_name = data["name"]
            number = data["playcount"]
            artists.add_field(name=f"{rank}. ({number} plays)", value=f"{artist_name}", inline=False)

        await ctx.channel.send(embed=artists)

    @commands.command(aliases=['topalbums', 'tal'])
    async def top_albums(self, ctx, *, period='overall'):
        """Shows top 10 albums for associated LastFM Account. Format: ^topalbums [time period]
        Aliases: tal
        Time periods: week, month, 2 months, 6 months, year. Defaults to overall."""

        method = 'user.getTopAlbums'
        user = self.get_user(ctx)
        time_period = self.get_time_period(period)

        tal_params = self.get_params(method, user, time_period)

        response = await self.get_fm_response(tal_params)

        albums = discord.Embed(title=f"{self.get_user(ctx)}'s top albums", description=f"({time_period})", color=0x3DFFBE)

        for data in response["topalbums"]["album"]:
            rank = data["@attr"]["rank"]
            artist_name = data["artist"]["name"]
            album_name = data["name"]
            number = data["playcount"]
            albums.add_field(name=f"{rank}. ({number} plays)", value=f"{album_name} by {artist_name}", inline=False)

        await ctx.channel.send(embed=albums)

    @commands.command(aliases=['recenttracks', 'rt'])
    async def recent_tracks(self, ctx):
        """Shows last 10 recent tracks for associated LastFM account. Format: ^recenttracks
        Aliases: rt"""

        method = 'user.getRecentTracks'
        user = self.get_user(ctx)

        rt_params = self.get_params(method, user, period=None)

        response = await self.get_fm_response(rt_params)

        artists = discord.Embed(title=f"{self.get_user(ctx)}'s recent tracks", color=0x3DFFBE)

        for data in response["recenttracks"]["track"]:
            try:
                time_in = f'Listened on {data["date"]["#text"]}'
                time = time_in.replace(",", " at")
            except:
                time = "Currently Listening"
            artist_name = data["artist"]["#text"]
            album_name = data["album"]["#text"]
            song_name = data["name"]
            artists.add_field(name=f"{song_name}", value=f"On {album_name} by {artist_name}\n{time}", inline=False)

        await ctx.channel.send(embed=artists)

    @commands.command(aliases=['tto', 'toptracksof'])
    async def top_tracks_of(self, ctx, *, artist_period):
        """Shows most listened tracks of chosen artist for associated LastFM account. Format: ^toptracksof artist period
        Aliases: tto
        Time periods: week, month, year. Defaults to overall."""

        input_nospace = artist_period.replace(" ", "")
        input = input_nospace.lower()

        time_period_in = "overall"
        artist = input

        if input.endswith("week"):
            time_period_in = "week"
            artist = input[:-4]
        elif input.endswith("month"):
            time_period_in = "month"
            artist = input[:-5]
        elif input.endswith("year"):
            time_period_in = "year"
            artist = input[:-4]

        method = 'user.getTopTracks'
        user = self.get_user(ctx)
        time_period = self.get_time_period(time_period_in)

        limit = 1000

        rt_params = self.get_params(method, user, time_period, limit)

        response = await self.get_fm_response(rt_params)

        tracks = discord.Embed(title=f"{self.get_user(ctx)}'s top {artist} tracks", description=f"{time_period}", color=0x3DFFBE)

        rank = 1

        for data in response["toptracks"]["track"]:
            artist_lower = data["artist"]["name"].lower()
            artist_nospace = artist_lower.replace(" ", "")
            if artist_nospace == artist and rank <= 10:
                song_name = data["name"]
                number = data["playcount"]
                tracks.add_field(name=f"{rank}. {number} plays", value=song_name, inline=False)
                rank += 1
            elif rank > 10:
                break

        await ctx.channel.send(embed=tracks)


def setup(client):
    client.add_cog(Lastfm(client))
