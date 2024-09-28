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


    def getPersonalBests(self) -> dict[Category.Category: FullGameRun.FullGameRun]:
        r = self.db.executeQuery("""
            SELECT fgrc.category, fgr.id, MIN(fgr.time) as time
            FROM FullGameRunCategories fgrc
            LEFT JOIN FullGameRuns fgr ON fgrc.run = fgr.id
            WHERE fgr.user = ?
            GROUP BY fgrc.category
        """, (self.id,))

        pbs = {Category.category(self.db, x['category']): FullGameRun.fullGameRunFromId(self.db, x['id']) for x in r}

        return pbs





def userFromId(db: Interface, id: int) -> User:
    v = db.executeQuery("""
                    SELECT * FROM Users WHERE id = ?"
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


    



