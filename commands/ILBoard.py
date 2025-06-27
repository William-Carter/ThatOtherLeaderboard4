import interactions
import database.leaderboards
import database.models.IndividualLevelCategory
import database.models.Map
import UI.leaderboards
import UI.durations

class ILBoard(interactions.Extension):
    @interactions.slash_command(
        name="ilboard",
        description="See the leaderboard for an individual level",
    )
    @interactions.slash_option(
        name="category",
        argument_name="category",
        description="The category you want to the leaderboard for",
        required=True,
        opt_type=interactions.OptionType.STRING
    )
    @interactions.slash_option(
        name="map",
        argument_name="map",
        description="The map you want to the leaderboard for",
        required=True,
        opt_type=interactions.OptionType.STRING
    )

    @interactions.slash_option(
        name="start",
        argument_name="start",
        description="Where to start the leaderboard (defaults to 1st place)",
        required=False,
        opt_type=interactions.OptionType.INTEGER
    )
    

    async def ilboard(self, ctx: interactions.SlashContext, category: str, map: str, start: int = 1):


        categoryObj = database.models.IndividualLevelCategory.individualLevelCategoryFromName(self.bot.db, category.lower())

        if categoryObj == None:
            await ctx.send(f"{category.title()} is not a valid category!")
            return
        
            
        mapObj = database.models.Map.mapFromName(self.bot.db, map)

        if mapObj == None:
            await ctx.send("Invalid map!")
            return

        header = f"Leaderboard for {mapObj.name} {categoryObj.name.title()}:\n"
        dbData = database.leaderboards.getIlLeaderboard(self.bot.db, categoryObj, mapObj)


        formatted = [[x[0], UI.durations.formatted(x[1])] for x in dbData]
        lb = UI.leaderboards.Leaderboard(["Runner", "Time"], formatted, 1, start)
        
        response = header + lb.getDiscordFormattedMessage()
        await ctx.send(response)
            

