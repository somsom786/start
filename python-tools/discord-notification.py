import discord
from playsound import playsound

TOKEN = "YOUR_USER_TOKEN"
TRIGGER = ".n"
SOUND_FILE = "notification.mp3"

GUILD_ID = 1111222233334444       # Only track this server
CHANNEL_ID = 5555666677778888     # Only track this channel
ALLOWED_USER_IDS = [999900001111] # Only react to specific users

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user} ({client.user.id})")

@client.event
async def on_message(message):
    if message.author.bot:
        return

    if message.guild and message.guild.id != GUILD_ID:
        return

    if message.channel.id != CHANNEL_ID:
        return

    if message.author.id not in ALLOWED_USER_IDS:
        return

    if TRIGGER in message.content.lower():
        print(f"Trigger from {message.author} in {message.guild.name}/{message.channel.name}")
        playsound(SOUND_FILE)

client.run(TOKEN, bot=False)
