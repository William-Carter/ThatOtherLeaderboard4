import sys
import requests
import json
import UI.durations
from database.Interface import Interface
from database.models import User
from database.models import Map
from database.models import IndividualLevelCategory 
from database import submissions

from SRC.SRCValues import values


categoryIds = {
    "oob": "xw20jzkn",
    "inbounds": "xwdmg4dq",
    "glitchless": "02qoxl7k"
}
categories = {v: k for k, v in categoryIds.items()}

levelIds = {
    "testchmb_a_00": "x5d73q9y",
    "testchmb_a_01": "ykwje09g",
    "testchmb_a_02": "nowo2jd6",
    "testchmb_a_03": "jxd15zwo",
    "testchmb_a_04": "lewpqy9n",
    "testchmb_a_05": "3y9mpz95",
    "testchmb_a_06": "q5wkrv94",
    "testchmb_a_07": "p592o7d6",
    "testchmb_a_08": "329vkqdv",
    "testchmb_a_09": "8xd43q9m",
    "testchmb_a_10": "7xd07mwq",
    "testchmb_a_11": "4rw6npd7",
    "testchmb_a_13": "kn9372d0",
    "testchmb_a_14": "oz986rdl",
    "testchmb_a_15": "krdn05wm",
    "escape_00": "zldyypd3",
    "escape_01": "kn9377d0",
    "escape_02": "oz9867dl",
    "testchmb_a_08_advanced": "xd0kl849",
    "testchmb_a_09_advanced": "rw6qrzgd",
    "testchmb_a_10_advanced": "n93q8rzw",
    "testchmb_a_11_advanced": "z98rexpd",
    "testchmb_a_13_advanced": "rdnory7w",
    "testchmb_a_14_advanced": "ldy1jord"
}
levels = {v: k for k, v in levelIds.items()}

def addUser(db: Interface, user: dict):
    if user['rel'] == "guest": # TOL does not track guest users
        return
    
    userObj = User.userFromSrcId(db, user['id'])
    if userObj:
        # Update the name in the DB if it changes on SRC (only if they aren't registered on TOL because some people use different names there)
        if userObj.name != user['names']['international'] and userObj.discordId == None:
                userObj.updateName(user['names']['international'])
        return
    
    with open("SRC/CountryCodes.json", "r") as f:
        countryCodes = json.load(f)

    if user["location"] == None:
                country = None
    else:
        alpha2 = user["location"]["country"]["code"][:2].upper()
        if not alpha2 in countryCodes.keys(): # SRC supports some "countries" that TOL does not, like antarctica
            country = None
        else:
            country = countryCodes[alpha2].lower()

    print(f"Inserting user named {user['names']['international']}")
    db.insertAndFetchRowID(
        """
        INSERT INTO Users (name, srcId, representing)
        VALUES (?, ?, ?)
        """,
        (user['names']['international'], user['id'], country)
    )
    
def addRun(db: Interface, run: dict):
    runData = run["run"]

    if runData['players'][0]['rel'] == "guest": # TOL does not track runs by guest users
        return
    
    userObj = User.userFromSrcId(db, runData["players"][0]["id"])

    if userObj == None:
         raise Exception("Runner for run not found in db. Did you forget to sync users before syncing runs?")
     
    runTime = runData["times"]["primary_t"]
    runTime = UI.durations.correctToTick(runTime)
    runLevel = levels[runData['level']]
    runCategory = categories[runData['category']]

    existingRuns = db.executeQuery(
        """
        SELECT category, map, time, user
        FROM IndividualLevelRunCategories ilrc
        LEFT JOIN IndividualLevelRuns ilr ON ilrc.run = ilr.id
        WHERE category = ?
        AND map = ?
        AND time = ?
        AND user = ? 
        """,
        (runCategory, runLevel, runTime, userObj.id)
    )
    if len(existingRuns) > 0:
         return # Run already in database
    
    runDate = runData["date"]
    runMapObj = Map.map(db, runLevel)
    runCategoryObj = IndividualLevelCategory.individualLevelCategory(db, runCategory)

    print(f"Inserting {runCategoryObj.name} {runMapObj.name} run of {UI.durations.formatted(runTime)} by {userObj.name}")
    submissions.submitIndividualLevelRun(db, userObj, runTime, runDate, runMapObj, runCategoryObj)


def sync(db: Interface, category: str, map: str):
    response = requests.get(f"https://speedrun.com/api/v1/leaderboards/{values.GAME_PORTAL}/level/{levelIds[map]}/{categoryIds[category]}?embed=players")
    if response.status_code != 200:
        return
    
    data = response.json()['data']

    for user in data['players']['data']:
        addUser(db, user)

    for run in data['runs']:
         addRun(db, run)


if __name__ == "__main__":
    db = Interface("ThatOtherLeaderboard.db")
    if len(sys.argv) != 3:
         raise Exception("Incorrect number of arguments provided")
    
    if not sys.argv[1] in categoryIds.keys():
         raise Exception("Invalid category provided")

    if not sys.argv[2] in levelIds.keys():
         raise Exception("Invalid level provided") 

    sync(db, sys.argv[1], sys.argv[2])
    