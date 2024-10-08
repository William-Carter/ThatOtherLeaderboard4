from database.Interface import Interface
from database.models import Country
from database.models import FullGameRun
from database.models import Category
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
                    """, (name,))
    
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


    



