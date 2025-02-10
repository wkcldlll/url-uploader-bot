import os
import aiohttp
from pyrogram import Client, filters

# Load environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")

app = Client("url_uploader", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("Hello! Send me a direct download link, and I'll fetch the file for you.")

@app.on_message(filters.text & filters.private)
async def download_and_upload(client, message):
    url = message.text.strip()

    if not url.startswith("http"):
        await message.reply_text("Please send a valid direct download link.")
        return

    try:
        filename = url.split("/")[-1]  
        await message.reply_text("Downloading... Please wait.")

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    await message.reply_text("Failed to download the file.")
                    return
                with open(filename, "wb") as file:
                    file.write(await response.read())

        await message.reply_document(filename)
        os.remove(filename)  

    except Exception as e:
        await message.reply_text(f"Error: {str(e)}")

app.run()
