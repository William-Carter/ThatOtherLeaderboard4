import interactions
import UI.neatTables
from database.models import Category
from database import Golds
import UI.durations


class Comgolds(interactions.Extension):
    @interactions.slash_command(
        name="comgolds",
        description="See the community golds",
    )
    @interactions.slash_option(
        name="category",
        argument_name="category",
        description="What category to see the community golds for",
        required=True,
        opt_type=interactions.OptionType.STRING
    )


    async def comgolds(self, ctx: interactions.SlashContext, category: str):
        categoryObj = Category.categoryFromName(self.bot.db, category)
        if categoryObj == None:
            await ctx.send("Invalid category!")
            return
        
        cgolds = Golds.getCommunityGolds(self.bot.db, categoryObj)
        csob = 0
        tableData = [["Level", "Time", "Runner"]]
        for cgold in cgolds:
            csob += cgold[1]
            level = cgold[0].name
            time = UI.durations.formatted(cgold[1])

            # Concatenate if there's multiple runners
            runners = ""
            for runner in cgold[2]:
                runners += ", "
                runners += runner.name
            runners = runners[2:]

            tableData.append([level, time, runners])


        output = f"```ansi\nCommunity Golds for {categoryObj.name.title()}:\n"
        output += UI.neatTables.generateTable(tableData)
        output += f"\nCommunity Sum of Best: {UI.durations.formatted(csob)}```"

        await ctx.send(output)



        

