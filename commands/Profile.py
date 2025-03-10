import interactions
import UI.differences
import database.leaderboards
import database.models.User
import UI.durations
import UI.neatTables
import database.sprm
import database.AMC

class Profile(interactions.Extension):
    @interactions.slash_command(
        name="profile",
        description="See a user's profile",
    )
    @interactions.slash_option(
        name="user",
        argument_name="username",
        description="The user whose profile you wish to see, defaults to yourself if left blank",
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
        data = [[UI.differences.underline(header) for header in ["Category", "Time", "SPRM", "WR", "CR", "NR"]]]
        
        profilePbCount = 0

        for category in userPersonalBests.keys():
            if not category.isExtension:
                profilePbCount += 1
                run = userPersonalBests[category]
                
                sprm = database.sprm.calculateSprm(self.bot.db, category, run.time)
                globalRank = UI.durations.formatLeaderBoardPosition(run.getRankInCategory(category), True)
                if userObj.country:
                    countryRank = UI.durations.formatLeaderBoardPosition(
                        run.getRankInCategoryInCountry(category, userObj.country), True
                        )
                    
                    continentRank = UI.durations.formatLeaderBoardPosition(
                        run.getRankInCategoryInContinent(category, userObj.country.continent), True
                        )
                else:
                    countryRank = ""
                    continentRank = ""

                

                data.append([UI.differences.underline(category.name.title()), 
                             UI.durations.formatted(run.time),
                             str(int(round(sprm, 0))),
                             globalRank,
                             continentRank,
                             countryRank
                             ])

        amcResult = database.AMC.getAmc(self.bot.db, userObj)
        if amcResult:
            amcTime, amcRank = amcResult

        avgResult = database.leaderboards.getAverageRank(self.bot.db, userObj)
        if avgResult:
            avgRank, avgRankRank = avgResult

        sprmResult = database.sprm.getSprmPlacement(self.bot.db, userObj)
        if sprmResult:
            sprmSum, sprmPlacement = sprmResult

        response = f"```ansi\n{UI.differences.underline(f'Profile for {userObj.name}:')}"


        response += "\n"+UI.neatTables.generateTable(data, padding=3)

        if amcResult:
            response += f"\n{UI.differences.underline('AMC Summary:')}  {UI.durations.formatted(amcTime)} ({UI.durations.formatLeaderBoardPosition(amcRank, True)})"
        if avgResult:
            response += f"\n{UI.differences.underline('Average Rank:')} {avgRank} ({UI.durations.formatLeaderBoardPosition(avgRankRank, True)})"

        if sprmResult:
            response += f"\n{UI.differences.underline('Overall SPRM:')} {int(round(sprmSum, 0))} ({UI.durations.formatLeaderBoardPosition(sprmPlacement, True)})"

        if userObj.country:
            response += UI.differences.underline(f"\n\nRepresenting {userObj.country.name.title()}")

        response += "```"

                

        await ctx.send(response)
            

