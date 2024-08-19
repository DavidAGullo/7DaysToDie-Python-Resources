# Discord bot.py for 7 Days to Die Companion Bot
import os
import discord
import requests
from dotenv import load_dotenv

load_dotenv()

# Discord Bot Tokens
discord_token = os.getenv('DISCORD_TOKEN') # Discord Bot Token

# Define Discord Bot Intents
intents = discord.Intents.default()
intents.message_content = True

# 7 Days Token Values
token_name = os.getenv('TOKEN_NAME') # X-SDTD-API-TOKENNAME -- Actual Key Name for Token Name
token_value = os.getenv('TOKEN_SECRET') # X-SDTD-API-TOKENSECRET -- Actual Key Name for Secret
web_Url = 'http://50.20.249.117:27026/api' #Should be the URL for the portal but instead of the app that we are accessing we will use 'api'

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


def get_player(value):
    url = web_Url + '/Player'
    headers = {
        "X-SDTD-API-TOKENNAME": token_name,
        "X-SDTD-API-SECRET": token_value,
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print('Error!')
        return None  # Handle Error

    print('Success!')
    data = response.json()

    players = data.get('data', {}).get('players', [])

    if not players:
        return "No players found or an error occurred."

    # Helper functions to extract data
    def get_player_id():
        return [player['entityId'] for player in players]

    def get_player_name():
        return [player['name'] for player in players]

    def get_platform_id():
        return '\n'.join([
                             f"Platform ID: {player['platformId']['combinedString']} | EOS ID: {player['crossplatformId']['combinedString']}"
                             for player in players])

    def get_ip():
        return [player['ip'] for player in players]

    def get_ping():
        return [player['ping'] for player in players]

    def get_health():
        return [player['health'] for player in players]

    def get_stamina():
        return [player['stamina'] for player in players]

    def get_score():
        return [player['score'] for player in players]

    def get_deaths():
        return [player['deaths'] for player in players]

    def get_kill_zombie():
        return [player['kills']['zombies'] for player in players]

    def get_kill_player():
        return [player['kills']['players'] for player in players]

    def get_is_banned():
        return [player['banned']['banActive'] for player in players]

    def get_ban_reason():
        return [player['banned']['reason'] for player in players]

    def get_ban_expire():
        return [player['banned']['until'] for player in players]

    def get_all_info():
        return '\n'.join([
            f"Player ID: {player['entityId']}\n"
            f"Name: {player['name']}\n"
            f"Platform ID: {player['platformId']['combinedString']}\n"
            f"EOS ID: {player['crossplatformId']['combinedString']}\n"
            f"IP: {player['ip']}\n"
            f"Ping: {player['ping']}\n"
            f"Health: {player['health']}\n"
            f"Stamina: {player['stamina']}\n"
            f"Score: {player['score']}\n"
            f"Deaths: {player['deaths']}\n"
            f"Zombie Kills: {player['kills']['zombies']}\n"
            f"Player Kills: {player['kills']['players']}\n"
            f"Banned: {player['banned']['banActive']}\n"
            f"Ban Reason: {player['banned']['reason']}\n"
            f"Ban Expire: {player['banned']['until']}\n"
            for player in players
        ])

    def get_all_no_id():
        return '\n'.join([
            f"Name: {player['name']}\n"
            f"Platform ID: {player['platformId']['combinedString']}\n"
            f"EOS ID: {player['crossplatformId']['combinedString']}\n"
            f"IP: {player['ip']}\n"
            f"Ping: {player['ping']}\n"
            f"Health: {player['health']}\n"
            f"Stamina: {player['stamina']}\n"
            f"Score: {player['score']}\n"
            f"Deaths: {player['deaths']}\n"
            f"Zombie Kills: {player['kills']['zombies']}\n"
            f"Player Kills: {player['kills']['players']}\n"
            f"Banned: {player['banned']['banActive']}\n"
            f"Ban Reason: {player['banned']['reason']}\n"
            f"Ban Expire: {player['banned']['until']}\n"
            for player in players
        ])

    # Dictionary to handle different value cases (simulating a switch-case)
    switch = {
        "id": get_player_id,
        "name": get_player_name,
        "platform_id": get_platform_id,
        "ip": get_ip,
        "ping": get_ping,
        "health": get_health,
        "stamina": get_stamina,
        "score": get_score,
        "death": get_deaths,
        "kill_zombie": get_kill_zombie,
        "kill_player": get_kill_player,
        "isBanned": get_is_banned,
        "banReason": get_ban_reason,
        "banExpire": get_ban_expire,
        "all": get_all_info,
        "all_no_id": get_all_no_id,
        "t": lambda: "Test"  # Test case
    }

    # Call the appropriate function from the switch dictionary
    result = switch.get(value, lambda: None)()

    return result

############################################################################################################################################################################################################
############################################################################################################################################################################################################
############################################################################################################################################################################################################

# Event Listener for Bot OFFLINE/ONLINE STATUS
@client.event
async def on_ready():
    print('We have now Connected!')
    guild_count = 0

    for guild in client.guilds:
        print(f'Guild Name: {guild.name}')
        print(f'Guild ID: {guild.id}')
        guild_count += 1
    # Print out the number of guilds the bot is in
    print(f'7 Days to Die Companion Bot is in {guild_count} guilds.')

############################################################################################################################################################################################################
############################################################################################################################################################################################################

# Event Listener for Bot Messages
@client.event
async def on_message(message):
    msg = ''
    bloodmoon_day = get_bloodmoon_day()
    cur_day = get_current_day()
    if message.author == client.user:
        return

### Bot Commands [via Event Listener]
    # !bloodmoon or !bm - Get the next Blood Moon Day
    if message.content.startswith('!bloodmoon') or message.content.startswith('!bm'):
        msg = '[CURRENT DAY: ' + str(cur_day) + '] - The next Blood Moon is on Day: ' + str(bloodmoon_day)
        await message.delete()

        def is_string(m):
            return "the next blood moon is on day:" in m.content.lower()

        deleted = await message.channel.purge(limit=500, check=is_string)
        await message.channel.send(msg)
    # !currentday or !cd - Get the current day
    elif message.content.startswith('!currentday') or message.content.startswith('!cd'):
        msg = 'The current day is: ' + str(cur_day)
        await message.delete()

        def is_string(m):
            return "the current day is:" in m.content.lower()

        deleted = await message.channel.purge(limit=500, check=is_string)
        await message.channel.send(msg)
    # !viewonline or !vo - Get the number of players online and their names
    elif message.content.startswith('!viewonline') or message.content.startswith('!vo'):
        await message.delete()
        msg = get_player("name")
        if msg:  # Check if msg is not None or empty
            await message.channel.send(msg)
        else:
            await message.channel.send("No online players found or an error occurred.")

############################################################################################################################################################################################################
############################################################################################################################################################################################################

client.run(discord_token)

