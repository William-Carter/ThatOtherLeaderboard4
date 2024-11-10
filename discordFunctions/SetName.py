import interactions
import tol

async def updateUserNickname(user: interactions.Member, newName: str):
    if not user.has_role(tol.adminRole): # bot doesn't (and can't) have permissions to edit admin nicknames
        await user.edit_nickname(newName)