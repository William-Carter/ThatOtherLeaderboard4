import interactions
import tol
import discordFunctions.SetName
from database.models import User
class IAm(interactions.Extension):
    @interactions.slash_command(
        name="iam",
        description="Link your discord account to a speedrun.com profile",
        scopes = [tol.homeGuild]
    )

    @interactions.slash_option(
        name="name",
        argument_name="username",
        description="Your speedrun.com username",
        required=True,
        opt_type=interactions.OptionType.STRING
    )

    
    
    async def iam(self, ctx: interactions.SlashContext, username: str):
        oldUserObj = User.userFromDiscordId(self.bot.db, ctx.author.id)
        userObj = User.userFromName(self.bot.db, username)
        if userObj == None:
            await ctx.send("No user with that name!")
            return
        
        if userObj.discordId != None:
            await ctx.send("That account is already linked to someone else!")
            return
        if oldUserObj:
            oldUserObj.updateDiscordId(None)

        userObj.updateDiscordId(str(ctx.author.id))

        await ctx.send("Accounts linked!!")
        await discordFunctions.SetName.updateUserNickname(ctx.author, userObj.name)
        

       
        

