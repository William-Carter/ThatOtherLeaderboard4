import interactions
import UI.durations
import UI.differences
from database.models import Category
from database.models import User
from database.models import Map
from database import Maps
from database import MapTimes
from database import Golds


async def Updategolds(command: interactions.Extension, ctx: interactions.SlashContext, userObj: User.User, category: str, times: str):
    categoryObj = Category.categoryFromName(command.bot.db, category)
    if categoryObj == None:
        await ctx.send("Invalid category!")
        return
    
    maps = Maps.getMainLevels(command.bot.db)

    timeList = times.strip().split(" ")
    if len(timeList) != len(maps):
        await ctx.send("Incorrect number of times given!")
        return
    
    timeNums = []
    for index, time in enumerate(timeList):
        timeNum = UI.durations.seconds(time)
        if not timeNum:
            await ctx.send(f"Time for {maps[index].name} invalid!")
            return
        
        timeNum = UI.durations.correctToTick(timeNum)
        timeNums.append([maps[index], timeNum])
        
    oldSob = userObj.getSumOfBest(categoryObj)
    oldComgolds = Golds.getCommunityGolds(command.bot.db, categoryObj)
    Golds.upsertGolds(command.bot.db, userObj, categoryObj, timeNums)
    newSob = sum([x[1] for x in timeNums])
    newComgolds = Golds.getCommunityGolds(command.bot.db, categoryObj)
    difference = round(oldSob-newSob, 3)

    newSobFormatted = UI.durations.formatted(newSob)

    await ctx.send(f"```ansi\nUpdated golds! New sum of best is {newSobFormatted} ({UI.differences.colourDifference(difference)})!```")
    await activityFeed(command, userObj, categoryObj, oldComgolds, newComgolds)

    
async def activityFeed(command: interactions.Extension, userObj: User.User, categoryObj: Category.Category, oldComgolds: list, newComgolds: list):
    updates = []
    for index, gold in enumerate(oldComgolds):
        if gold[1] != newComgolds[index][1]: # check if the gold has changed
            if gold[1] > newComgolds[index][1]: # make sure that it's faster (a rollback shouldn't send a notif)
                updates.append(
                    f"{userObj.name} beat the community gold for {categoryObj.name.title()} {gold[0].name} with a time of {UI.durations.formatted(newComgolds[index][1])}!"
                )

        elif len(gold[2]) < len(newComgolds[index][2]): # check if a new person has the same gold
            updates.append(
                f"{userObj.name} tied the community gold for {categoryObj.name.title()} {gold[0].name} with a time of {UI.durations.formatted(newComgolds[index][1])}!"
            )


    for update in updates:
        await command.bot.activityFeed.send("`"+update+"`")

