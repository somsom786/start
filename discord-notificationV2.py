import discord
import pygame
import tkinter as tk
import ctypes
import webbrowser
from datetime import datetime
import asyncio
import threading

# --- CONFIG ---
TOKEN = "YOUR_DISCORD_TOKEN"
TRIGGER = "WHATEVER_MESSAGE_YOU_WANT_TO_TRIGGER"
SOUND_FILE = r"YOUR_DISCORD_SOUND_FILE/PATH" #you can download some here: https://pixabay.com/sound-effects/search/ping/
GUILD_ID = "THE_GUILD_ID" #you right click the server you are in and copy the server ID
CHANNEL_ID = "THE_CHANNEL_ID" #same as guild id

# --- INIT DISCORD CLIENT (No intents!) ---
client = discord.Client()
pygame.mixer.init()

# --- INIT TK ---
popup_root = tk.Tk()
popup_root.withdraw()

def play_notification():
    try:
        pygame.mixer.music.stop()
        pygame.mixer.music.load(SOUND_FILE)
        pygame.mixer.music.play()
    except Exception as e:
        print(f"[ERROR] Failed to play sound: {e}")

def show_custom_popup(title, message_text, url):
    def create_popup():
        win = tk.Toplevel(popup_root)
        win.title(title)
        win.overrideredirect(True)
        win.attributes('-topmost', True)
        win.attributes('-alpha', 0.0)

        # Bottom-right position
        screen_width = win.winfo_screenwidth()
        screen_height = win.winfo_screenheight()
        width, height = 320, 100
        x = screen_width - width - 10
        y = screen_height - height - 50
        win.geometry(f"{width}x{height}+{x}+{y}")

        # Rounded corners (Windows 11+)
        hwnd = ctypes.windll.user32.GetParent(win.winfo_id())
        try:
            DWMWA_WINDOW_CORNER_PREFERENCE = 33
            DWMWCP_ROUND = 2
            ctypes.windll.dwmapi.DwmSetWindowAttribute(
                hwnd,
                DWMWA_WINDOW_CORNER_PREFERENCE,
                ctypes.byref(ctypes.c_int(DWMWCP_ROUND)),
                ctypes.sizeof(ctypes.c_int())
            )
        except:
            pass

        frame = tk.Frame(win, bg="#222222", bd=0)
        frame.pack(fill='both', expand=True)

        label = tk.Label(
            frame,
            text=message_text,
            fg='white',
            bg='#222222',
            font=('Segoe UI', 11),
            wraplength=300,
            justify='left',
            anchor='w'
        )
        label.pack(expand=True, padx=10, pady=10)

        def on_click(event):
            webbrowser.open(url)
            win.destroy()

        label.bind("<Button-1>", on_click)
        frame.bind("<Button-1>", on_click)

        def fade(alpha=0.0):
            alpha = round(alpha + 0.05, 2)
            if alpha <= 1.0:
                win.attributes('-alpha', alpha)
                win.after(30, fade, alpha)
            else:
                win.attributes('-alpha', 1.0)

        fade()
        win.after(6000, win.destroy)

    popup_root.after(0, create_popup)

@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user} (ID: {client.user.id})")

@client.event
async def on_message(message):
    if message.guild and message.guild.id == GUILD_ID and message.channel.id == CHANNEL_ID:
        if TRIGGER in message.content.lower():
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{timestamp}] 🔔 Trigger by {message.author}: {message.content}")

            play_notification()

            # Truncate message for pop-up
            clean_message = message.content.strip().replace('\n', ' ')
            max_length = 100
            if len(clean_message) > max_length:
                clean_message = clean_message[:max_length - 3] + "..."

            popup_text = f"{message.author}: {clean_message}"
            message_url = f"https://discord.com/channels/{GUILD_ID}/{CHANNEL_ID}/{message.id}"

            show_custom_popup("🚨 Discord Trigger", popup_text, message_url)

# --- RUN DISCORD BOT IN BACKGROUND THREAD ---
async def run_bot():
    await client.start(TOKEN)

def start_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run_bot())

threading.Thread(target=start_bot, daemon=True).start()

# --- MAIN TK LOOP ---
popup_root.mainloop()
