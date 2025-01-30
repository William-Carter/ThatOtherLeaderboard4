import interactions
from database.models import User
from database.models import Country

class SetCountryFor(interactions.Extension):
    @interactions.slash_command(
        name="setcountryfor",
        description="Update someone else's nationality on tol",
        scopes=[1081155162065862697]
    )
    @interactions.slash_option(
        name="user",
        argument_name="username",
        description="Whose nationality to update",
        required=True,
        opt_type=interactions.OptionType.STRING
    )

    @interactions.slash_option(
        name="country",
        argument_name="country",
        description="The country you want to change them to",
        required=True,
        opt_type=interactions.OptionType.STRING,
    )

    async def setcountryfor(self, ctx: interactions.SlashContext, username: str, country: str):
        userObj = User.userFromName(self.bot.db, username)
        if userObj == None:
            await ctx.send(f"No user with name {username}")
            return
        
        countryObj = Country.countryFromName(self.bot.db, country)
        if countryObj == None:
            await ctx.send("Invalid country!")
            return
        
        userObj.updateNationality(countryObj)
        await ctx.send(f"Updated nationality to {countryObj.name.title()} for {userObj.name}!")
        
        
            

