import interactions
import database.sprm
import database.models.Category
import UI.durations

class Sprm(interactions.Extension):
    @interactions.slash_command(
        name="sprm",
        description="Calculate the SPRM for a given time in a given category",
    )

    @interactions.slash_option(
        name="time",
        argument_name="time",
        description="What time to calculate SPRM for",
        required=True,
        opt_type=interactions.OptionType.STRING
    )
    
    @interactions.slash_option(
        name="category",
        argument_name="category",
        description="What category to calculate SPRM for",
        required=True,
        opt_type=interactions.OptionType.STRING
    )
    

    async def sprm(self, ctx: interactions.SlashContext, category: str, time: str):
        categoryObj = database.models.Category.categoryFromName(self.bot.db, category.lower())
        if categoryObj == None:
            await ctx.send(f"{category.title()} is not a valid category!")
            return
        
        timeFloat = UI.durations.seconds(time)
        if not timeFloat:
            await ctx.send(f"Invalid time!")
            return
        
        calculatedSprm = database.sprm.calculateSprm(self.bot.db, categoryObj, timeFloat)

        await ctx.send(f"A time of {UI.durations.formatted(timeFloat)} in {categoryObj.name.title()} gives a score of {calculatedSprm}")
            

