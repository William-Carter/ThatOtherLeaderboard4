import interactions
import database.models.FullGameRun
import database.models.User
import database.sprm
import database.models.Country
import database.models.Category
import database.categories
import database.submissions
import UI.durations
import UI.validations
from datetime import datetime

class Submit(interactions.Extension):
    @interactions.slash_command(
        name="submit",
        description="Submit a run to the leaderboard",
    )

    @interactions.slash_option(
        name="category",
        argument_name="category",
        description="What category to submit a run to",
        required=True,
        opt_type=interactions.OptionType.STRING
    )
    
    @interactions.slash_option(
        name="time",
        argument_name="time",
        description="Your run's final time",
        required=True,
        opt_type=interactions.OptionType.STRING
    )
    @interactions.slash_option(
        name="date",
        argument_name="date",
        description="The date your run was performed (defaults to today if left blank)",
        required=False,
        opt_type=interactions.OptionType.STRING
    )

    async def submit(self, ctx: interactions.SlashContext, category: str, time: str, date: str = None):
        if date and not UI.validations.checkDateFormat(date):
            await ctx.send("Invalid date!")
            return
        
        if not date:
            date = datetime.today().strftime('%Y-%m-%d')

        categoryObj = database.models.Category.categoryFromName(self.bot.db, category)
        if categoryObj == None:
            await ctx.send("Invalid category!")
            return
        
        timeNum = UI.durations.seconds(time)
        if not timeNum:
            await ctx.send("Invalid time!")
            return
        
        userObj = database.models.User.userFromDiscordId(self.bot.db, ctx.author.id)
        if userObj == None:
            ctx.send("User is not registered!")
            return
        
        previousPb = userObj.getPersonalBest(categoryObj)

        if timeNum >= previousPb.time:
            ctx.send("An equal or faster time is already tracked!")
            return


        globalRankPriorToSubmission = previousPb.getRankInCategory(categoryObj)
        sprmPriorToSubmission = int(round(database.sprm.calculateSprm(self.bot.db, categoryObj, previousPb.time), 0))
        # TODO get average rank

        run = database.submissions.submitFullGameRun(self.bot.db, userObj, timeNum, date, categoryObj)

        changes = []
        # List formatted as [name, oldValue, newValue]
        changes.append(["Rank:", 
                       globalRankPriorToSubmission, 
                       run.getRankInCategory(categoryObj)])
        changes.append(["SPRM:", 
                       sprmPriorToSubmission, 
                       int(round(database.sprm.calculateSprm(self.bot.db, categoryObj, run.time), 0))])

        response = f"```ansi\nSubmitted a run of {UI.durations.formatted(run.time)} to {categoryObj.name.title()}"
        for change in changes:
            difference = abs(change[2]-change[1])

            colour = "\u001b[0m"
            if difference > 0:
                colour = "\u001b[0;32m"
            

            response += f"\n{change[0]} {change[1]} -> {change[2]} ({colour}+{difference}\u001b[0m)"
        

        response += "```"


        await ctx.send(response)




        

                
            


        
        

        
        
    


