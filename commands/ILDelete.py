import interactions
import database.models.IndividualLevelCategory
import database.models.IndividualLevelRun
import database.models.Map
import tol
import UI.durations
import deletion.Delete
import database.submissions
import database.models.FullGameRun
import database.models.User
import database.models.Category

class ILDelete(interactions.Extension):
    @interactions.slash_command(
        name="ildelete",
        description="Delete an IL run from the database",
        scopes=[tol.homeGuild]
    )

    @interactions.slash_option(
        name="runid",
        argument_name="runId",
        description="The ID of the run you want to delete (use /listils to find it)",
        required=True,
        opt_type=interactions.OptionType.INTEGER
    )
    @interactions.slash_option(
        name="code",
        argument_name="confirmNumber",
        description="The run deletion confirmation code",
        required=False,
        opt_type=interactions.OptionType.STRING
    )


    async def delete(self, ctx: interactions.SlashContext, runId: int, confirmNumber: str = None):
        if not confirmNumber:
            runObj = database.models.IndividualLevelRun.individualLevelrun(self.bot.db, runId)
            if runObj == None:
                await ctx.send("Run with that ID does not exist!")
                return
            
            userObj = database.models.User.userFromId(self.bot.db, runObj.userId)
            word = deletion.Delete.getVerificationWord(runId)
            categoryObj = database.models.IndividualLevelCategory.individualLevelCategory(self.bot.db, runObj.categories[0])
            mapObj = database.models.Map.map(self.bot.db, runObj.mapId)
            await ctx.send(f"`{runObj.id}`\nYou're trying to delete a {UI.durations.formatted(runObj.time)} run of {mapObj.name} {categoryObj.name.title()} by {userObj.name}\nIf you meant to do this, run this command again with the confirmation code `{word}`")
            


        else:
            if confirmNumber.lower() == deletion.Delete.getVerificationWord(runId):
                database.submissions.deleteIndividualLevelRun(self.bot.db, runId)
                await ctx.send("Run deleted.")
            else:
                await ctx.send("Incorrect confirmation code! Run was not deleted.")

        

    
 