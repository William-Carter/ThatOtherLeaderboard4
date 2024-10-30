import interactions
from database.models import User
from database.models import Category
from database.models import Map

async def Eligible(command: interactions.Extension, ctx: interactions.SlashContext, userObj: User.User, category: str, map: str):
    categoryObj = Category.categoryFromName(command.bot.db, category)
    if categoryObj == None:
        await ctx.send("Invalid category!")
        return
    
    mapObj = Map.mapFromName(command.bot.db, map)
    if mapObj == None:
        await ctx.send("Invalid map!")
        return
    
    golds = userObj.getGolds(categoryObj)
    if golds == None:
        await ctx.send("User has no recorded golds!")
        return
    

    
    for gold in golds:
        if gold.category == categoryObj and gold.map == mapObj:
            goldObj = gold
            break
    

    outcome = goldObj.toggleEligible()

    if outcome:
        await ctx.send(f"Your {categoryObj.name.title()} {mapObj.name} gold is now eligible for comgold!")

    else:
        await ctx.send(f"Your {categoryObj.name.title()} {mapObj.name} gold is no longer eligible for comgold!")


