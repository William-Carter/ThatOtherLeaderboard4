import interactions
import UI.durations
import UI.ILsheet
import database.models.User
from database import leaderboards
from database import Maps

class ILPBs(interactions.Extension):
    @interactions.slash_command(
        name="ilpbs",
        description="View all of a user's IL PBs"
    )
    @interactions.slash_option(
        name="user",
        argument_name="username",
        description="The user whose IL PBs you wish to see, defaults to yourself if left blank",
        required=False,
        opt_type=interactions.OptionType.STRING
    )

    async def ilpbs(self, ctx: interactions.SlashContext, username: str = None):
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
            
        
        pbs = userObj.getILPersonalBests()
        headers = ["Map"]
        data = [[]]
        for map in Maps.getMainLevels(self.bot.db, True):
            data[0].append([map.name,])

        data[0] += [["-"], ["NoAdv"], ["Total"]]

        for cat in pbs.keys():
            headers.append(cat.name.title())
            column = []
            runningTotal = 0
            mapsTotal = 0
            noAdvTotal = 0
            noAdvMapsTotal = 0
            for map in pbs[cat].keys():
                pb = pbs[cat][map]
                if pb != None:
                    rank = pb.getRankInCategory(cat)
                    column.append([UI.durations.formatted(pb.time), UI.durations.formatLeaderBoardPosition(rank)])
                    runningTotal += pb.time
                    mapsTotal += 1
                    if map.order <= 17:
                        noAdvTotal += pb.time
                        noAdvMapsTotal += 1
                else:
                    column.append([""])


            if mapsTotal == 24:
                rank = leaderboards.getSumOfIlsRank(self.bot.db, cat, runningTotal, True)
                totalRow = [UI.durations.formatted(runningTotal), UI.durations.formatLeaderBoardPosition(rank)]
            else:
                totalRow = [""]

            if noAdvMapsTotal == 18:
                rank = leaderboards.getSumOfIlsRank(self.bot.db, cat, noAdvTotal, False)
                noAdvTotalRow = [UI.durations.formatted(noAdvTotal), UI.durations.formatLeaderBoardPosition(rank)]
            else:
                noAdvTotalRow = [""]

            column += [["-"], noAdvTotalRow, totalRow] # TODO add rank for sum of ils
            data.append(column)

        
        output = f"```Personal Bests for {userObj.name}:\n"+UI.ILsheet.generateSheet(headers, data)+"```"

        await ctx.send(output)




        