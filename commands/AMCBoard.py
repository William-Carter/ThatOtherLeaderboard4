import interactions
import UI.durations
import UI.neatTables
import UI.leaderboards
from database import AMC

class AMCBoard(interactions.Extension):
    @interactions.slash_command(
        name="amcboard",
        description="See the leaderboard for AMC sums",
    )
    @interactions.slash_option(
        name="start",
        argument_name="start",
        description="Where to start the leaderboard (defaults to 1st place)",
        required=False,
        opt_type=interactions.OptionType.INTEGER
    )

    async def amcboard(self, ctx: interactions.SlashContext, start: int = 1):
        

        data = [[amc["Name"], UI.durations.formatted(amc["AMCTotal"])] for amc in AMC.getAmcLeaderboard(self.bot.db)]

        
        rows = 20
        startIndex = start-1
        endIndex = min(startIndex + rows, len(data))
        gb = UI.leaderboards.Leaderboard(["Runner", "AMC"], data, startIndex=startIndex, endIndex=endIndex)

        await ctx.send(f"AMC Leaderboard:\n"+gb.getDiscordFormattedMessage())
