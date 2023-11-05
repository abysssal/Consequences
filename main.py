import discord
import os
import dotenv
import textblob
import tinydb

dotenv.load_dotenv()
token = str(os.getenv("TOKEN"))

db = tinydb.TinyDB("./db.json")
bot = discord.Bot(intents=discord.Intents().all())

@bot.event
async def on_message():
    blurb = textblob.TextBlob()

bot.run(token)