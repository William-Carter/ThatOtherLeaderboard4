import interactions
import commandlogic.Submit
from database.models import User
class SubmitFor(interactions.Extension):
    @interactions.slash_command(
        name="submitfor",
        description="Submit a run to the leaderboard on behalf of someone else",
        scopes=[1081155162065862697]
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

    async def submitfor(self, ctx: interactions.SlashContext, username: str, category: str, time: str, date: str = None):
        userObj = User.userFromName(self.bot.db, username)
        if userObj == None:
            ctx.send(f"No user with name {username}")
            return
        
        # Logic moved to separate file for reuse in moderator commands
        await commandlogic.Submit.Submit(self, ctx, userObj, category, time, date)
        

        
