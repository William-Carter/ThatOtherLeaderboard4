import interactions
import database.leaderboards
import database.models.User
import database.categories
import tabulate
from database import ilpoints
from UI import durations

class ILProfile(interactions.Extension):
    @interactions.slash_command(
        name="ilprofile",
        description="See a user's IL profile",
    )
    @interactions.slash_option(
        name="user",
        argument_name="username",
        description="The user whose profile you wish to see, defaults to yourself if left blank",
        required=False,
        opt_type=interactions.OptionType.STRING
    )

    async def ilprofile(self, ctx: interactions.SlashContext, username: str = None):
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
            

        data = {}

        pbs = userObj.getILPersonalBests()
        for cat in pbs.keys():
            data[cat] = {}
            data[cat]['points'] = 0
            data[cat]['nonAdvMapsRun'] = 0
            data[cat]['advMapsRun'] = 0
            data[cat]['sumOfRanks'] = 0
            data[cat]['noAdvSoils'] = 0
            data[cat]['totalSoils'] = 0
            for level, run in pbs[cat].items():
                if run == None:
                    continue
                rank = run.getRankInCategory(cat)
                if database.categories.checkILActiveness(self.bot.db, level.id, cat.id):
                    data[cat]['points'] += ilpoints.points(rank)
                data[cat]['sumOfRanks'] += rank

                if level.order < 18:
                    data[cat]['nonAdvMapsRun'] += 1
                    data[cat]['noAdvSoils'] += run.time
                else:
                    data[cat]['advMapsRun'] += 1

                data[cat]["totalSoils"] += run.time


            data[cat]['rank'] = database.leaderboards.getIlPointsRank(self.bot.db, round(data[cat]['points'], 2), cat)

        
        headers = ["Category", "Points", "Rank", "Maps Run", "Avg. Rank", "NoAdv Time", "Total Time"]
        table = []

        totalPoints = 0
        totalMaps = 0
        totalAvg = 0
        totalNoAdv = 0
        total = 0
        for cat in data.keys():
            totalPoints += data[cat]['points']
            totalRuns = data[cat]['nonAdvMapsRun']+data[cat]['advMapsRun']
            totalMaps += totalRuns
            avgRank = data[cat]['sumOfRanks']/totalRuns
            totalAvg += avgRank
            totalNoAdv += data[cat]["noAdvSoils"]
            total += data[cat]["totalSoils"]
            row = [
                cat.name.title(),
                str(round(data[cat]['points'], 0)),
                durations.formatLeaderBoardPosition(data[cat]["rank"], True),
                f"{data[cat]['nonAdvMapsRun']}/18 {data[cat]['advMapsRun']}/6",
                str(round(avgRank, 2)),
                durations.formatted(data[cat]["noAdvSoils"]),
                durations.formatted(data[cat]["totalSoils"])
            ]
            table.append(row)

        table.append(
            [
                "Total",
                str(round(totalPoints, 0)),
                durations.formatLeaderBoardPosition(database.leaderboards.getIlPointsRank(self.bot.db, round(totalPoints, 2)), True),
                f"{totalMaps}/72",
                str(round(totalAvg/len(data.keys()), 2)),
                durations.formatted(totalNoAdv),
                durations.formatted(total)
            ]
        )

        result = tabulate.tabulate(table, headers, "rounded_outline", numalign="left")

        await ctx.send(f"```ansi\n{result}```")
            

