# required libraries for this bot to work
import discord
import os
import dotenv
import textblob
import tinydb
import random

# load .env
dotenv.load_dotenv()
token = str(os.getenv("TOKEN"))

# create bot and register database
db = tinydb.TinyDB("./db.json")
names = tinydb.Query()
bot = discord.Bot(intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("read E")

@bot.event
async def on_message(message):
    blurb = textblob.TextBlob(message.content)

    # check to make sure the message sender isn't a bot
    if message.author.id != 1170490245431693414:
        # if they aren't in the database, register them in the database
        if not db.contains(message.author.name):
            db.insert({"name": message.author.name, "reputation": 50})

        # if db.search(where("name") == )

bot.run(token)