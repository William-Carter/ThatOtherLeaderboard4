import interactions
import UI.differences
from database import Golds
from database import Maps
from database.models import Category
from database.models import User
from database.models import FullGameRun
import UI.durations
import UI.neatTables

class Compare(interactions.Extension):

    @interactions.slash_command(
        name="compare",
        description="Compare stuff",
        sub_cmd_name="segments",
        sub_cmd_description="Compare two sets of segments to each other"
    )
    @interactions.slash_option(
        name="category",
        argument_name="category1",
        description="The category to compare in",
        required=True,
        opt_type=interactions.OptionType.STRING
    )


    @interactions.slash_option(
        name="first-type",
        argument_name="type1",
        description="The type of the first segment set.",
        required=True,
        opt_type=interactions.OptionType.STRING,
        choices = [
            interactions.SlashCommandChoice("Golds", "golds"),
            interactions.SlashCommandChoice("PB", "pb"),
            interactions.SlashCommandChoice("Run", "run")
        ]
    )

    @interactions.slash_option(
        name="first-user",
        argument_name="user1",
        description="The name of the first user ('*' for comgolds)",
        required=True,
        opt_type=interactions.OptionType.STRING
    )

    @interactions.slash_option(
        name="second-type",
        argument_name="type2",
        description="The type of the second segment set.",
        required=True,
        opt_type=interactions.OptionType.STRING,
        choices = [
            interactions.SlashCommandChoice("Golds", "golds"),
            interactions.SlashCommandChoice("PB", "pb"),
            interactions.SlashCommandChoice("Run", "run")
        ]
    )

    @interactions.slash_option(
        name="second-user",
        argument_name="user2",
        description="The name of the second user ('*' for comgolds)",
        required=True,
        opt_type=interactions.OptionType.STRING
    )

    @interactions.slash_option(
        name="second-category",
        argument_name="category2",
        description="A differing category for the second comparison. If you want that. For some reason.",
        required=False,
        opt_type=interactions.OptionType.STRING
    )

    async def compareSegments(self, 
                              ctx: interactions.SlashContext, 
                              type1: str, user1: str, category1: str, 
                              type2: str, user2: str, category2: str = None):
        
        if category2 == None:
            category2 = category1



        comparisons = [
            [type1, user1, category1],
            [type2, user2, category2]
        ]

        # Will populate with {"header": str, "segments": [[Map, Float],...]} for each comparison
        segmentSets = []

        for comparison in comparisons:
            cType = comparison[0]
            cUser = comparison[1]
            cCategory = comparison[2]

            categoryObj = Category.categoryFromName(self.bot.db, cCategory)
            if categoryObj == None:
                await ctx.send(f"No category named {cCategory}!")
                return


            match cType:
                case "golds":
                    if cUser == "*":
                        header = f"{categoryObj.name.title()} Comgolds"
                        cgoldOutput = Golds.getCommunityGolds(self.bot.db, categoryObj)
                        segments = [[x[0], x[1]] for x in cgoldOutput] # Remove runner, we don't need them for comparing
                        segmentSets.append({"header": header, "segments": segments})
                    else:
                        userObj = User.userFromName(self.bot.db, cUser)
                        if userObj == None:
                            await ctx.send(f"No user with name {cUser}!")
                            return
                        
                        header = f"{userObj.name} Golds"
                        segments = [[x.map, x.time] for x in userObj.getGolds(categoryObj)]
                        segmentSets.append({"header": header, "segments": segments})

                case "pb":
                    userObj = User.userFromName(self.bot.db, cUser)
                    if userObj == None:
                            await ctx.send(f"No user with name {cUser}!")
                            return

                    segments = userObj.getPbSegments(categoryObj)
                    if segments == None:
                        await ctx.send(f"{userObj.name.capitalize()} has no segments recorded for their pb!")
                        return
                    
                    header = f"{userObj.name} PB"
                    
                    segmentSets.append({"header": header, "segments": segments})

                case "run":
                    run = FullGameRun.fullGameRunFromId(self.bot.db, cUser)
                    if run == None:
                        await ctx.send(f"No run with id {cUser}!")
                        return
                    header = f"Run {run.id}"

                    segments = run.getSegments()
                    if segments == None:
                        await ctx.send(f"Run with id {cUser} has no recorded segments!")

                    segmentSets.append({"header": header, "segments": segments})


        
        maps = Maps.getMainLevels(self.bot.db)
        columns = [["Map"]+[map.name for map in maps]+["Total"]]


        for segmentSet in segmentSets:
            total = sum([x[1] for x in segmentSet["segments"]])
            segmentSet["segments"].append([None, total])

        sortedSegmentSets = sorted(segmentSets, key = lambda x: x["segments"][-1])
        


        standard = [x[1] for x in sortedSegmentSets[0]["segments"]] # List of floats for the fastest of the segment sets

        for index, segmentSet in enumerate(sortedSegmentSets):
            column = [segmentSet["header"]]
            if index == 0:
                segments = []
                for segment in segmentSet["segments"]:
                    segments.append(UI.durations.formatted(segment[1]))


            else:
                segments = []
                for i, segment in enumerate(segmentSet["segments"]):
                    timeStr = UI.durations.formatted(segment[1])
                    timeStr += " "*(max(9-len(timeStr), 1)) # Make all the comparisons lined up 

                    segments.append(
                        timeStr + f"({UI.differences.colourDifference(standard[i]-segment[1])})"
                    )

            columns.append(column+segments)


        rows = list(zip(*columns))

        await ctx.send("```ansi\n"+UI.neatTables.generateTable(rows)+"```")