import requests
from database import Interface
from database import submissions
from database.models import User
from database.models import Category
from SRC.SRCValues import values
import UI.durations
import json

def downloadRuns(db: Interface.Interface) -> dict:
    """
    Download runs for every category
    
    Returns:
        A dict in the form {Category: {srcLeaderboardData}}
    """

    leaderboards = {}

    # Glitchless
    print("Fetching Glitchless")
    glitchlessLeaderboard = requests.get(
        f"https://www.speedrun.com/api/v1/leaderboards/{values.GAME_PORTAL}/category/{values.CATEGORY_GLITCHLESS}?embed=players"
        ).json()
    
    glitchlessObj = Category.category(db, "glitchless")
    leaderboards[glitchlessObj] = glitchlessLeaderboard

    # Legacy
    print("Fetching Legacy")
    legacyLeaderboard = requests.get(
        f"https://www.speedrun.com/api/v1/leaderboards/{values.GAME_PORTAL}/category/{values.CATEGORY_NOSLA}?var-{values.VARIABLE_UNR_OR_LEG}={values.VALUE_UNR_OR_LEG_LEGACY}&embed=players"
        ).json()
    
    legacyObj = Category.category(db, "legacy")
    leaderboards[legacyObj] = legacyLeaderboard

    #Unrestricted
    print("Fetching Unrestricted")
    unrestrictedLeaderboard = requests.get(
        f"https://www.speedrun.com/api/v1/leaderboards/{values.GAME_PORTAL}/category/{values.CATEGORY_NOSLA}?var-{values.VARIABLE_UNR_OR_LEG}={values.VALUE_UNR_OR_LEG_UNRESTRICTED}&embed=players"
        ).json()
    
    unrestrictedObj = Category.category(db, "unrestricted")
    leaderboards[unrestrictedObj] = unrestrictedLeaderboard

    # Inbounds
    print("Fetching Inbounds")
    inboundsLeaderboard = requests.get(
        f"https://www.speedrun.com/api/v1/leaderboards/{values.GAME_PORTAL}/category/{values.CATEGORY_INBOUNDS}?embed=players"
        ).json()
    
    inboundsObj = Category.category(db, "inbounds")
    leaderboards[inboundsObj] = inboundsLeaderboard

    # Out of Bounds
    print("Fetching Out of Bounds")
    oobLeaderboard = requests.get(
        f"https://www.speedrun.com/api/v1/leaderboards/{values.GAME_PORTAL}/category/{values.CATEGORY_OOB}?embed=players"
        ).json()
    
    oobObj = Category.category(db, "oob")
    leaderboards[oobObj] = oobLeaderboard


    return leaderboards


def main():
    with open("SRC/CountryCodes.json", "r") as f:
        countryCodes = json.load(f)

    db = Interface.Interface("ThatOtherLeaderboard.db")
    leaderboards = downloadRuns(db)
    for categoryObj in leaderboards.keys():
        data = leaderboards[categoryObj]
        for player in data["data"]["players"]["data"]:
            if player["rel"] == "guest":
                continue
            id = player["id"]

            name = player["names"]["international"]
            if player["location"] == None:
                country = None
            else:
                alpha2 = player["location"]["country"]["code"][:2].upper()
                if not alpha2 in countryCodes.keys():
                    country = None
                else:
                    country = countryCodes[alpha2].lower()


            userObj = User.userFromSrcId(db, id)
            if userObj == None:
                db.insertAndFetchRowID("""
                    INSERT INTO Users (name, srcId, representing)
                    VALUES (?, ?, ?)
                """, (name, id, country))
                print(f"Added new user {name}")

            if userObj.discordId == None: 
                if userObj.name != name:
                    userObj.updateName(name)

        for run in data["data"]["runs"]:
            runData = run["run"]
            runTime = runData["times"]["primary_t"]
            runTime = UI.durations.correctToTick(runTime)
            runDate = runData["date"]
            if runData["players"][0]["rel"] == "guest":
                continue
            userObj = User.userFromSrcId(db, runData["players"][0]["id"])
            
            existingRuns = db.executeQuery(
                """
                SELECT category, time, user
                FROM FullGameRunCategories fgrc
                LEFT JOIN FullGameRuns fgr ON fgrc.run = fgr.id
                WHERE user = ?
                AND category = ?
                AND submittedAs = 1
                """, (userObj.id, categoryObj.id)
            )

            duplicate = False
            for existingRun in existingRuns:
                if existingRun["time"] == runTime:
                    duplicate = True
                    break

            if not duplicate:
                print(f"Inserting {categoryObj.name.title()} run of {UI.durations.formatted(runTime)} by {userObj.name}")
                submissions.submitFullGameRun(db, userObj, runTime, runDate, categoryObj)

            


            




if __name__ == "__main__":
    main()

