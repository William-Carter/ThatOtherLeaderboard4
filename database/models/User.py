from database.Interface import Interface
from database.models import Country

class User:
    def __init__(self, db: Interface, id: int, name: str, srcId: str, discordId: str, countryId: str):
        self.id = id
        self.name = name
        self.srcId = srcId
        self.discordId = discordId
        self.country = Country.country(db, countryId)


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
                    SELECT * FROM Users WHERE name = ?"
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


    



