import interactions
import database.models.Map
import database.models.User
import database.models.Category
import database.models.User
import UI.durations
import UI.neatTables
import UI.leaderboards
from database import Golds

class Goldboard(interactions.Extension):
    @interactions.slash_command(
        name="goldboard",
        description="See the leaderboard for sum of bests or golds for a specific chamber",
    )
    @interactions.slash_option(
        name="category",
        argument_name="category",
        description="What category to see the leaderboard for",
        required=True,
        opt_type=interactions.OptionType.STRING
    )

    @interactions.slash_option(
        name="map",
        argument_name="mapName",
        description="The map to see the leaderboard for (shows sum of best leaderboard if left blank)",
        required=False,
        opt_type=interactions.OptionType.STRING
    )

    @interactions.slash_option(
        name="start",
        argument_name="start",
        description="Where to start the leaderboard (defaults to 1st place)",
        required=False,
        opt_type=interactions.OptionType.INTEGER
    )

    async def goldboard(self, ctx: interactions.SlashContext, category: str, mapName: str = None, start: int = 1):
        categoryObj = database.models.Category.categoryFromName(self.bot.db, category.lower())

        if categoryObj == None:
            await ctx.send(f"{category.title()} is not a valid category!")
            return
        
        if mapName:
            mapObj = database.models.Map.mapFromName(self.bot.db, mapName.lower())
            if mapObj == None:
                await ctx.send(f"Map does not exist!")
                return


            golds = [[gold[0].name, UI.durations.formatted(gold[1])] for gold in Golds.getGoldLeaderboard(self.bot.db, categoryObj, mapObj)]
            rows = 20
            startIndex = start-1
            endIndex = min(startIndex + rows, len(golds))
            gb = UI.leaderboards.Leaderboard(["Runner", "Gold"], golds, startIndex=startIndex, endIndex=endIndex)

            await ctx.send(f"Gold Leaderboard for {categoryObj.name.title()} {mapObj.name}:\n"+gb.getDiscordFormattedMessage())

        else:
            golds = [[gold[0].name, UI.durations.formatted(gold[1])] for gold in Golds.getSumOfBestLeaderboard(self.bot.db, categoryObj)]
            rows = 20
            startIndex = start-1
            endIndex = min(startIndex + rows, len(golds))
            gb = UI.leaderboards.Leaderboard(["Runner", "Sum of Best"], golds, startIndex=startIndex, endIndex=endIndex)

            await ctx.send(f"Sum of Best Leaderboard for {categoryObj.name.title()}:\n"+gb.getDiscordFormattedMessage())
            