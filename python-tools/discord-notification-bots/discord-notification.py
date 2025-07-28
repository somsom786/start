import discord
import pygame

# Your settings
TOKEN = "YOUR_DISCORD_TOKEN"
TRIGGER = "WHATEVER_MESSAGE_YOU_WANT_TO_TRIGGER"
SOUND_FILE = r"YOUR_DISCORD_SOUND_FILE/PATH" #you can download some here: https://pixabay.com/sound-effects/search/ping/
GUILD_ID = "THE_GUILD_ID" #you right click the server you are in and copy the server ID
CHANNEL_ID = "THE_CHANNEL_ID" #same as guild id

# Initialize Discord client (no intents)
client = discord.Client()

# Initialize Pygame mixer, tried to use playsound but it didn't work well and this was a more reliable library and it worked :)
pygame.mixer.init()

def play_notification():
    try:
        pygame.mixer.music.stop()
        pygame.mixer.music.load(SOUND_FILE)
        pygame.mixer.music.play()
    except Exception as e:
        print(f"[ERROR] Failed to play sound: {e}")

@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user} (ID: {client.user.id})")

@client.event
async def on_message(message):
    # GUILD_ID and CHANNEL_ID filtering
    if message.guild and message.guild.id == GUILD_ID and message.channel.id == CHANNEL_ID:
        if TRIGGER in message.content.lower():
            print(f"[ALERT] Trigger by {message.author}: {message.content}")
            play_notification()

client.run(TOKEN)