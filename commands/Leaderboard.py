import interactions
import database.leaderboards
import database.models.Category
import database.models.Country
import database.models.Continent
import UI.leaderboards
import UI.durations

class Leaderboard(interactions.Extension):
    @interactions.slash_command(
        name="leaderboard",
        description="See the leaderboard for a category",
    )
    @interactions.slash_option(
        name="category",
        argument_name="category",
        description="The category you want to the leaderboard for",
        required=True,
        opt_type=interactions.OptionType.STRING
    )

    @interactions.slash_option(
        name="country",
        argument_name="country",
        description="The country you want to the leaderboard for",
        required=False,
        opt_type=interactions.OptionType.STRING
    )
    @interactions.slash_option(
        name="continent",
        argument_name="continent",
        description="The continent you want to the leaderboard for",
        required=False,
        opt_type=interactions.OptionType.STRING
    )

    async def leaderboard(self, ctx: interactions.SlashContext, category: str = None, country: str = None, continent: str = None):
        if country and continent:
            await ctx.send(f"Can't filter by country and continent at the same time!")
            return


        categoryObj = database.models.Category.categoryFromName(self.bot.db, category.lower())

        if categoryObj == None:
            await ctx.send(f"{category.title()} is not a valid category!")
            return
        
            
        
        if country:
            countryObj = database.models.Country.countryFromName(self.bot.db, country.lower())
            if countryObj == None:
                await ctx.send(f"{country.title()} is not a valid country!")
                return

            header = f"Leaderboard for {categoryObj.name.title()} in {countryObj.name.title()}:\n"
            dbData = database.leaderboards.getCountryLeaderboard(self.bot.db, categoryObj.id, countryObj.id)
        

        elif continent:
            continentObj = database.models.Continent.continentFromName(self.bot.db, continent.lower())
            if continentObj == None:
                await ctx.send(f"{continent.title()} is not a valid continent!")
                return


            header = f"Leaderboard for {categoryObj.name.title()} in {continentObj.name.title()}:\n"
            dbData = database.leaderboards.getContinentLeaderboard(self.bot.db, categoryObj.id, continentObj.id)

        else:
            header = f"Leaderboard for {categoryObj.name.title()}:\n"
            dbData = database.leaderboards.getLeaderboard(self.bot.db, categoryObj.id)

        formatted = [[x[0], UI.durations.formatted(x[1])] for x in dbData]
        lb = UI.leaderboards.Leaderboard(["Runner", "Time"], formatted, 1)
        
        response = header + lb.getDiscordFormattedMessage()
        await ctx.send(response)
            

