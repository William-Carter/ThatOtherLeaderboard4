import interactions
import database.models.User
import commandlogic.Submit

class Submit(interactions.Extension):
    @interactions.slash_command(
        name="submit",
        description="Submit a run to the leaderboard",
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
        name="time",
        argument_name="time",
        description="Your run's final time",
        required=True,
        opt_type=interactions.OptionType.STRING
    )
    @interactions.slash_option(
        name="date",
        argument_name="date",
        description="The date your run was performed (defaults to today if left blank)",
        required=False,
        opt_type=interactions.OptionType.STRING
    )

    async def submit(self, ctx: interactions.SlashContext, category: str, time: str, date: str = None):

        userObj = database.models.User.userFromDiscordId(self.bot.db, ctx.author.id)
        if userObj == None:
            ctx.send("User is not registered!")
            return
        
        # Logic moved to separate file for reuse in moderator commands
        await commandlogic.Submit.Submit(self, ctx, userObj, category, time, date)

        




        

                
            


        
        

        
        
    


