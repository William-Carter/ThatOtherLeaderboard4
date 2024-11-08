import interactions
import UI.durations
import UI.differences
from database.models import Category
from database.models import User
from database import Maps
from database import MapTimes


async def UpdateSegments(command: interactions.Extension, ctx: interactions.SlashContext, userObj: User.User, category: str, times: str):
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
    total = 0
    for index, time in enumerate(timeList):
        timeNum = UI.durations.seconds(time)
        if not timeNum:
            await ctx.send(f"Time for {maps[index].name} invalid!")
            return
        
        timeNum = UI.durations.correctToTick(timeNum)
        total += timeNum
        timeNums.append([maps[index], timeNum])
        
    MapTimes.upsertMapTimes(command.bot.db, userObj, "segment", categoryObj, timeNums)


    pbRun = userObj.getPersonalBest(categoryObj)
    response = f"```ansi\nUpdated PB segments for a run of {UI.durations.formatted(total)}!"
    if round(total, 3) != round(pbRun.time, 3):
        response += f"\nThis doesn't match your recorded PB ({UI.durations.formatted(pbRun.time)}), double check any discrepancies!"

    response += "```"

    await ctx.send(response)