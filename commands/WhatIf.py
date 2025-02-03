import interactions
import UI.durations
import database.leaderboards
import database.sprm
from database.models import Category
class WhatIf(interactions.Extension):
    @interactions.slash_command(
        name="whatif",
        description="Check what a given time would place in a given category",
    )
    @interactions.slash_option(
        name="category",
        argument_name="category",
        description="Which category to check for",
        required=True,
        opt_type=interactions.OptionType.STRING
    )
    @interactions.slash_option(
        name="time",
        argument_name="time",
        description="The time to check",
        required=True,
        opt_type=interactions.OptionType.STRING
    )
    

    async def whatif(self, ctx: interactions.SlashContext, category: str, time: str):
        categoryObj = Category.categoryFromName(self.bot.db, category.lower())
        if categoryObj == None:
            await ctx.send(f"{category.title()} is not a valid category!")
            return
        
        timeFloat = UI.durations.seconds(time)
        if not timeFloat:
            await ctx.send(f"Invalid time!")
            return
        
        # Correct to tick to make sure ties are handled correctly when calculating place
        timeFloat = UI.durations.correctToTick(timeFloat)

        lb = database.leaderboards.getLeaderboard(self.bot.db, categoryObj.id)

        placement = 1
        for run in lb:
            if timeFloat > run[1]:
                placement += 1
            else:
                break

        sprmValue = database.sprm.calculateSprm(self.bot.db, categoryObj, timeFloat)

        response = f"A time of {UI.durations.formatted(timeFloat)} would place {UI.durations.formatLeaderBoardPosition(placement)} on the {categoryObj.name.title()} leaderboard and have a SPRM of {sprmValue}"
        await ctx.send(response)