import interactions
import commandlogic
import commandlogic.SetName
from database.models import User

class SetName(interactions.Extension):
    @interactions.slash_command(
        name="setname",
        description="Update your name on tol",
        scopes=[1081155162065862697]
    )

    @interactions.slash_option(
        name="name",
        argument_name="name",
        description="The name you want to change to",
        required=True,
        opt_type=interactions.OptionType.STRING,
        min_length=1,
        max_length=20
    )

    async def setname(self, ctx: interactions.SlashContext, name: str):
        userObj = User.userFromDiscordId(self.bot.db, ctx.author.id)
        if userObj == None:
            ctx.send("User is not registered!")
            return
        
        
        await commandlogic.SetName.updateName(self, ctx, userObj, name, ctx.author)
        
        
            

