import interactions
import database.leaderboards
import database.models.User
import UI.durations
import UI.neatTables

from database.models import SetupElement
from database.models import UserSetup

class Setup(interactions.Extension):
    @interactions.slash_command(
        name="setup",
        description="See a user's setup",
    )
    @interactions.slash_option(
        name="user",
        argument_name="username",
        description="The user whose setup you wish to see, defaults to yourself if left blank",
        required=False,
        opt_type=interactions.OptionType.STRING
    )

    async def setup(self, ctx: interactions.SlashContext, username: str = None):
        if username:
            userObj = database.models.User.userFromName(self.bot.db, username.lower())
            if userObj == None:
                await ctx.send(f"No user with name {username}")
                return

        else:
            userObj = database.models.User.userFromDiscordId(self.bot.db, ctx.author.id)
            if userObj == None:
                await ctx.send(f"User is not registered!")
                return
            

        setupElements = userObj.getUserSetup()
        if setupElements == None:
            await ctx.send("User has no recorded setup!")
            return
        
        dpiValue = -1
        sensitivity = -1
        tableData = []
        # This is all so wonderfully crap, but setup tracking is so far down the priority list for this project that I don't care
        for element in setupElements:
            if element.element.id == "dpi":
                dpiValue = element.value
            
            if element.element.id == "sensitivity":
                sensitivity = element.value

            tableData.append([element.element.name, str(element.value)])

        if dpiValue != -1 and sensitivity != -1:
            tableData.append(["eDPI", str(dpiValue*sensitivity)])


        output = f"{userObj.name}'s Setup:\n```\n"+UI.neatTables.generateTable(tableData)+"```"

        await ctx.send(output)

