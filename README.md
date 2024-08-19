# 7 Days to Die Companion Bot - Documentation
##Overview
This script is a Discord bot designed to interact with a "7 Days to Die" game server. The bot provides various functionalities, including fetching game server stats such as the current day, the next Blood Moon day, and the list of online players. The bot is built using the discord.py library and communicates with the game server through API calls.

## Setup
### Environment Variables
The bot requires the following environment variables to be set in a .env file:

**DISCORD_TOKEN:** The token for your Discord bot.

**TOKEN_NAME:** The token name for accessing the 7 Days to Die server API.

**TOKEN_SECRET:** The token secret for accessing the 7 Days to Die server API.

## Dependencies
The following Python libraries are required:

- os: For accessing environment variables.

- discord: The main library for creating the Discord bot.

- requests: For making HTTP requests to the game server API.

- dotenv: For loading environment variables from a .env file.

## Bot Configuration

### Discord Bot Intents
```
intents = discord.Intents.default()
intents.message_content = True
```
The bot is configured with default intents, with explicit permission to read message content.

### Bot Client Initialization
```
client = discord.Client(intents=intents)
```
A Discord client is created with the specified intents.

## API Interaction
### Base URL
```
web_Url = 'http://ip-address:8081/api'
```
This is the URL you would normal use to login to the web portal, make sure the ip-address matches the server, the Web portal is enabled, and you are using the right port that is accessiable (may need to port more ports).

### Headers
The bot uses the following headers for API requests:
```
headers = {
    "X-SDTD-API-TOKENNAME": token_name,
    "X-SDTD-API-SECRET": token_value,
    "Content-Type": "application/json"
}
```
These headers include the API token name and secret for authentication.

## Helper Function
`find_value_in_json(json_data, target_key)`
This function recursively searches for a specific key in a nested JSON structure and returns its corresponding value.

## Bot Functions
[Functional]
`get_bloodmoon_day()`
Fetches the current day from the game server and calculates the number of days until the next Blood Moon. Blood Moons occur every 7 days.

`get_current_day()`
Fetches the current day in the game from the server.

[Work in Progress]
`get_player(value)`
Fetches player information from the game server. The value parameter determines what specific information is retrieved (e.g., player ID, name, platform ID, etc.). The function uses several helper functions to extract specific pieces of player data.

Options:
```
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
```
[Future]
`heal_all`
`teleport`
`kick`
`ban`
`say`

## Bot Events
`on_ready()`
This event is triggered when the bot successfully connects to Discord. It prints the number of guilds (servers) the bot is connected to.

`on_message(message)`
This event is triggered whenever a message is sent in a channel the bot has access to. The bot listens for specific commands and responds accordingly:

- `!bloodmoon` or `!bm:` Fetches and displays the next Blood Moon day.
- `!currentday` or `!cd:` Fetches and displays the current in-game day.
- `!viewonline` or `!vo:` Fetches and displays the names of online players.

Each command deletes the user's original message and any previous bot responses containing similar content to keep the channel clean.

## Running the Bot
The bot is started using:
```
client.run(discord_token)
```
This line initiates the bot using the Discord token specified in the environment variables.
