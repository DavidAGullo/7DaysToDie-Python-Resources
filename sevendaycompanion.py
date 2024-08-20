# Discord bot.py for 7 Days to Die Companion Bot
import os
import discord
import requests
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()

# Discord Bot Tokens
discord_token = os.getenv('DISCORD_TOKEN') # Discord Bot Token

# Define Discord Bot Intents
intents = discord.Intents.default()
intents.message_content = True

# Create the bot with all intents
bot = commands.Bot(command_prefix='!', intents=intents)

# 7 Days Token Values
token_name = os.getenv('TOKEN_NAME') # X-SDTD-API-TOKENNAME -- Actual Key Name for Token Name
token_value = os.getenv('TOKEN_SECRET') # X-SDTD-API-TOKENSECRET -- Actual Key Name for Secret
web_Url = os.getenv('WEB_URL') #Should be the URL for the portal but instead of the app that we are accessing we will use 'api'

# Create a new bot
client = discord.Client(intents=intents)

############################################################################################################################################################################################################
############################################################################################################################################################################################################
## Required Functions for things to work don't touch this
############################################################################################################################################################################################################
## find in JSON data
############################################################################################################################################################################################################
def find_value_in_json(json_data, target_key):
    if isinstance(json_data, dict):
        for key, value in json_data.items():
            if key == target_key:
                return value
            elif isinstance(value, (dict, list)):
                result = find_value_in_json(value, target_key)
                if result is not None:
                    return result
    elif isinstance(json_data, list):
        for item in json_data:
            result = find_value_in_json(item, target_key)
            if result is not None:
                return result
    return None
############################################################################################################################################################################################################
############################################################################################################################################################################################################

############################################################################################################################################################################################################
############################################################################################################################################################################################################
# Functions for 7 Days to Die Companion Bot

### Function to get the Blood Moon Day
def get_bloodmoon_day():
    url = web_Url + '/serverstats'
    headers = {
        "X-SDTD-API-TOKENNAME": token_name,
        "X-SDTD-API-SECRET": token_value,
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print('Success!')
        data = response.json()
        current_day = data['data']['gameTime']['days']
        bloodmoon_day = 7 - (current_day % 7)
        return bloodmoon_day
    else:
        print('Error!')
        return None # Handle Error
def get_current_day():
    url = web_Url + '/serverstats'
    headers = {
        "X-SDTD-API-TOKENNAME": token_name,
        "X-SDTD-API-SECRET": token_value,
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print('Success!')
        data = response.json()
        current_day = data['data']['gameTime']['days']
        return current_day
    else:
        print('Error!')
        return None # Handle Error


def get_player(user, value):
    url = web_Url + '/Player'
    headers = {
        "X-SDTD-API-TOKENNAME": token_name,
        "X-SDTD-API-SECRET": token_value,
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print('Success!')
        player_data = { }
        data = response.json()
        player_data_count = len(data['data']['players'])
        print(player_data_count)
        for player_ind in data['data']['players']:
            #For each player in the list of players (represented by a integer), create an object for each player
            player_data[player_ind] = {
                "id": data['data']['players'][player_ind]['entityId'],
                "name": data['data']['players'][player_ind]['name'],
                "platformId": data['data']['players'][player_ind]['platformId']['combinedString'],
                "crossplatformId": data['data']['players'][player_ind]['crossplatformId']['combinedString'],
                "ip": data['data']['players'][player_ind]['ip'],
                "ping": data['data']['players'][player_ind]['ping'],
                "position_x": data['data']['players'][player_ind]['position']['x'],
                "position_y": data['data']['players'][player_ind]['position']['y'],
                "position_z": data['data']['players'][player_ind]['position']['z'],
                #"level": data['data']['players'][player_ind]['level'], #Not available in the API yet?
                "health": data['data']['players'][player_ind]['health'],
                "stamina": data['data']['players'][player_ind]['stamina'],
                "score": data['data']['players'][player_ind]['score'],
                "deaths": data['data']['players'][player_ind]['deaths'],
                "zombies_kills": data['data']['players'][player_ind]['kills']['zombies'],
                "players_kills": data['data']['players'][player_ind]['kills']['players'],
                "banned": data['data']['players'][player_ind]['banned']['banActive'],
                "banned_reason": data['data']['players'][player_ind]['banned']['reason'],
                "banned_until": data['data']['players'][player_ind]['banned']['until'],
            }
        if player_data[0] != None:
            #If there are players online, this can return data
            #If requesting players name, return name of player
            if value == 'name':
                return_msg = ''
                for x in player_data:
                    if player_data[x]['name'] == user:
                        return_msg = player_data[x]['name'] + ' is online.'
                return return_msg
            elif value == 'ping':
                return_msg = ''
                for x in player_data:
                    if player_data[x]['name'] == user:
                        return_msg = player_data[x]['name'] + ' has a ping of ' + str(player_data[x]['ping']) + 'ms.'
                return return_msg
        else:
            return "Player may be offline right now."
    else:
        print('Error!')
        return None # Handle

############################################################################################################################################################################################################
############################################################################################################################################################################################################
# Event Listener for Bot OFFLINE/ONLINE STATUS
@bot.event
async def on_ready():
    print('We have now Connected!')
    guild_count = 0

    for guild in bot.guilds:
        print(f'Guild Name: {guild.name}')
        print(f'Guild ID: {guild.id}')
        guild_count += 1
    # Print out the number of guilds the bot is in
    print(f'7 Days to Die Companion Bot is in {guild_count} guilds.')

############################################################################################################################################################################################################
# Event Listener for Bot Messages
@bot.event
async def on_message(message):
    msg = ''
    bloodmoon_day = get_bloodmoon_day()
    cur_day = get_current_day()
    if message.author == bot.user:
        return

    ### Bot Commands [via Event Listener]
    # !bloodmoon or !bm - Get the next Blood Moon Day
    if message.content.startswith('?bloodmoon') or message.content.startswith('?bm'):
        msg = '[CURRENT DAY: ' + str(cur_day) + '] - The next Blood Moon is in: ' + str(bloodmoon_day) + ' days.'
        await message.delete()
        await message.channel.send(msg)
    # !currentday or !cd - Get the current day
    elif message.content.startswith('?currentday') or message.content.startswith('?cd'):
        msg = 'The current day is: ' + str(cur_day)
        await message.delete()
        await message.channel.send(msg)

############################################################################################################################################################################################################
# Bot Commands (Commands)
@bot.command()
async def helpme(ctx):
    embed = discord.Embed(
        title='7 Days to Die Companion Bot',
        description='List of Commands for the 7 Days to Die Companion Bot',
        color=discord.Color.blue()
    )
    embed.add_field(name='!help', value='Get the list of commands', inline=False)
    embed.add_field(name='!ping', value='Pong!', inline=False)
    embed.add_field(name='!bloodmoon or !bm', value='Get the next Blood Moon Day', inline=False)
    embed.add_field(name='!currentday or !cd', value='Get the current day', inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

@bot.command()
async def userstats(ctx, user: str, value: str):
    sel_player = get_player(user, value)
    await ctx.send(sel_player)

############################################################################################################################################################################################################
# Running the bot
bot.run(discord_token)

