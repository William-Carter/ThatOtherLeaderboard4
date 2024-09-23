import interactions
import database.leaderboards
import database.models.Category
import UI.leaderboards
import UI.durations

class Leaderboard(interactions.Extension):
    @interactions.slash_command(
        name="leaderboard",
        description="See the leaderboard for a category",
    )
    @interactions.slash_option(
        name="category",
        argument_name="category",
        description="The category you want to the leaderboard for",
        required=True,
        opt_type=interactions.OptionType.STRING
    )
    async def leaderboard(self, ctx: interactions.SlashContext, category: str = None):

        categoryObj = database.models.Category.categoryFromName(self.bot.db, category)
        if categoryObj == None:
            await ctx.send(f"{category.title()} is not a valid category!")
            return

        dbData = database.leaderboards.getLeaderboard(self.bot.db, categoryObj.id)
        formatted = [[x[0], UI.durations.formatted(x[1])] for x in dbData]
        lb = UI.leaderboards.Leaderboard(["Runner", "Time"], formatted, 1)
        response = f"Leaderboard for {categoryObj.name.title()}:\n"
        response += lb.getDiscordFormattedMessage()
        await ctx.send(response)
            

