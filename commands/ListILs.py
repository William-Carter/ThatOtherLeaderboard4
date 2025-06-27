import interactions
import UI.neatTables
import database.models.Map
import database.models.User
import math
import UI.durations

class ListILs(interactions.Extension):
    @interactions.slash_command(
        name="listils",
        description="List every IL run on record for a given user",
    )

    @interactions.slash_option(
        name="user",
        argument_name="username",
        description="The user whose runs you want to list, defaults to yourself",
        required=False,
        opt_type=interactions.OptionType.STRING
    )

    @interactions.slash_option(
        name="page",
        argument_name="page",
        description="Which page to show (each page contains 20 runs)",
        required=False,
        opt_type=interactions.OptionType.INTEGER
    )

    async def listils(self, ctx: interactions.SlashContext, username: str = None, page = 1):
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

        runs = userObj.getILRuns()

        pageLength = 20
        maxPage = math.ceil(len(runs) / pageLength)
        page = min(page, maxPage)

        startIndex = pageLength * (page-1)
        endIndex = startIndex + pageLength
        runs = runs[startIndex:endIndex]
        

        tableData = [[str(run.id), run.categories[0], database.models.Map.map(self.bot.db, run.mapId).name, UI.durations.formatted(run.time), run.date] for run in runs]
        tableData = [["ID", "Category", "Map", "Time", "Date"]] + tableData

        response = f"```\nIL Runs for {userObj.name}:\n{UI.neatTables.generateTable(tableData)}\nPage {page} of {maxPage}```"

        await ctx.send(response)
        
