import interactions
import tol
import commandlogic.UpdateGolds
from database.models import User


class UpdateGoldsFor(interactions.Extension):
    @interactions.slash_command(
        name="updategoldsfor",
        description="Update someone else's golds for a given category",
        scopes=[tol.homeGuild]
    )

    @interactions.slash_option(
        name="user",
        argument_name="username",
        description="Who to submit on behalf of",
        required=True,
        opt_type=interactions.OptionType.STRING
    )

    @interactions.slash_option(
        name="category",
        argument_name="category",
        description="What category to update golds for",
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

    async def updategolds(self, ctx: interactions.SlashContext, username: str, category: str, times: str):
        userObj = User.userFromName(self.bot.db, username)
        if userObj == None:
            await ctx.send(f"No user with name {username}")
            return
        
        await commandlogic.UpdateGolds.Updategolds(self, ctx, userObj, category, times)
        
        




        

                
            


        
        

        
        
    


