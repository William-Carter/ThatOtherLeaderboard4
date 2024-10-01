import interactions
import os
import json
from database.Interface import Interface

dirPath = os.path.dirname(os.path.realpath(__file__))

bot = interactions.Client(intents=interactions.Intents.DEFAULT)
bot.db = Interface(dirPath+"/ThatOtherLeaderboard.db")


@interactions.listen()
async def on_startup():
    bot.activityFeed = await bot.fetch_channel(1290549823992238120)
    print("Bot is ready!")
    print("Bot is in:")
    for guild in bot.guilds:
        print(guild.name, guild.id)


# Attempt to load all files in the commands directory as extensions
for item in os.scandir(dirPath+"/commands/"):
    if os.path.isfile(f"commands/{item.name}"):
        bot.load_extension(f"commands.{item.name[:-3]}") # Strip .py for import


# Load bot token from config file
with open(dirPath+"/config.json", "r") as f:
    data = json.load(f)
    token = data["token"]

bot.start(token)