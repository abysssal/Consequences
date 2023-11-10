# required libraries for this bot to work
import discord
import os
import dotenv
import textblob
import tinydb
import tinydb.operations
import random
import datetime
import math
from insults import getInsult, getKidFriendlyInsult, getMixedInsult

# load .env
dotenv.load_dotenv()
token = str(os.getenv("TOKEN"))

# create bot and register database, the extra jargon after 'db.json' is to prettify the json file
db = tinydb.TinyDB('db.json', sort_keys=True, indent=4, separators=(',', ': '))
users = tinydb.Query()
bot = discord.Bot(intents=discord.Intents.all())

# just to make sure the bot is not die
@bot.event
async def on_ready():
    print("read E")

# whenever a message gets sent, it triggers this event
@bot.event
async def on_message(message):
    blurb = textblob.TextBlob(message.content)

    # check to make sure the message sender isn't this bot
    if message.author.id != 1170490245431693414:
        # if they aren't in the database, register them in the database
        if not db.contains(users.name == message.author.name):
            db.insert({"name": message.author.name, "reputation": 100})

        # why did this take me so fucking long AAAAAAAAAAAAAAAA
        # anyways, this looks through the database to find the author, and adds the rounded polarity of their message * 10
        # if the reputation is below a certain amount, it'll delete the message and punish you
        for item in db.all():
            if item.get("name") == message.author.name:
                subtract = 0
                # punishments, consists of insults, kid friendly insults, timeouts, bans, and kicks
                # will remove reputation along with it
                if item.get("reputation") < -30 and item.get("reputation") > -61:
                    if random.randint(0, 1) == 0:
                        await message.reply(getKidFriendlyInsult())
                        await message.delete(reason="low repuation")

                if item.get("reputation") < -60 and item.get("reputation") > -101:
                    if random.randint(0, 1) == 0:
                        await message.reply(getMixedInsult())
                        await message.delete(reason="eat shit")
                
                if item.get("reputation") < -100 and item.get("reputation") > -201:
                     if random.randint(0, 1) == 0:
                        subtract += 1
                        await message.reply(getInsult())
                        await message.delete(reason="eat my ass")

                if item.get("reputation") < -200 and item.get("reputation") > -251:
                    if random.randint(0, 1) == 0:
                        if random.randint(0, 1) == 0:
                            subtract += 2
                            await message.author.timeout(until=datetime.datetime(0, 0, 0, 0, round(blurb.sentiment.polarity * 10)) + 5)
                            await message.reply(getInsult())
                            await message.delete(reason="eat my brown ass")
                        else:
                            subtract += 1
                            await message.reply(getInsult())
                            await message.delete(reason="eat my brown ass")

                if item.get("reputation") < -250 and item.get("reputation") > -401:
                    if random.randint(0, 1) == 0:
                        rando = random.randint(0, 2)
                        if rando == 0:
                            subtract += 2
                            await message.author.timeout(until=datetime.datetime(0, 0, 0, 0, round(blurb.sentiment.polarity * 10)) + 5)
                            await message.reply(getInsult())
                            await message.delete(reason="eat my brown ass")
                        elif rando == 1:
                            subtract += 3
                            await message.author.kick()
                            await message.reply(getInsult())
                            await message.delete(reason="eat my ass")
                        else:
                            subtract += 1
                            await message.reply(getInsult())
                            await message.delete(reason="eat my ass")

                if item.get("reputation") < -400 and item.get("reputation") > -1000:
                    if random.randint(0, 1) == 0:
                        rando = random.randint(0, 3)
                        if rando == 0:
                            subtract += 2
                            await message.author.timeout(until=datetime.datetime(0, 0, 0, 0, round(blurb.sentiment.polarity * 10)) + 5)
                            await message.reply(getInsult())
                            await message.delete(reason="eat my brown ass")
                        elif rando == 1:
                            subtract += 3
                            await message.author.kick()
                            await message.reply(getInsult())
                            await message.delete(reason="eat my ass")
                        elif rando == 2:
                            subtract += 4
                            await message.author.ban()
                            await message.reply(getInsult())
                            await message.delete(reason="eat my brown ass")
                        else:
                            subtract += 1
                            await message.reply(getInsult())
                            await message.delete(reason="eat my ass")

                if item.get("reputation") <= -1000:
                    subtract += 100
                    await message.author.ban()
                    await message.reply(getInsult())
                    await message.delete(reason="harassment")
                
                # update the reputation
                db.update({"reputation": (item.get("reputation") + round(blurb.sentiment.polarity * 10) + -subtract)}, users.name == item.get("name"))
                print(item.get("reputation") + round(blurb.sentiment.polarity * 10))


@bot.command(description="Check reputation of you and other people")
async def reputation(ctx, user: discord.Option(discord.SlashCommandOptionType.user)):
    for item in db.all():
        if item.get("name") == user.name:
            local_reputation = item.get("reputation")
            status = ""

            if local_reputation > 100:
                status = "good"

            if local_reputation < 100 and local_reputation > -1:
                status = "fine"

            if local_reputation < -30 and local_reputation > -61:
                status = "tolerable"

            if local_reputation < -60 and local_reputation > -101:
                status = "meh"

            if local_reputation < -101 and local_reputation > -201:
                status = "bad"

            if local_reputation < -200 and local_reputation > -251:
                status = "hate"

            if local_reputation < -250 and local_reputation > -401:
                status = "dispise"

            if local_reputation < -400 and local_reputation > -1001:
                status = "on my kill list"

            if local_reputation < -1000:
                status = "murdering"    

            embed = discord.Embed(title=item.get("name") + "\'s stats",description="Reputation: " + str(local_reputation) + "\nOpinion: " + status,color=discord.Color.random())
            
            await ctx.respond(embed = embed)  

@bot.command(description="Reduces others' rep if yours >50, max 10; costs +1 from yours if used correctly")
async def removereputation(ctx, user: discord.Option(discord.SlashCommandOptionType.user), amount: discord.Option(int)):
    for item in db.all():
        if item.get("name") == ctx.author.name:
            if not item.get("reputation") > 50 or abs(amount) > 10:
                if item.get("reputation") < 0:
                    await ctx.respond(getInsult())
                    db.update({"reputation": item.get("reputation") - round(abs(amount) * 2)}, users.name == ctx.author.name)
                elif item.get("reputation") >= 0:
                    await ctx.respond("Your reputation is too low to use this command! Taking " + str((abs(amount) + 3)) + " reputation.")
                    db.update({"reputation": item.get("reputation") - (abs(amount) + 3)}, users.name == ctx.author.name)
                elif abs(amount) > 10:
                    await ctx.respond("You went over the 10 maximum! Taking " + str(abs(amount) + 2) + " reputation." )
                    db.update({"reputation": item.get("reputation") - (abs(amount) + 2)}, users.name == ctx.author.name)
            else:
                for item in db.all():
                    if item.get("name") == user.name:
                        db.update({"reputation": item.get("reputation") - amount}, users.name == item.get("name"))
                        db.update({"reputation": item.get("reputation") - (amount + 1)}, users.name == ctx.author.name)
                        await ctx.respond("Removed " + str(abs(amount)) + " from " + user.name)

@bot.command(description="Reduces others' rep if yours >75, max 10; costs +1 from yours if used correctly")
async def removereputationsecretly(ctx, user: discord.Option(discord.SlashCommandOptionType.user), amount: discord.Option(int)):
    for item in db.all():
        if item.get("name") == ctx.author.name:
            if not item.get("reputation") > 75 or abs(amount) > 10:
                if item.get("reputation") < 0:
                    await ctx.respond(getInsult())
                    db.update({"reputation": item.get("reputation") - round(abs(amount) * 2)}, users.name == ctx.author.name)
                elif item.get("reputation") >= 0:
                    await ctx.respond("Your reputation is too low to use this command! Taking " + str((abs(amount) + 3)) + " reputation.")
                    db.update({"reputation": item.get("reputation") - (abs(amount) + 3)}, users.name == ctx.author.name)
                elif abs(amount) > 10:
                    await ctx.respond("You went over the 10 maximum! Taking " + str(abs(amount) + 2) + " reputation." )
                    db.update({"reputation": item.get("reputation") - (abs(amount) + 2)}, users.name == ctx.author.name)
            else:
                for item in db.all():
                    if item.get("name") == user.name:
                        db.update({"reputation": item.get("reputation") - amount}, users.name == item.get("name"))
                        db.update({"reputation": item.get("reputation") - (amount + 1)}, users.name == ctx.author.name)
                        await ctx.defer(ephemeral=True)
                        await ctx.respond("Removed " + str(abs(amount)) + " from " + user.name)

@bot.command(description="Increases others' rep if yours >50, max 10; deducts same plus one from yours if used right.")
async def addreputation(ctx, user: discord.Option(discord.SlashCommandOptionType.user), amount: discord.Option(int)):
    for item in db.all():
        if item.get("name") == ctx.author.name:
            if not item.get("reputation") > 50 or abs(amount) > 10:
                if item.get("reputation") < 0:
                    await ctx.respond(getInsult())
                    db.update({"reputation": item.get("reputation") - round(abs(amount) * 2)}, users.name == ctx.author.name)
                elif item.get("reputation") >= 0:
                    await ctx.respond("Your reputation is too low to use this command! Taking " + str((abs(amount) + 3)) + " reputation.")
                    db.update({"reputation": item.get("reputation") - (abs(amount) + 3)}, users.name == ctx.author.name)
                elif abs(amount) > 10:
                    await ctx.respond("You went over the 10 maximum! Taking " + str((abs(amount) + 2)) + " reputation." )
                    db.update({"reputation": item.get("reputation") - (abs(amount) + 2)}, users.name == ctx.author.name)
            else:
                for item in db.all():
                    if item.get("name") == user.name:
                        db.update({"reputation": item.get("reputation") + amount}, users.name == item.get("name"))
                        db.update({"reputation": item.get("reputation") - (amount + 1)}, users.name == ctx.author.name)
                        await ctx.respond("Added " + int(abs(amount)) + " from " + user.name)

@bot.command(description="Increases others' rep if yours >75, max 10; deducts same plus one from yours if used right.")
async def addreputationsecretly(ctx, user: discord.Option(discord.SlashCommandOptionType.user), amount: discord.Option(int)):
    for item in db.all():
        if item.get("name") == ctx.author.name:
            if not item.get("reputation") > 75 or abs(amount) > 10:
                if item.get("reputation") < 0:
                    await ctx.respond(getInsult())
                    db.update({"reputation": item.get("reputation") - round(abs(amount) * 2)}, users.name == ctx.author.name)
                elif item.get("reputation") >= 0:
                    await ctx.respond("Your reputation is too low to use this command! Taking " + str((abs(amount) + 3)) + " reputation.")
                    db.update({"reputation": item.get("reputation") - (abs(amount) + 3)}, users.name == ctx.author.name)
                elif abs(amount) > 10:
                    await ctx.respond("You went over the 10 maximum! Taking " + str((abs(amount) + 2)) + " reputation." )
                    db.update({"reputation": item.get("reputation") - (abs(amount) + 2)}, users.name == ctx.author.name)
            else:
                for item in db.all():
                    if item.get("name") == user.name:
                        db.update({"reputation": item.get("reputation") + amount}, users.name == item.get("name"))
                        db.update({"reputation": item.get("reputation") - (amount + 1)}, users.name == ctx.author.name)
                        await ctx.defer(ephemeral=True)
                        await ctx.respond("Added " + str(abs(amount)) + " from " + user.name)

bot.run(token)