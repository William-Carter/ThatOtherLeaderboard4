import interactions
import UI.durations

class Ticks(interactions.Extension):
    @interactions.slash_command(
        name="ticks",
        description="Convert a time into a number of ticks",
    )
    @interactions.slash_option(
        name="time",
        argument_name="time",
        description="The time you want to convert to ticks",
        required=True,
        opt_type=interactions.OptionType.STRING
    )

    async def ticks(self, ctx: interactions.SlashContext, time: str):
        timeNum = UI.durations.seconds(time)
        if not timeNum:
            await ctx.send("Invalid time")
            return
        if timeNum == float('inf'):
            await ctx.send("Time too large!")
            return
        
        ticks = int(round(timeNum/0.015, 0))
        correctedTime = round(ticks*0.015, 3)

        response = f"Had to round: {correctedTime!=timeNum}\nTime: {UI.durations.formatted(correctedTime)}\nTicks: {ticks}"
        await ctx.send(response)

