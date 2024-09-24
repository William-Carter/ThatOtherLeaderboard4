from database.Interface import Interface

class Continent:
    def __init__(self, db: Interface, id: str, names: list[str]):
        self.db = db
        self.id = id
        self.names = names
        self.name = names[0]


def continent(db: Interface, id: str) -> Continent:
    v = db.executeQuery("""
                        SELECT id
                        FROM Continents
                        WHERE id = ?
        """, (id,))
    
    if len(v) == 0:
        return None
    
    v = v[0]

    q = db.executeQuery("""
                        SELECT name
                        FROM ContinentNames
                        WHERE continent = ?
                        ORDER BY isPrimary DESC
        """, (v['id'],))
    
    names = [x['name'] for x in q]

    
    return Continent(db, v['id'], names)



def continentFromName(db: Interface, name: str) -> Continent:
    v= db.executeQuery("""
                    SELECT continent AS ID
                    FROM ContinentNames
                    WHERE name = ?
    """, (name,))

    if len(v) == 0:
        return None
    
    id = v[0]['ID']
    return (continent(db, id))