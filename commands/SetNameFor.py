import interactions
import tol
import commandlogic
import commandlogic.SetName
from database.models import User

class SetNameFor(interactions.Extension):
    @interactions.slash_command(
        name="setnamefor",
        description="Update someone else's name on tol",
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
        name="name",
        argument_name="newName",
        description="The name you want to change them to",
        required=True,
        opt_type=interactions.OptionType.STRING,
        min_length=1,
        max_length=20
    )

    async def setnamefor(self, ctx: interactions.SlashContext, username: str, newName: str):
        userObj = User.userFromName(self.bot.db, username)
        if userObj == None:
            await ctx.send(f"No user with name {username}")
            return
        
        await commandlogic.SetName.updateName(self, ctx, userObj, newName)
        
        
            

