import interactions
import database.models.SetupElement
import tol
import database.models.User
import database.Setups

class UpdateSetup(interactions.Extension):
    @interactions.slash_command(
        name="updatesetup",
        description="Update your setup",
        scopes=[tol.homeGuild]
    )

    @interactions.slash_option(
        name="element",
        argument_name="element",
        description="What element to update",
        required=True,
        opt_type=interactions.OptionType.STRING
    )

    @interactions.slash_option(
        name="value",
        argument_name="value",
        description="What value to set it to",
        required=True,
        opt_type=interactions.OptionType.STRING
    )
    
   

    async def updatesetup(self, ctx: interactions.SlashContext, element, value):
        userObj = database.models.User.userFromDiscordId(self.bot.db, ctx.author.id)
        if userObj == None:
            await ctx.send("User is not registered!")
            return
        
        elementObj = database.models.SetupElement.setupElementFromId(self.bot.db, element)
        if elementObj == None:
            await ctx.send("Invalid element!")
            return
        
        if elementObj.valueType == "num":
            try:
                float(value)
            except:
                await ctx.send("Value must be a number!")


        database.Setups.upsertUserSetup(self.bot.db, userObj, elementObj, value)
        await ctx.send("Updated!")

                
            


        
        

        
        
    


