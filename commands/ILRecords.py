import interactions
import UI.durations
from UI import ILsheet
from database.models import User
from database.models import IndividualLevelCategory as ilc
from database import leaderboards
from database import Maps
import tabulate

class ILRecords(interactions.Extension):
    @interactions.slash_command(
        name="ilwrs",
        description="View all the IL world records for a category"
    )
    @interactions.slash_option(
        name="category",
        argument_name="category",
        description="The category you wish to see world records for",
        required=True,
        opt_type=interactions.OptionType.STRING
    )

    async def ilwrs(self, ctx: interactions.SlashContext, category: str = None):
        categoryObj = ilc.individualLevelCategoryFromName(self.bot.db, category)
        if categoryObj == None:
            await ctx.send("Invalid category!")
            return
        
        wrs = leaderboards.getIlWorldRecords(self.bot.db)[categoryObj]

        headers = ["Map", "Record", "Runners"]
        runners = []
        maps = []
        records = []
        noAdvTotal = 0
        totalTime = 0

        for level, wr in wrs.items():
            if level.order < 18:
                noAdvTotal += wr['time']
            totalTime += wr['time']

            maps.append([level.name])
            runnerStr = ""
            for runner in wr["runners"]:
                runnerStr += f", {runner.name}"
            
            runnerStr = runnerStr[2:]

            records.append([UI.durations.formatted(wr["time"])])
            runners.append([runnerStr])

        maps += [["-"], ["NoAdv"], ["Total"]]
        records += [["-"], [UI.durations.formatted(noAdvTotal)], [UI.durations.formatted(totalTime)]]
        runners += [["-"], [""], [""]]


        table = ILsheet.generateSheet(headers, [maps, records, runners])
        await ctx.send(f"World Records for {categoryObj.name.title()}\n```\n"+table+"```")




        