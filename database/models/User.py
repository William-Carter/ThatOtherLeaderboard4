from Interface import Interface

class User:
    def __init__(self, db: Interface, id: int, name: str, srcID: str, discordID: str, nationality: str):
        self.id = id
        self.name = name
        self.srcID = srcID
        self.discordID = discordID
        self.nationality = nationality


def user(db: Interface, id: int) -> User:
    v = db.executeQuery("""
                    SELECT * FROM Users WHERE id = ?"
                    """, (id,))
    
    return User(db, v['id'], v['name'], v['srcID'], v['discordID'], v['nationality'])

    



