# required libraries for this bot to work
import discord
import os
import dotenv
import textblob
import tinydb
import tinydb.operations
import random
import math

# load .env
dotenv.load_dotenv()
token = str(os.getenv("TOKEN"))

# create bot and register database, the extra jargon after 'db.json' is to prettify the json file
db = tinydb.TinyDB('db.json', sort_keys=True, indent=4, separators=(',', ': '))
users = tinydb.Query()
bot = discord.Bot(intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("read E")

@bot.event
async def on_message(message):
    blurb = textblob.TextBlob(message.content)
    
    # check to make sure the message sender isn't this bot
    if message.author.id != 1170490245431693414:
        # if they aren't in the database, register them in the database
        if not db.contains(users.name == message.author.name):
            db.insert({"name": message.author.name, "reputation": 100})
        
        # why did this take me so fucking long AAAAAAAAAAAAAAAA
        for item in db.all():
            if item.get("name") == message.author.name:
                db.update({"reputation": (item.get("reputation") + round(blurb.sentiment.polarity * 10))}, users.name == item.get("name"))
                print(item.get("reputation") + round(blurb.sentiment.polarity * 10))

@bot.command(description="Check reputation of you and other people")
async def reputation(ctx, user: discord.Option(discord.SlashCommandOptionType.user)):
    for item in db.all():
        if item.get("name") == user.name:
            local_reputation = item.get("reputation")
            embed = discord.Embed(title=item.get("name"),
                                  description="Reputation: " + str(local_reputation),
                                  color=discord.Color.random(),
                                  )
            
            await ctx.respond(embed = embed)  

@bot.command(description="Reduces others' rep if yours >50, max -10; costs +1 from yours if used correctly")
async def removereputation(ctx, user: discord.Option(discord.SlashCommandOptionType.user), amount: discord.Option(int)):
    for item in db.all():
        if item.get("name") == ctx.author.name:
            if not item.get("reputation") > 50 or abs(amount) > 10:
                if item.get("reputation") < 0:
                    ctx.respond("little baby shithead")
                    db.update({"reputation": item.get("reputation") - round(abs(amount) * 2)}, users.name == ctx.author.name)
                elif item.get("reputation") >= 0:
                    ctx.respond("Your reputation is too low to use this command! Taking " + str((abs(amount) + 3)) + " reputation.")
                    db.update({"reputation": item.get("reputation") - (abs(amount) + 3)}, users.name == ctx.author.name)
                elif abs(amount) > 10:
                    ctx.respond("You went over the 10 maximum! Taking " + str((abs(amount) + 2)) + " reputation." )
                    db.update({"reputation": item.get("reputation") - (abs(amount) + 2)}, users.name == ctx.author.name)
            else:
                for item in db.all():
                    if item.get("name") == user.name:
                        db.update({"reputation": item.get("reputation") - amount}, users.name == item.get("name"))
                        db.update({"reputation": item.get("reputation") - (amount + 1)}, users.name == ctx.author.name)

@bot.command(description="Increases others' rep if yours >50, max +10; deducts same plus one from yours if used right.")
async def addreputation(ctx, user: discord.Option(discord.SlashCommandOptionType.user), amount: discord.Option(int)):
    for item in db.all():
        if item.get("name") == ctx.author.name:
            if not item.get("reputation") > 50 or abs(amount) > 10:
                if item.get("reputation") < 0:
                    ctx.respond("little baby shithead")
                    db.update({"reputation": item.get("reputation") - round(abs(amount) * 2)}, users.name == ctx.author.name)
                elif item.get("reputation") >= 0:
                    ctx.respond("Your reputation is too low to use this command! Taking " + str((abs(amount) + 3)) + " reputation.")
                    db.update({"reputation": item.get("reputation") - (abs(amount) + 3)}, users.name == ctx.author.name)
                elif abs(amount) > 10:
                    ctx.respond("You went over the 10 maximum! Taking " + str((abs(amount) + 2)) + " reputation." )
                    db.update({"reputation": item.get("reputation") - (abs(amount) + 2)}, users.name == ctx.author.name)
            else:
                for item in db.all():
                    if item.get("name") == user.name:
                        db.update({"reputation": item.get("reputation") + amount}, users.name == item.get("name"))
                        db.update({"reputation": item.get("reputation") - (amount + 1)}, users.name == ctx.author.name)

bot.run(token)