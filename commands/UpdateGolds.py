import interactions
import tol
import database.models.User
import commandlogic.UpdateGolds

class UpdateGolds(interactions.Extension):
    @interactions.slash_command(
        name="updategolds",
        description="Update your golds for a given category",
        scopes=[tol.homeGuild]
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

    async def updategolds(self, ctx: interactions.SlashContext, category: str, times: str):

        userObj = database.models.User.userFromDiscordId(self.bot.db, ctx.author.id)
        if userObj == None:
            await ctx.send("User is not registered!")
            return
        
        await commandlogic.UpdateGolds.Updategolds(self, ctx, userObj, category, times)
        
        




        

                
            


        
        

        
        
    


