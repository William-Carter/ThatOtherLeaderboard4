import interactions
import UI.durations
import UI.neatTables
import database.leaderboards
import database.sprm
from database.models import Category
from database.models import Country
from database.models import Continent
from database.models import User
class Records(interactions.Extension):
    @interactions.slash_command(
        name="records",
        description="See the records for categories",
    )

    @interactions.slash_option(
        name="country",
        argument_name="country",
        description="Which country to see the records for",
        required=False,
        opt_type=interactions.OptionType.STRING
    )

    @interactions.slash_option(
        name="continent",
        argument_name="continent",
        description="Which continent to see the records for",
        required=False,
        opt_type=interactions.OptionType.STRING
    )  

    @interactions.slash_option(
        name="include-extensions",
        argument_name="extensions",
        description="Whether to include category extensions",
        required=False,
        opt_type=interactions.OptionType.BOOLEAN
    )
    
    
    async def records(self, ctx: interactions.SlashContext, country: str = None, continent: str = None, extensions: bool = False):
        if country and continent:
            await ctx.send("Can only show country or continent records at a time!")
            return
        
        if country:
            
            countryObj = Country.countryFromName(self.bot.db, country)
            if countryObj == None:
                await ctx.send("Invalid country!")
                return
            
            header = f"Records for {countryObj.name.title()}\n" 
            records = database.leaderboards.getCountryRecords(self.bot.db, countryObj, extensions)

        elif continent:
            continentObj = Continent.continentFromName(self.bot.db, continent)
            if continentObj == None:
                await ctx.send("Invalid continent!")
                return
            header = f"Records for {continentObj.name.title()}\n"
            records = database.leaderboards.getContinentRecords(self.bot.db, continentObj, extensions)

        else:
            header = f"World Records\n"
            records = database.leaderboards.getWorldRecords(self.bot.db, extensions)


        tableData = [["Category", "Time", "Player"]]
        for category in records.keys():
            run = records[category]
            timeStr = UI.durations.formatted(run.time)
            userObj = User.userFromId(self.bot.db, run.userId)
            tableData.append([category.name.title(), timeStr, userObj.name])


        await ctx.send("```"+header+UI.neatTables.generateTable(tableData)+"```")

        

