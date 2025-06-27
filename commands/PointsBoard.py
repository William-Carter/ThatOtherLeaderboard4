import interactions
import database.leaderboards
import UI.leaderboards
from database.models import IndividualLevelCategory as ilc
class PointsBoard(interactions.Extension):
    @interactions.slash_command(
        name="pointsboard",
        description="See the leaderboard for a IL points",
    )
    @interactions.slash_option(
        name="category",
        argument_name="category",
        description="Only see points obtained in this category",
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

    async def pointsboard(self, ctx: interactions.SlashContext, category: str = None, start: int = 1):
        if category:
            categoryObj = ilc.individualLevelCategoryFromName(self.bot.db, category)
            if not categoryObj:
                await ctx.send("Invalid category!")
                return
            header = f"IL Points Leaderboard for {categoryObj.name.title()}"
            results = database.leaderboards.getIlPointsLeaderboard(self.bot.db, categoryObj)

        else:
            header = "IL Points Leaderboard"
            results = database.leaderboards.getIlPointsLeaderboard(self.bot.db)


        leaderboard = UI.leaderboards.Leaderboard(["Player", "Points"], results, keyColumn = 1, start = start)

        await ctx.send(header+"\n"+leaderboard.getDiscordFormattedMessage())
        