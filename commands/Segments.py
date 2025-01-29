import interactions
import database.models.User
import database.models.Gold
import database.models.Category
import UI.durations
import UI.neatTables
import database.sprm

class Segments(interactions.Extension):
    @interactions.slash_command(
        name="segments",
        description="See the segment times for a run",
        sub_cmd_name="pb",
        sub_cmd_description="See the segment times for someone's current PB"
    )
    @interactions.slash_option(
        name="category",
        argument_name="category",
        description="The category of the run. Will use the fastest qualifying run.",
        required=True,
        opt_type=interactions.OptionType.STRING
    )

    @interactions.slash_option(
        name="user",
        argument_name="username",
        description="The user whose segments you wish to see. Defaults to yourself if left blank.",
        required=False,
        opt_type=interactions.OptionType.STRING
    )


    async def segmentsForPb(self, ctx: interactions.SlashContext, category: str, username: str = None):
        await ctx.send("Segments for PB")


    @interactions.slash_command(
        name="segments",
        description="See the segment times for a run",
        sub_cmd_name="id",
        sub_cmd_description="See the segment times for a run based on its id"
    )
    @interactions.slash_option(
        name="id",
        argument_name="runId",
        description="The ID of the run",
        required=True,
        opt_type=interactions.OptionType.INTEGER
    )
    async def segmentsForId(self, ctx: interactions.SlashContext, runId: int):
        await ctx.send("Segments for ID")
        


