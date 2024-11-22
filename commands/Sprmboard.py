import interactions
import database.leaderboards
import database.sprm
import database.models.Country
import database.models.Continent
import UI.leaderboards
import UI.durations

class Sprmboard(interactions.Extension):
    @interactions.slash_command(
        name="sprmboard",
        description="See the leaderboard for the Subjective Player Ranking Metric",
    )

    @interactions.slash_option(
        name="start",
        argument_name="start",
        description="Where to start the leaderboard (defaults to 1st place)",
        required=False,
        opt_type=interactions.OptionType.INTEGER
    )

    async def sprmboard(self, ctx: interactions.SlashContext, start: int = 1):
        header = "Leaderboard for SPRM:\n"

        dbData = database.sprm.getSprmLeaderboard(self.bot.db)

        formatted = [[x['name'], str(int(round(x['sprm'], 0)))] for x in dbData]
        lb = UI.leaderboards.Leaderboard(["Runner", "SPRM"], formatted, 1, start)
        
        response = header + lb.getDiscordFormattedMessage()
        await ctx.send(response)
            

