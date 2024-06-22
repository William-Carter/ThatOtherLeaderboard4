from Interface import Interface

class Continent:
    def __init__(self, db: Interface, id: str, name: str, descriptor: str):
        self.db = db
        self.id = id
        self.name = name
        self.descriptor = descriptor



def continent(db: Interface, id: str) -> Continent:
    v = db.executeQuery("""
                        SELECT * FROM Continents WHERE id = ?

        """, id)
    
    return Continent(db, v['id'], v['name'], v['descriptor'])