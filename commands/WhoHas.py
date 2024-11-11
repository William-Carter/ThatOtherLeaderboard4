import interactions
import UI.durations
import UI.neatTables
import database.leaderboards
from database.models import Category
class WhoHas(interactions.Extension):
    @interactions.slash_command(
        name="whohas",
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
    
    async def whohas(self, ctx: interactions.SlashContext, category: str, time: str):
        categoryObj = Category.categoryFromName(self.bot.db, category.lower())
        if categoryObj == None:
            await ctx.send(f"{category.title()} is not a valid category!")
            return
        
        timeFloat = UI.durations.seconds(time)
        if not timeFloat:
            await ctx.send(f"Invalid time!")
            return
        
        # Correct to tick to make sure ties are handled correctly when calculating place

        lb = database.leaderboards.getLeaderboard(self.bot.db, categoryObj.id)

        playersWithTime = []
        for run in lb:
            if timeFloat >= run[1]:
                playersWithTime.append(run)
            else:
                break

        playersWithTime = list(reversed(playersWithTime))

        tableData = [["Player", "Time"]]
        for player in playersWithTime[:min(len(playersWithTime), 20)]:
            tableData.append([player[0], UI.durations.formatted(player[1])])

        response = f"There are {len(playersWithTime)} people with a time of {UI.durations.formatted(timeFloat)} or better.\n"
        if len(playersWithTime) > 20:
            response += "Here are the 20 slowest.\n"

        response += "```"+UI.neatTables.generateTable(tableData)+"```"
        await ctx.send(response)