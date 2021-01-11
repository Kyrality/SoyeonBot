import discord
import json
from discord.ext import commands
import os
from keys import client_token


def get_prefix(client, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]


intent = discord.Intents(messages=True, members=True, guilds=True)
client = commands.Bot(command_prefix=get_prefix, intents=intent)


@client.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = '^'

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)


@client.event
async def on_guild_remove(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)


@client.command()
async def load(ctx, extension):
    """Loads the selected cog. Format: ^load [extension]"""
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f'{extension} extension loaded.')


@client.command()
async def unload(ctx, extension):
    """Unloads the selected cog. Format: ^unload [extension]"""
    client.unload_extension(f'cogs.{extension}')
    await ctx.send(f'{extension} extension unloaded.')


@client.command()
async def reload(ctx, extension):
    """Reloads the selected cog. Format: ^reload [extension]"""
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f'{extension} extension reloaded.')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


@client.event
async def on_message(message):
    if message.content == "Hello":
        await message.channel.send("Hello!")
    await client.process_commands(message)


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please pass in all required arguments.")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("Invalid command used.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("You are not authorised to use this command")

client.run(client_token)
