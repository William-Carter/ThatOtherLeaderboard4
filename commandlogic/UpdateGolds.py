import interactions
import UI.durations
from database.models import Category
from database.models import User
from database.models import Map
from database import Maps
from database import MapTimes


async def Updategolds(command: interactions.Extension, ctx: interactions.SlashContext, userObj: User, category: str, times: str):
    categoryObj = Category.categoryFromName(command.bot.db, category)
    if categoryObj == None:
        await ctx.send("Invalid category!")
        return
    
    maps = Maps.getMainLevels(command.bot.db)

    timeList = times.strip().split(" ")
    if len(timeList) != 18:
        await ctx.send("Incorrect number of times given!")
        return
    
    timeNums = []
    for index, time in enumerate(timeList):
        timeNum = UI.durations.seconds(time)
        if not timeNum:
            await ctx.send(f"Time for {maps[index].name} invalid!")
            return
        timeNums.append([maps[index], timeNum])
        
    
    MapTimes.upsertMapTimes(command.bot.db, userObj, "gold", categoryObj, timeNums)
    sob = UI.durations.formatted(sum([x[1] for x in timeNums]))
    await ctx.send(f"```ansi\nUpdated golds! Your new sum of best is {sob}!```")
    # TODO get previous sum of best and show difference with highlighted text



    
