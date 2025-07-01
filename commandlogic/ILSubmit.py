import interactions
import UI.validations
import UI.durations
import database.models.IndividualLevelRun
import database.ilpoints
import database.submissions
from database.models.User import User
from database.models import IndividualLevelCategory as ilc
from database.models import Map
from datetime import datetime


async def ILSubmit(command: interactions.Extension, ctx: interactions.SlashContext, userObj: User, category: str, map: str, time: str, date: str = None):
    if date and not UI.validations.checkDateFormat(date):
        await ctx.send("Invalid date!")
        return
    
    if not date:
        date = datetime.today().strftime('%Y-%m-%d')

    categoryObj = ilc.individualLevelCategoryFromName(command.bot.db, category)
    if categoryObj == None:
        await ctx.send("Invalid category!")
        return
    
    mapObj = Map.mapFromName(command.bot.db, map)
    if mapObj == None:
        await ctx.send("Invalid map!")
        return
    
    timeNum = UI.durations.seconds(time)
    if not timeNum:
        await ctx.send("Invalid time!")
        return
    
    
    previousPb = userObj.getILPersonalBest(categoryObj, mapObj)

    if (previousPb != None) and (timeNum >= previousPb.time):
        await ctx.send("An equal or faster time is already tracked!")
        return


    if previousPb != None:
        globalRankPriorToSubmission = previousPb.getRankInCategory(categoryObj)
    

    run = database.submissions.submitIndividualLevelRun(command.bot.db, userObj, timeNum, date, mapObj, categoryObj)

    changes = []
    # List formatted as [name, oldValue, newValue]

    newRank = run.getRankInCategory(categoryObj)
    if previousPb != None:
        changes.append(["Rank:", 
                        globalRankPriorToSubmission, 
                        newRank
                        ])
    
    if not categoryObj.isExtension:
        if previousPb != None:
            pointsPriorToSubmission = int(round(database.ilpoints.points(globalRankPriorToSubmission), 0))
        else:
            pointsPriorToSubmission = 0

        changes.append(["Points:", 
                        pointsPriorToSubmission, 
                        int(round(database.ilpoints.points(newRank), 0))
                        ])

    response = f"```ansi\nSubmitted a run of {UI.durations.formatted(run.time)} to {mapObj.name} {categoryObj.name.title()} for {userObj.name}"
    for change in changes:
        difference = abs(change[2]-change[1])

        colour = "\u001b[0m"
        if difference > 0:
            colour = "\u001b[0;32m"
        

        response += f"\n{change[0]} {change[1]} -> {change[2]} ({colour}+{difference}\u001b[0m)"
    

    response += "```"


    await ctx.send(response)

    await activityFeed(command, userObj, categoryObj, mapObj, run)



async def activityFeed(command: interactions.Extension, userObj: User, categoryObj: ilc.IndividualLevelCategory, map: Map.Map, run: database.models.IndividualLevelRun.IndividualLevelRun):
    response = f"{userObj.name} achieved a time of {UI.durations.formatted(run.time)} in {map.name} {categoryObj.name.title()}"
    globalRank = run.getRankInCategory(categoryObj)

    if globalRank == 1:
        response += ", a new World Record!"

    else:
        response += f", ranking them {UI.durations.formatLeaderBoardPosition(globalRank)} in the world"


    await command.bot.activityFeed.send("```"+response+"```")