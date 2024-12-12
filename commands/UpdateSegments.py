import interactions
import commandlogic.UpdateSegments
import database.models.User

class UpdateSegments(interactions.Extension):
    @interactions.slash_command(
        name="updatesegments",
        description="Update your PB segments for a given category",
        scopes=[1081155162065862697]
    )

    @interactions.slash_option(
        name="category",
        argument_name="category",
        description="What category to submit a run to",
        required=True,
        opt_type=interactions.OptionType.STRING
    )
    
    @interactions.slash_option(
        name="times",
        argument_name="times",
        description="A list of times",
        required=True,
        opt_type=interactions.OptionType.STRING
    )

    async def updatesegments(self, ctx: interactions.SlashContext, category: str, times: str):

        userObj = database.models.User.userFromDiscordId(self.bot.db, ctx.author.id)
        if userObj == None:
            await ctx.send("User is not registered!")
            return
        
        await commandlogic.UpdateSegments.UpdateSegments(self, ctx, userObj, category, times)
        
        




        

                
            


        
        

        
        
    


