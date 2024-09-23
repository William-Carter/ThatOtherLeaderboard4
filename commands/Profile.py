import interactions
import database.models.User

class Profile(interactions.Extension):
    @interactions.slash_command(
        name="profile",
        description="See a user's profile",
    )
    @interactions.slash_option(
        name="user",
        argument_name="username",
        description="The user whose profile you wish to see",
        required=False,
        opt_type=interactions.OptionType.STRING
    )
    async def profile(self, ctx: interactions.SlashContext, username: str = None):
        if username:
            user = database.models.User.userFromName(self.bot.db, username)
            if user == None:
                await ctx.send(f"No user with name {username}")
                return

        else:
            user = database.models.User.userFromDiscordId(self.bot.db, ctx.author.id)
            if user == None:
                await ctx.send(f"User is not registered!")
                return

        await ctx.send(user.name)
            

