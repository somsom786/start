"""
feat: upgrade to V3 with multi-keyword triggers, role-based username color, avatar display, and improved UI
- Added support for multiple trigger keywords
- Fetched and displayed user avatar in popup
- Styled popup to resemble Discord UI (dark mode, rounded corners)
- Username now adopts user's top role color
- Improved message rendering with truncation and layout
- Added logging to file (trigger_log.txt)
- Included fade-in animation and auto-destroy
- Added auto-reconnect logic for stability
"""

import discord
import pygame
import tkinter as tk
import ctypes
import webbrowser
import requests
import io
from PIL import Image, ImageTk, ImageDraw
from datetime import datetime
import asyncio
import threading

# --- CONFIG ---
TOKEN = "YOUR_DISCORD_TOKEN"
TRIGGERS = [".n", "!alert", "hello"] #you can add more keywords here
SOUND_FILE = r"YOUR_DISCORD_SOUND_FILE/PATH" #you can download some here: https://pixabay.com/sound-effects/search/ping/
GUILD_ID = "THE_GUILD_ID" #you right click the server you are in and copy the server ID
CHANNEL_ID = "THE_CHANNEL_ID" #same as guild id

# --- INIT ---
client = discord.Client()
pygame.mixer.init()
popup_root = tk.Tk()
popup_root.configure(bg="#2b2d31")
popup_root.withdraw()

def play_notification():
    def do_play():
        try:
            pygame.mixer.music.stop()
            pygame.mixer.music.load(SOUND_FILE)
            pygame.mixer.music.play()
        except Exception as e:
            print(f"[ERROR] Failed to play sound: {e}")
    popup_root.after(0, do_play)

def fetch_avatar(user):
    try:
        url = user.avatar.url if user.avatar else user.default_avatar.url
        r = requests.get(url)
        img_data = r.content
        image = Image.open(io.BytesIO(img_data)).resize((40, 40)).convert("RGBA")

        # Create circular mask
        mask = Image.new('L', (40, 40), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, 40, 40), fill=255)
        image.putalpha(mask)

        return ImageTk.PhotoImage(image)
    except:
        return None

def log_trigger(author, content):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("trigger_log.txt", "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {author}: {content}\n")

def show_custom_popup(author, content, avatar_image, url, name_color):
    def create_popup():
        win = tk.Toplevel(popup_root)
        win.overrideredirect(True)
        win.configure(bg="#2b2d31")
        win.attributes('-topmost', True)
        win.attributes('-alpha', 0.0)

        screen_width = win.winfo_screenwidth()
        screen_height = win.winfo_screenheight()
        width, height = 350, 110
        x = screen_width - width - 10
        y = screen_height - height - 50
        win.geometry(f"{width}x{height}+{x}+{y}")

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

        frame = tk.Frame(win, bg="#2b2d31")
        frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Avatar
        avatar_label = tk.Label(frame, image=avatar_image, bg="#2b2d31")
        avatar_label.image = avatar_image
        avatar_label.grid(row=0, column=0, rowspan=2, sticky="n")

        # Username + time
        name_time = tk.Frame(frame, bg="#2b2d31")
        name_time.grid(row=0, column=1, sticky="w")

        name_label = tk.Label(name_time, text=author.name, font=("Segoe UI", 10, "bold"), fg=name_color, bg="#2b2d31")
        name_label.pack(side="left")

        timestamp = datetime.now().strftime("%H:%M")
        time_label = tk.Label(name_time, text=timestamp, font=("Segoe UI", 9), fg="#999", bg="#2b2d31")
        time_label.pack(side="left", padx=(6, 0))

        # Message text
        text_label = tk.Label(frame, text=content, font=("Segoe UI", 10), fg="white", bg="#2b2d31",
                              wraplength=270, justify="left", anchor="nw")
        text_label.grid(row=1, column=1, sticky="w")

        def on_click(event):
            webbrowser.open(url)
            win.destroy()

        frame.bind("<Button-1>", on_click)
        text_label.bind("<Button-1>", on_click)

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
        content = message.content.strip().replace('\n', ' ')
        if any(trigger in content.lower() for trigger in TRIGGERS):
            print(f"🚨 Trigger by {message.author}: {content}")
            play_notification()
            log_trigger(message.author, content)

            msg_url = f"https://discord.com/channels/{GUILD_ID}/{CHANNEL_ID}/{message.id}"
            avatar = fetch_avatar(message.author)
            top_role_color = message.author.top_role.color.to_rgb()
            name_color = '#{:02x}{:02x}{:02x}'.format(*top_role_color) if top_role_color != (0, 0, 0) else "#ffffff"
            show_custom_popup(message.author, content, avatar, msg_url, name_color)

# --- Reconnect logic ---
async def run_bot():
    while True:
        try:
            await client.start(TOKEN)
        except Exception as e:
            print(f"[DISCORD ERROR] {e}")
            await asyncio.sleep(5)

def start_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run_bot())

threading.Thread(target=start_bot, daemon=True).start()
popup_root.mainloop()