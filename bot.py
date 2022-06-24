import discord
from python_aternos import Client
from mcstatus import JavaServer

import functools
import typing
import asyncio
import time

import json
with open('config.json', 'r') as f:
  config = json.load(f)


PREFIX = config["prefix"]
if PREFIX == "":
	raise Exception("No command prefix set in config.json")


# Connect to aternos
aternos = Client.from_credentials(config["aternos"]["username"], config["aternos"]["password"])
servs = aternos.list_servers()
serv = None
# Find server name
for i in servs:
	if i.address == config["server_address"]:
		serv = i
		break
# Throw an error if the server was not found
if serv == None:
	raise Exception("No server with address " + config["server_address"] + " found")
print("Connected to aternos. Found server " + serv.address)


# Connect to the minecraft server
mc_server = JavaServer(serv.address, serv.port)
print("Connected to minecraft server")


# Connect to discord
client = discord.Client()
@client.event
async def on_ready():
    print("Connected to discord as user " + client.user.name)
    await client.change_presence(activity=discord.Game(name=(PREFIX+" help")))


def is_command(command, message):
    return message.content.startswith(PREFIX + command)

# Returns the current status of the server. You need to go through aternos each time to get the updated status.
def get_server_status():
    return aternos.list_servers()[0].status


def to_thread(func: typing.Callable) -> typing.Coroutine:
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        return await asyncio.to_thread(func, *args, **kwargs)
    return wrapper
# Hangs the program without the connection to discord timing out
@to_thread
def wait_until_online():
    while get_server_status() != "online":
        time.sleep(3)


@client.event
async def on_message(message):
    # Ignore messages the bot itself sent
    if message.author == client.user:
        return

    message.content = message.content.lower()

    # Awake - respond to the user so they know the bot is online
    if is_command("awake", message):
        await message.channel.send("I'm online")

    # server - respond with the server details the user needs to connect
    elif is_command("server", message):
        await message.channel.send("Address: " + serv.address)

    # status - respond to the user with the current status of the server
    elif is_command("status", message):
        await message.channel.send("The server is currently " + get_server_status())

    # help - respond with a list of commands
    elif is_command("help", message):
        # The message for this is stored in help.txt
        await message.channel.send(open("misc/help.txt", "r").read())

    # online - responds with the number of players online
    elif is_command("online", message):
        status = get_server_status()
        if status == "online":
            await message.channel.send("There is currently " + str(mc_server.status().players.online) + " players online")
        else:
            await message.channel.send("No players online as the server is currently: " + status)

    # start - if the server is asleep, start the server
    elif is_command("start", message):
        if get_server_status() == "offline":
            serv.start()
            await message.channel.send("Starting server...")
            await wait_until_online()
            await message.reply("Server is now online")

        else:
            await message.channel.send("The server is already awake. Server status: " + get_server_status())

    # stop - stops the server if no one is online or if I sent the message
    elif is_command("stop", message):
        online = mc_server.status().players.online

        if get_server_status() == "online":
            if mc_server.status().players.online == 0:
                serv.stop()
                await message.channel.send("Shutting down server...")
            # There are players online, so do not shut down the server
            else:
                await message.channel.send("The server was not shut down as there is still " + str(online) + " players online")
        # The server is not online
        else:
            await message.channel.send("The server is not online")

client.run(config["bot_token"])
