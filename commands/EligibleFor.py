import interactions
import commandlogic.Eligible
import database.models.User
import commandlogic

class EligibleFor(interactions.Extension):
    @interactions.slash_command(
        name="eligiblefor",
        description="Toggle whether someone else's gold is eligible to be on the community gold leaderboard",
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
        description="The category you want to update",
        required=True,
        opt_type=interactions.OptionType.STRING
    )
    
    @interactions.slash_option(
        name="map",
        argument_name="map",
        description="The map you want to update",
        required=True,
        opt_type=interactions.OptionType.STRING
    )


    async def eligiblefor(self, ctx: interactions.SlashContext, username: str, category: str, map: str):
        userObj = database.models.User.userFromName(self.bot.db, username)
        if userObj == None:
            ctx.send(f"No user with name {username}")
            return
        
        await commandlogic.Eligible.Eligible(self, ctx, userObj, category, map)
 