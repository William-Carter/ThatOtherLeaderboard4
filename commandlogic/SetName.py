import interactions
from database.models import User
import discordFunctions
import re

import discordFunctions.SetName

async def updateName(command: interactions.Extension, ctx: interactions.SlashContext, userObj: User.User, newName: str, member: interactions.Member = None):
    nameIsValid = re.match('^[a-zA-Z0-9]+$', newName)
    if not nameIsValid:
        await ctx.send("Names can only contain English characters and digits")
        return


    existingUserWithName = User.userFromName(command.bot.db, newName)
    if existingUserWithName:
        await ctx.send("User with that name already exists!")
        return
    

    oldName = userObj.name
    userObj.updateName(newName)

    # If member object wasn't provided, try to fetch it if the user has a discord account linked
    if userObj.discordId and not member:
        member = await ctx.guild.fetch_member(userObj.discordId)

    if member:
        await discordFunctions.SetName.updateUserNickname(member, newName)

    await ctx.send(f"Name updated from {oldName} to {userObj.name}!")


    

    
