from database import Interface
from database import categories
from database import leaderboards
from database.models import User
def getSweepers(db: Interface.Interface, top: int) -> list[User.User|list[int]]:
    mainCats = categories.getMainFullGameCategories(db)
    userPlacements = {}
    for cat in mainCats:
        for entry in leaderboards.getLeaderboard(db, cat.id):
            if not entry[3] in userPlacements.keys():
                userPlacements[entry[3]] = []

            userPlacements[entry[3]].append(entry[2])


    usersWithSweep = []
    for user in userPlacements.keys():
        if len(userPlacements[user]) != len(mainCats):
            continue

        if max(userPlacements[user]) > top:
            continue

        userObj = User.userFromId(db, user)
        usersWithSweep.append([userObj, userPlacements[user]])

     

    return usersWithSweep
        

    

