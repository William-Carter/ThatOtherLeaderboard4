import interactions
import UI.durations
import UI.differences
from database.models import Category
from database.models import User
from database import Maps
from database.models import FullGameRun as fgr
from database import Segments


async def UpdateSegments(command: interactions.Extension, ctx: interactions.SlashContext, userObj: User.User, category: str, times: str, runId: int):
    categoryObj = Category.categoryFromName(command.bot.db, category)
    if categoryObj == None:
        await ctx.send("Invalid category!")
        return
    
    maps = Maps.getMainLevels(command.bot.db)

    timeList = times.strip().split(" ")
    if len(timeList) != len(maps):
        await ctx.send("Incorrect number of times given!")
        return
    
    mapTimes = []
    inputTotal = 0
    for index, time in enumerate(timeList):
        timeNum = UI.durations.seconds(time)
        if not timeNum:
            await ctx.send(f"Time for {maps[index].name} invalid!")
            return
        
        timeNum = UI.durations.correctToTick(timeNum)
        inputTotal += timeNum
        mapTimes.append([maps[index], timeNum])

    identifiedRun = None
    if runId == -1:
        # Iterate through every run on record for this user in this category to find one with a matching final time
        runs = userObj.getAllRunsButSlow(categoryObj)
        for run in runs:
            if run.time == inputTotal:
                identifiedRun = run
                break

        if identifiedRun == None:
            await ctx.send(f"No run matching those segments was found! You can specify the ID of the run to get around any problems.")
            return

    else:
        identifiedRun = fgr.fullGameRunFromId(command.bot.db, runId)
        if identifiedRun == None:
            await ctx.send(f"No run with that ID!")
            return

    Segments.upsertSegments(command.bot.db, identifiedRun, mapTimes)

    await ctx.send(f"Segments updated for run of {UI.durations.formatted(identifiedRun.time)}")

    

        
    