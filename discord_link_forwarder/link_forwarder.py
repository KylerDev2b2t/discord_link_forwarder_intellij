import discord
import re
import requests

# ============ SETUP ============
BOT_TOKEN = 'YOUR_BOT_TOKEN_HERE'
SOURCE_CHANNEL_ID = YOUR_SOURCE_CHANNEL_ID_HERE  # e.g. 123456789012345678 (int, no quotes)
WEBHOOK_URL = "YOUR_WEBHOOK_URL_HERE"
# ===============================

url_pattern = re.compile(r'https?://\S+')

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"✅ Bot logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author.bot:
        return
    if message.channel.id != SOURCE_CHANNEL_ID:
        return

    urls = url_pattern.findall(message.content)
    if urls:
        for url in urls:
            payload = {
                "content": f"🔗 **{message.author}** posted a link:\n{url}"
            }
            try:
                requests.post(WEBHOOK_URL, json=payload)
                print(f"✅ Forwarded: {url}")
            except Exception as e:
                print(f"❌ Failed to forward: {e}")

client.run(BOT_TOKEN)
