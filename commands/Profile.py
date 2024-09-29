import interactions
import database.models.User
import UI.durations
import UI.neatTables
import database.sprm

class Profile(interactions.Extension):
    @interactions.slash_command(
        name="profile",
        description="See a user's profile",
    )
    @interactions.slash_option(
        name="user",
        argument_name="username",
        description="The user whose profile you wish to see",
        required=False,
        opt_type=interactions.OptionType.STRING
    )

    async def profile(self, ctx: interactions.SlashContext, username: str = None):
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


        userPersonalBests = userObj.getPersonalBests()
        data = [["Category", "Time", "SPRM", "WR", "CR", "NR"]]
        amcSum = 0
        avgRank = 0
        sprmSum = 0
        profilePbCount = 0

        for category in userPersonalBests.keys():
            if not category.isExtension:
                profilePbCount += 1
                run = userPersonalBests[category]
                
                sprm = database.sprm.calculateSprm(self.bot.db, category, run.time)
                globalRank = run.getRankInCategory(category)
                countryRank = run.getRankInCategoryInCountry(category, userObj.country)
                continentRank = run.getRankInCategoryInContinent(category, userObj.country.continent)

                avgRank += globalRank
                amcSum += run.time
                sprmSum += sprm
                

                data.append([category.name.title(), 
                             UI.durations.formatted(run.time),
                             str(int(round(sprm, 0))),
                             UI.durations.formatLeaderBoardPosition(globalRank, True),
                             UI.durations.formatLeaderBoardPosition(continentRank, True),
                             UI.durations.formatLeaderBoardPosition(countryRank, True)
                             ])
                
        avgRank = round(avgRank/profilePbCount, 2)
        response = f"```ansi\nProfile for {userObj.name}"


        response += "\n"+UI.neatTables.generateTable(data, padding=3)

        response += f"\nAMC Summary:  {UI.durations.formatted(amcSum)}"
        response += f"\nAverage Rank: {avgRank}"
        response += f"\nOverall SPRM: {int(round(sprmSum, 0))}"

        response += f"\n\nRepresenting {userObj.country.name.title()}"

        response += "```"

                

        await ctx.send(response)
            

