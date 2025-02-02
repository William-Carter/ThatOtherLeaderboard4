import interactions
import UI.durations
import UI.neatTables
import database.sprm
from database.models import FullGameRun
from database.models import User
from database.models import Category

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
        if username:
            userObj = User.userFromName(self.bot.db, username)
        else:
            userObj = User.userFromDiscordId(self.bot.db, ctx.author.id)
                 
        if userObj == None:
            await ctx.send(f"No user with name {username}")
            return
        
        categoryObj = Category.categoryFromName(self.bot.db, category)
        if categoryObj == None:
            await ctx.send("Invalid category!")
            return
        
        run = userObj.getPersonalBest(categoryObj)
        if run == None:
            await ctx.send("User has no personal best in that category!")
            return
        
        segments = run.getSegments()
        if segments == None:
            await ctx.send("Run doesn't have any recorded segment times!")
            return
        
        await ctx.send(self.generateSegmentView(segments, run))



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
        run = FullGameRun.fullGameRunFromId(self.bot.db, runId)
        if run == None:
            await ctx.send("No run with that ID!")
            return
        
        segments = run.getSegments()
        if segments == None:
            await ctx.send("Run doesn't have any recorded segment times!")
            return
        
        await ctx.send(self.generateSegmentView(segments, run))
        
    def generateSegmentView(self, mapTimes: list[list], run: FullGameRun.FullGameRun) -> str:
        finalTime = UI.durations.formatted(run.time)
        userObj = User.userFromId(self.bot.db, run.userId)
        tableData = [["Map", "Time"]]
        for entry in mapTimes:
            tableData.append([entry[0].name, UI.durations.formatted(entry[1])])

        return f"```\nSegments for a Run of {finalTime} by {userObj.name}\n" + UI.neatTables.generateTable(tableData) + f"\nFinal Time: {finalTime}```"
        
        


