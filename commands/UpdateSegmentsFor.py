import interactions
import tol
import commandlogic.UpdateSegments
import database.models.User

class UpdateSegmentsFor(interactions.Extension):
    @interactions.slash_command(
        name="updatesegmentsfor",
        description="Update someone else's PB segments for a given category",
        scopes=[tol.homeGuild]
    )

    @interactions.slash_option(
        name="user",
        argument_name="username",
        description="The user to update for",
        required=True,
        opt_type=interactions.OptionType.STRING
    )

    @interactions.slash_option(
        name="category",
        argument_name="category",
        description="What category the run is",
        required=True,
        opt_type=interactions.OptionType.STRING
    )
    
    @interactions.slash_option(
        name="times",
        argument_name="times",
        description="A list of 18 times",
        required=True,
        opt_type=interactions.OptionType.STRING
    )

    @interactions.slash_option(
        name="runid",
        argument_name="runId",
        description="The ID of the run you're updating segments for. Will automatically identify the run if left blank.",
        required=False,
        opt_type=interactions.OptionType.INTEGER
    )

    async def updatesegments(self, ctx: interactions.SlashContext, username: str, category: str, times: str, runId: int = -1):

        userObj = database.models.User.userFromName(self.bot.db, username)
        if userObj == None:
            await ctx.send(f"No user with name {username}!")
            return
        
        await commandlogic.UpdateSegments.UpdateSegments(self, ctx, userObj, category, times, runId)
        
        




        

                
            


        
        

        
        
    


