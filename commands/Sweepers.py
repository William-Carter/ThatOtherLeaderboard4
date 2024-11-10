import interactions
import database.Sweepers
import UI.neatTables
class Sweepers(interactions.Extension):
    @interactions.slash_command(
        name="sweepers",
        description="See how many people have top X in every main category",
    )
    @interactions.slash_option(
        name="top",
        argument_name="top",
        description="Top X",
        required=True,
        opt_type=interactions.OptionType.INTEGER
    )
    

    async def sweepers(self, ctx: interactions.SlashContext, top: int):
        # Sorts list by average rank
        sweepers = sorted(database.Sweepers.getSweepers(self.bot.db, top), key = lambda x: sum(x[1])/len(x[1]))
        output = f"There are {len(sweepers)} people with top {top} in all main categories\n"
        if len(sweepers) > 20:
            output += "Here are the 20 with the highest average rank"

        
        tableData = [["Player", "Average Rank", "Highest Rank"]]
        for sweeper in sweepers[:(min(20, len(sweepers)))]:
            userName = sweeper[0].name
            avgRank = str(round(sum(sweeper[1])/len(sweeper[1]), 2))
            maxRank = str(max(sweeper[1]))
            tableData.append([userName, avgRank, maxRank])
        output += "```" + UI.neatTables.generateTable(tableData) + "```"

        await ctx.send(output)
