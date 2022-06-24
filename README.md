# Aternos-Server-Discord-Bot
A bot that can startup your aternos minecraft server through discord.

## How To Use
All you need to do is download the repository and edit the config.json file.
- **prefix** - the prefix to put at the start of commands, make sure it doesn't clash with any other bots already in your server
- **aternos.username** - your username on aternos
- **aternos.password** - your password for aternos. **Your password will only be sent to aternos.**
- **server_address** - your aternos server's address
- **bot_token** - your discord bot's token

## Commands
- **awake** - the bot will reply to this message so you know it is online
- **server** - The bot sends the server address
- **status** - the bot sends the current server status (online/offline/loading)
- **online** - the bot sends how many players are currently online
- **start** - starts the server if it is offline, the bot will reply to your message once it is online
- **stop** - stops the server if no one is online
