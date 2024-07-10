from database.Interface import Interface

class Continent:
    def __init__(self, db: Interface, id: str, name: str):
        self.db = db
        self.id = id
        self.name = name



def continent(db: Interface, id: str) -> Continent:
    v = db.executeQuery("""
                        SELECT Continents.id, ContinentNames.name
                        FROM ContinentNames
                        LEFT JOIN Continents ON ContinentNames.continent = Continents.id
                        WHERE ContinentNames.isPrimary = 1
                        AND Continents.id = ?

        """, (id,))
    
    if len(v) == 0:
        return None
    
    v = v[0]
    
    return Continent(db, v['id'], v['name'])