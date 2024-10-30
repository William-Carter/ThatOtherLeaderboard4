import interactions
import commandlogic.Eligible
import database.models.User
import commandlogic

class Eligible(interactions.Extension):
    @interactions.slash_command(
        name="eligible",
        description="Toggle whether a run is eligible to be on the community gold leaderboard",
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


    async def eligible(self, ctx: interactions.SlashContext, category: str, map: str):
        userObj = database.models.User.userFromDiscordId(self.bot.db, ctx.author.id)
        if userObj == None:
            ctx.send("User is not registered!")
            return
        
        await commandlogic.Eligible.Eligible(self, ctx, userObj, category, map)
 