import interactions
import tol
import commandlogic.UpdateSegments
import database.models.User

class UpdateSegments(interactions.Extension):
    @interactions.slash_command(
        name="updatesegments",
        description="Update your PB segments for a given category",
        scopes=[tol.homeGuild]
    )

    @interactions.slash_option(
        name="category",
        argument_name="category",
        description="The category of the run you're adding segments for",
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
        description="The ID of the run you're updating segments for.",
        required=False,
        opt_type=interactions.OptionType.INTEGER
    )

    async def updatesegments(self, ctx: interactions.SlashContext, category: str, times: str, runId: int = -1):

        userObj = database.models.User.userFromDiscordId(self.bot.db, ctx.author.id)
        if userObj == None:
            await ctx.send("User is not registered!")
            return
        
        await commandlogic.UpdateSegments.UpdateSegments(self, ctx, userObj, category, times, runId)
        
        




        

                
            


        
        

        
        
    


