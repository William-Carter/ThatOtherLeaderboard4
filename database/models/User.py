from database.Interface import Interface
from database.models import Country
from database.models import FullGameRun
from database.models import Category
from database.models import Map
from database.models import Gold
from database.models import SetupElement
from database.models import UserSetup
class User:
    def __init__(self, db: Interface, id: int, name: str, srcId: str, discordId: str, countryId: str):
        self.db = db
        self.id = id
        self.name = name
        self.srcId = srcId
        self.discordId = discordId
        self.country = Country.country(db, countryId)

    def updateName(self, newName: str):
        """
        Update the user's name in the database
        """

        r = self.db.insertAndFetchRowID(
            """
            UPDATE Users
            SET name = ?
            WHERE id = ?
            """, (newName, self.id))
        
        self.name = newName

    def updateNationality(self, newNationality: Country.Country):
        """
        Update the user's country in the database
        """

        r = self.db.insertAndFetchRowID(
            """
            UPDATE Users
            SET representing = ?
            WHERE id = ?
            """, (newNationality.id, self.id))
        
        self.country = newNationality

    def updateDiscordId(self, newDiscordId: str):
        """
        Update the user's discordId
        """

        r = self.db.insertAndFetchRowID(
            """
            UPDATE Users
            SET discordId = ?
            WHERE id = ?
            """, (newDiscordId, self.id))
        
        self.discordId = newDiscordId



    def getPersonalBests(self) -> dict[Category.Category: FullGameRun.FullGameRun]:
        """
        Get all of the user's personal bests

        Returns:
            A dictionary where the keys are category objects and the values are FullGameRun objects
        """
        r = self.db.executeQuery("""
            SELECT fgrc.category, fgr.id, MIN(fgr.time) as time
            FROM FullGameRunCategories fgrc
            LEFT JOIN FullGameRuns fgr ON fgrc.run = fgr.id
            WHERE fgr.user = ?
            GROUP BY fgrc.category
        """, (self.id,))

        pbs = {Category.category(self.db, x['category']): FullGameRun.fullGameRunFromId(self.db, x['id']) for x in r}

        return pbs
    

    def getPersonalBest(self, category: Category.Category) -> FullGameRun.FullGameRun:
        r = self.db.executeQuery("""
            SELECT fgr.id, MIN(fgr.time) as time
            FROM FullGameRunCategories fgrc
            LEFT JOIN FullGameRuns fgr ON fgrc.run = fgr.id
            WHERE fgr.user = ?
            AND fgrc.category = ?

        """, (self.id, category.id))

        if len(r) == 0:
            return None
        
        return FullGameRun.fullGameRunFromId(self.db, r[0]['id'])



    def getAllRuns(self) -> list[FullGameRun.FullGameRun]:
        response = self.db.executeQuery(
            """
            SELECT fgr.id, fgr.user, fgr.time, fgr.date, fgrc.category, fgrc.submittedAs
            FROM FullGameRuns fgr
            LEFT JOIN FullGameRunCategories fgrc ON fgr.id = fgrc.run
            WHERE fgr.user = ?
            ORDER BY fgr.date DESC
            """, (self.id,))
        
        runs = {}

        for run in response:
            if run['id'] in runs:
                runs[run['id']]['categories'].append([run['category'], run['submittedAs']])
            else:
                runs[run['id']] = {'user': run['user'], 
                                   'time': run['time'], 
                                   'date': run['date'], 
                                   'categories': [[run['category'], run['submittedAs']]]}
            runs[run['id']]


        runObjects = []
        for runId in runs.keys():
            run = runs[runId]
            # Order the categories such that the submitted category is first in the list and extract just the category ids
            categories = [r[0] for r in sorted(run['categories'], key = lambda x: x[1], reverse=True)]
            newRunObject = FullGameRun.FullGameRun(self.db, runId, run['user'], run['time'], run['date'], categories)
            runObjects.append(newRunObject)

        return runObjects
    

    def getMapTimes(self, category: Category.Category, type: str) -> dict[Map.Map: float]:
        r = self.db.executeQuery(
            """
            SELECT MapTimes.map, MapTimes.time
            FROM MapTimes
            LEFT JOIN Maps ON MapTimes.map = Maps.id
            WHERE user = ?
            AND type = ?
            AND category = ?
            ORDER BY Maps.mapOrder
            """,
            (self.id, type, category.id)
        )

        maps = {}
        if len(r) == 0:
            return None
        for row in r:
            maps[Map.map(self.db, row['map'])] = row['time']
        return maps
    
    def getGolds(self, category: Category.Category) -> list[Gold.Gold]:
        r = self.db.executeQuery(
            """
            SELECT Golds.map, Golds.time, cge.eligible
            FROM Golds
            LEFT JOIN Maps ON Golds.map = Maps.id
            LEFT JOIN CommunityGoldEligibility cge
            ON cge.user = Golds.user
            AND cge.category = Golds.category
            AND cge.map = Golds.map
            WHERE Golds.user = ?
            AND Golds.category = ?
            ORDER BY Maps.mapOrder
            """,
            (self.id, category.id)
        )

        if len(r) == 0:
            return None
        golds = []
        for row in r:
            goldMap = Map.map(self.db, row['map'])
            golds.append(Gold.Gold(self.db, self, category, goldMap, row['time'], row['eligible']))

        return golds
        
        
    
    def getSumOfBest(self, category: Category.Category) -> float:
        golds = self.getGolds(category)
        if golds == None:
            return None
        
        return round(sum([gold.time for gold in golds]), 3)
    

    def getPbSegments(self, category: Category.Category) -> list|None:
        pb = self.getPersonalBest(category)
        if pb == None:
            return None
        
        return pb.getSegments()
    

    def getAllRunsButSlow(self, category: Category.Category = None) -> list[FullGameRun.FullGameRun]:
        if not category == None:
            catFilter = f"""WHERE category = "{category.id}" """
        else:
            catFilter = ""

        r = self.db.executeQuery(
            """
            SELECT id, time, category
            FROM (
                SELECT r.id, r.time, rc.category
                FROM FullGameRunCategories rc
                LEFT JOIN FullGameRuns r ON rc.run = r.id
                WHERE r.user = ?
                )
            
            """+catFilter+"\nORDER BY time ASC", (self.id,))
        

        runs = []
        for row in r:
            runs.append(FullGameRun.fullGameRunFromId(self.db, row['id']))

        return runs
    

    def getUserSetup(self) -> list[UserSetup.UserSetup]:
        """
        Fetch a user's recorded setup information

        Returns:
            None if the user has no recorded information

            Otherwise, a list of UserSetup objects
        """
        r = self.db.executeQuery(
            """
            SELECT user, element, value
            FROM UserSetups
            WHERE user = ?
            """, (self.id,))
        
        if len(r) == 0:
            return None
        
        userSetupElements = []
        for row in r:
            element = SetupElement.setupElementFromId(self.db, row["element"])
            userSetupElement = UserSetup.UserSetup(self, element, row["value"])
            userSetupElements.append(userSetupElement)

        return userSetupElements


def userFromId(db: Interface, id: int) -> User:
    v = db.executeQuery("""
                    SELECT * FROM Users WHERE id = ?
                    """, (id,))
    
    if len(v) == 0:
        return None
    
    v = v[0]
    
    return User(db, v['id'], v['name'], v['srcId'], v['discordId'], v['representing'])

def userFromName(db: Interface, name: str) -> User:
    v = db.executeQuery("""
                    SELECT * FROM Users WHERE LOWER(name) = ?
                    """, (name.lower(),))
    
    if len(v) == 0:
        return None
    
    v = v[0]
    
    return User(db, v['id'], v['name'], v['srcId'], v['discordId'], v['representing'])

def userFromDiscordId(db: Interface, discordId: int) -> User:
    v = db.executeQuery("""
                    SELECT * FROM Users WHERE discordId = ?
                    """, (discordId,))
    
    if len(v) == 0:
        return None
    
    v = v[0]
    
    return User(db, v['id'], v['name'], v['srcId'], v['discordId'], v['representing'])

def userFromSrcId(db: Interface, srcId: str) -> User:
    v = db.executeQuery("""
                    SELECT * FROM Users WHERE srcId = ?
                    """, (srcId,))
    
    if len(v) == 0:
        return None
    
    v = v[0]
    
    return User(db, v['id'], v['name'], v['srcId'], v['discordId'], v['representing'])


    



