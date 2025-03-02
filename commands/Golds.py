import interactions
import database.models.User
import database.models.Gold
import UI.durations
import UI.neatTables
import database.sprm

class Golds(interactions.Extension):
    @interactions.slash_command(
        name="golds",
        description="See a user's golds",
    )
    @interactions.slash_option(
        name="category",
        argument_name="category",
        description="What category to see golds for",
        required=True,
        opt_type=interactions.OptionType.STRING
    )

    @interactions.slash_option(
        name="user",
        argument_name="username",
        description="The user whose golds you wish to see. Defaults to yourself if left blank.",
        required=False,
        opt_type=interactions.OptionType.STRING
    )

    async def golds(self, ctx: interactions.SlashContext, category: str, username: str = None):
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
            

        golds = userObj.getGolds(categoryObj)

        if golds == None:
            await ctx.send(f"{userObj.name} hasn't recorded any golds for this category!")
            return

        output = f"```ansi\n{categoryObj.name.title()} golds for {userObj.name}:\n"
        tableData = [["Map", "Time", "Rank"]]
        ineligibleGold = False
        sumOfBest = 0
        for gold in golds:
            position = gold.getRank()
            sumOfBest += gold.time
            if position == -1:
                rank = ""
                ineligibleGold = True
            else:
                rank = UI.durations.formatLeaderBoardPosition(position, colorCode=True)
            tableData.append([
                gold.map.name,
                UI.durations.formatted(gold.time),
                rank
            ])

        tableData.append(["", "", ""])
        tableData.append(["Total", UI.durations.formatted(sumOfBest), ""])
        output += UI.neatTables.generateTable(tableData)
        if ineligibleGold:
            output += "\nGolds without a placement aren't valid for comgold due to differing strats\nUse /eligible to fix any inaccuracies"
        output += "```"

        await ctx.send(output)

        

