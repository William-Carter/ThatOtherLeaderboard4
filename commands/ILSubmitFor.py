import interactions
import tol
import database.models.User
import commandlogic.ILSubmit

class ILSubmitFor(interactions.Extension):
    @interactions.slash_command(
        name="ilsubmitfor",
        description="Submit a run to an IL leaderboard on behalf of someone else",
        scopes=[tol.homeGuild]
    )

    @interactions.slash_option(
        name="user",
        argument_name="user",
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
        name="map",
        argument_name="map",
        description="What map to submit a run to",
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
        description="The YYYY-MM-DD date your run was performed (defaults to today if left blank)",
        required=False,
        opt_type=interactions.OptionType.STRING
    )

    async def ilsubmit(self, ctx: interactions.SlashContext, user: str, category: str, map: str, time: str, date: str = None):

        userObj = database.models.User.userFromName(self.bot.db, user)
        if userObj == None:
            await ctx.send("No user with that name!")
            return
        
        # Logic moved to separate file for reuse in moderator commands
        await commandlogic.ILSubmit.ILSubmit(self, ctx, userObj, category, map, time, date)
