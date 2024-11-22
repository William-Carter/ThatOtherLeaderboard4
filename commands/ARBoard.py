import interactions
import UI.durations
import UI.neatTables
import UI.leaderboards
from database import leaderboards

class ARBoard(interactions.Extension):
    @interactions.slash_command(
        name="arboard",
        description="See the leaderboard for AMC sums",
    )
    @interactions.slash_option(
        name="start",
        argument_name="start",
        description="Where to start the leaderboard (defaults to 1st place)",
        required=False,
        opt_type=interactions.OptionType.INTEGER
    )

    async def arboard(self, ctx: interactions.SlashContext, start: int = 1):
        data = [[ar["name"], str(ar["avgRank"])] for ar in leaderboards.getAverageRankLeadboard(self.bot.db)]
        gb = UI.leaderboards.Leaderboard(["Runner", "Average Rank"], data, 1, start)

        await ctx.send(f"Average Rank Leaderboard:\n"+gb.getDiscordFormattedMessage())
