import interactions
import database.models.User
import UI.durations
import UI.neatTables
import database.sprm

class Seconds(interactions.Extension):
    @interactions.slash_command(
        name="seconds",
        description="Convert a number of ticks into seconds and minutes",
    )
    @interactions.slash_option(
        name="ticks",
        argument_name="ticks",
        description="The number of ticks you want to convert to seconds and minutes",
        required=True,
        opt_type=interactions.OptionType.INTEGER
    )

    async def seconds(self, ctx: interactions.SlashContext, ticks: int):
        
        seconds = round(ticks*0.015, 3)

        response = f"{ticks} ticks is {UI.durations.formatted(seconds)}"
        await ctx.send(response)

