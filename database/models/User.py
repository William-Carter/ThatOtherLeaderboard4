from Interface import Interface
import Country

class User:
    def __init__(self, db: Interface, id: int, name: str, srcId: str, discordId: str, countryId: str):
        self.id = id
        self.name = name
        self.srcId = srcId
        self.discordId = discordId
        self.country = Country.country(db, countryId)


def user(db: Interface, id: int) -> User:
    v = db.executeQuery("""
                    SELECT * FROM Users WHERE id = ?"
                    """, (id,))
    
    return User(db, v['id'], v['name'], v['srcId'], v['discordId'], v['nationality'])

    



