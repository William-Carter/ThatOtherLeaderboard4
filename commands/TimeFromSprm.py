import interactions
import UI.neatTables
import database.leaderboards
import database.sprm
import database.models.Country
import database.models.Category
import database.categories
import UI.leaderboards
import UI.durations

class TimeFromSprm(interactions.Extension):
    @interactions.slash_command(
        name="timefromsprm",
        description="Calculate the time needed for a given SPRM",
    )
    
    @interactions.slash_option(
        name="sprm",
        argument_name="sprm",
        description="The SPRM number you want to see the time(s) for",
        required=True,
        opt_type=interactions.OptionType.NUMBER
    )
    @interactions.slash_option(
        name="category",
        argument_name="category",
        description="What category to calculate SPRM for. Leave blank to see all main categories.",
        required=False,
        opt_type=interactions.OptionType.STRING
    )

    async def timefromsprm(self, ctx: interactions.SlashContext, sprm: float, category: str = None):
        if category:
            categoryObj = database.models.Category.categoryFromName(self.bot.db, category.lower())
            if categoryObj == None:
                await ctx.send(f"{category.title()} is not a valid category!")
                return
            
            time = database.sprm.calculateInverseSprm(self.bot.db, categoryObj, sprm)

            await ctx.send(f"A score of {sprm} in {categoryObj.name.title()} requires a time of {UI.durations.formatted(UI.durations.correctToTick(time))}")
            
        
        else:
            categories = database.categories.getMainFullGameCategories(self.bot.db)
            tableData = [["Category", "Time Needed"]]
            for category in categories:
                tableData.append([category.name.title(), UI.durations.formatted(UI.durations.correctToTick(database.sprm.calculateInverseSprm(self.bot.db, category, sprm)))])


            response = f"An SPRM of {sprm} in each category would require:\n```"
            response += UI.neatTables.generateTable(tableData)
            response += "```"

            await ctx.send(response)
            
        

        
        
    


