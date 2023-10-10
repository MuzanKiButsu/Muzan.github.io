import asyncio
import os
import shutil
from pyrogram import Client

# Set your Telegram bot token
BOT_TOKEN = "6337637965:AAFVJc09tFgqgeAszChm_XdjTYaQA24HFRw"

# Set your bot's server directory
SERVER_DIR = "/path/to/server/directory"

# Set your bot's desired format
DESIRED_FORMAT = "[SAW] Ep-01 NARUTO[720p][Dual].mkv"

# Initialize the bot
bot = Client("rename_bot", BOT_TOKEN)

# Set the bot's thumbnail
thumbnail = None

# Start the bot
bot.start()

# Define a function to download a file
async def download_file(file_id, file_name):
    file_path = os.path.join(SERVER_DIR, file_name)
    with open(file_path, "wb") as f:
        await bot.download_file(file_id, f)

# Define a function to rename a file
def rename_file(file_name):
    new_file_name = DESIRED_FORMAT.replace("[IAC]", "[SAW]")
    new_file_name = new_file_name.replace("[ANIME_NAME]", file_name.split("[")[1][:-1])
    new_file_name = new_file_name.replace("[EP_NUMBER]", file_name.split("[")[2].split("]")[0])
    os.rename(os.path.join(SERVER_DIR, file_name), os.path.join(SERVER_DIR, new_file_name))

# Define a function to send a file
async def send_file(file_name, chat_id):
    with open(os.path.join(SERVER_DIR, file_name), "rb") as f:
        await bot.send_document(chat_id, f, thumb=thumbnail)

# Define a function to handle the start command
@bot.on_message(filters.command("start"))
async def handle_start(client, message):
    global thumbnail
    await message.reply("Please send me a thumbnail for your renamed files.")
    thumbnail = await bot.wait_for_message(message.chat.id, filters.document)

# Define a function to handle messages containing files
@bot.on_message(filters.document)
async def handle_file(client, message):
    # Create a list to store the file names of the files to be renamed
    file_names = []

    # Download the file
    await download_file(message.document.file_id, message.document.file_name)

    # Add the file name to the list of files to be renamed
    file_names.append(message.document.file_name)

    # If the list of files to be renamed has 10 files, rename the files and send them back to the user
    if len(file_names) == 10:
        for file_name in file_names:
            rename_file(file_name)

        # Send the renamed files back to the user
        for file_name in file_names:
            await send_file(file_name, message.chat.id)

        # Clear the list of files to be renamed
        file_names.clear()

# Define a function to handle messages containing text
@bot.on_message(filters.text)
async def handle_text(client, message):
    # If the message is a command, handle it accordingly
    if message.text.startswith("/"):
        if message.text == "/start":
            await handle_start(client, message)
    # Otherwise, ignore the message
    else:
        pass

# Run the bot
async def main():
    await bot.idle()

if __name__ == "__main__":
    asyncio.run(main())
  
