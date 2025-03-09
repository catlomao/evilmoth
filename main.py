import discord
import pytesseract
from PIL import Image
import io
import requests
import re

# Set up the intents
intents = discord.Intents.default()
intents.message_content = True  # Allow the bot to read message content


client = discord.Client(intents=intents)


target_words = ["moth", "evil moth"]

def contains_target_words(text):
    return any(word.lower() in text.lower() for word in target_words)
def extract_text_from_image(image_url):
    try:
        response = requests.get(image_url)
        image = Image.open(io.BytesIO(response.content))
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        print(f"Error in OCR: {e}")
        return ""
def is_image_url(url):
    image_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp']
    return any(url.lower().endswith(ext) for ext in image_extensions)
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if contains_target_words(message.content):
        emoji = discord.PartialEmoji(name="<emoji-name>", id=<emoji id>)  # this reacts to messages
        await message.add_reaction(emoji)
    for word in message.content.split():
        if is_image_url(word):
            image_text = extract_text_from_image(word)         
            if contains_target_words(image_text):
                emoji = discord.PartialEmoji(name="<emoji-name>", id=<emoji id>)  # this reacts to embeded-image-url (idk if it works) (OCR)
                await message.add_reaction(emoji)
                return
    if message.attachments:
        for attachment in message.attachments:
            if attachment.filename.lower().endswith(('png', 'jpg', 'jpeg', 'gif')):
                # Extract text from the image
                image_text = extract_text_from_image(attachment.url)
                
                if contains_target_words(image_text):
                    emoji = discord.PartialEmoji(name="moth_emoji", id=1348411577833095251)  # this reacts to images-file (OCR)
                    await message.add_reaction(emoji)
                    return

# Run the bot with your token
client.run('TOKEN-HERE')
