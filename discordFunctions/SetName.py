import interactions
import tol

async def updateUserNickname(user: interactions.Member, newName: str):
    if not user.has_role(tol.adminRole):
        await user.edit_nickname(newName)