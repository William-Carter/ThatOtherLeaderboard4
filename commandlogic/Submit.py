import interactions
import UI.validations
import UI.durations
import database.submissions
from database.models.User import User
from database.models import Category
from datetime import datetime


async def Submit(command: interactions.Extension, ctx: interactions.SlashContext, userObj: User, category: Category.Category, time: str, date: str = None):
    if date and not UI.validations.checkDateFormat(date):
        await ctx.send("Invalid date!")
        return
    
    if not date:
        date = datetime.today().strftime('%Y-%m-%d')

    categoryObj = Category.categoryFromName(command.bot.db, category)
    if categoryObj == None:
        await ctx.send("Invalid category!")
        return
    
    timeNum = UI.durations.seconds(time)
    if not timeNum:
        await ctx.send("Invalid time!")
        return
    
    
    previousPb = userObj.getPersonalBest(categoryObj)

    if timeNum >= previousPb.time:
        await ctx.send("An equal or faster time is already tracked!")
        return


    globalRankPriorToSubmission = previousPb.getRankInCategory(categoryObj)
    sprmPriorToSubmission = int(round(database.sprm.calculateSprm(command.bot.db, categoryObj, previousPb.time), 0))
    # TODO get average rank

    run = database.submissions.submitFullGameRun(command.bot.db, userObj, timeNum, date, categoryObj)

    changes = []
    # List formatted as [name, oldValue, newValue]
    changes.append(["Rank:", 
                    globalRankPriorToSubmission, 
                    run.getRankInCategory(categoryObj)])
    changes.append(["SPRM:", 
                    sprmPriorToSubmission, 
                    int(round(database.sprm.calculateSprm(command.bot.db, categoryObj, run.time), 0))])

    response = f"```ansi\nSubmitted a run of {UI.durations.formatted(run.time)} to {categoryObj.name.title()} for {userObj.name}"
    for change in changes:
        difference = abs(change[2]-change[1])

        colour = "\u001b[0m"
        if difference > 0:
            colour = "\u001b[0;32m"
        

        response += f"\n{change[0]} {change[1]} -> {change[2]} ({colour}+{difference}\u001b[0m)"
    

    response += "```"


    await ctx.send(response)