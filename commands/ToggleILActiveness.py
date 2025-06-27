import interactions
import database.categories
import tol
from database.models import IndividualLevelCategory as ilc
from database.models import Map

class ToggleILActiveness(interactions.Extension):
    @interactions.slash_command(
        name="toggleil",
        description="Toggle whether an IL leaderboard actively contributes to the points rankings",
        scopes=[tol.homeGuild]
    )

    @interactions.slash_option(
        name="category",
        argument_name="category",
        description="The category of the il",
        required=True,
        opt_type=interactions.OptionType.STRING
    )
    @interactions.slash_option(
        name="map",
        argument_name="map",
        description="The map of the il",
        required=True,
        opt_type=interactions.OptionType.STRING
    )


    async def toggleil(self, ctx: interactions.SlashContext, category: str, map: str):
        categoryObj = ilc.individualLevelCategoryFromName(self.bot.db, category)
        if categoryObj == None:
            await ctx.send("Invalid category!")
            return

        mapObj = Map.mapFromName(self.bot.db, map)
        if mapObj == None:
            await ctx.send("Invalid map!")
            return
        
        newState = database.categories.toggleILActiveness(self.bot.db, mapObj.id, categoryObj.id)

        if newState:
            await ctx.send("IL is now active!")
        else:
            await ctx.send("IL is no longer active!")
 