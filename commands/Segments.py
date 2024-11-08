import interactions
import database.models.User
import database.models.Gold
import database.models.Category
import UI.durations
import UI.neatTables
import database.sprm

class Segments(interactions.Extension):
    @interactions.slash_command(
        name="segments",
        description="See a user's PB segments",
    )
    @interactions.slash_option(
        name="category",
        argument_name="category",
        description="What category to ",
        required=True,
        opt_type=interactions.OptionType.STRING
    )

    @interactions.slash_option(
        name="user",
        argument_name="username",
        description="The user whose segments you wish to see. Defaults to yourself if left blank.",
        required=False,
        opt_type=interactions.OptionType.STRING
    )

    async def segments(self, ctx: interactions.SlashContext, category: str, username: str = None):
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
            

        categoryObj = database.models.Category.categoryFromName(self.bot.db, category.lower())

        if categoryObj == None:
            await ctx.send(f"{category.title()} is not a valid category!")
            return
            

        segments = userObj.getPbSegments(categoryObj)
        if segments == None:
            await ctx.send("User has no recorded PB segments")

        tableData = [["Map", "Time"]]
        total = 0
        for row in segments:
            total += row[1]
            tableData.append([row[0].name, UI.durations.formatted(row[1])])

        tableData += [["", ""], ["Total", UI.durations.formatted(total)]]

        output = f"```\n{categoryObj.name.title()} PB Segments for {userObj.name}:\n"
        output += UI.neatTables.generateTable(tableData)
        output += "```"

        await ctx.send(output)


