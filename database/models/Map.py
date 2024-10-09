from database.Interface import Interface

class Map:
    def __init__(self, db: Interface, id: str, order: int, names: list[str]):
        self.db = db
        self.id = id
        self.order = order
        self.names = names
        self.name = names[0]
        


def map(db: Interface, id: str) -> Map:
    v = db.executeQuery("""
                        SELECT id, mapOrder
                        FROM Maps
                        WHERE id = ?
        """, (id,))
    
    if len(v) == 0:
        return None
        
    v = v[0]

    q = db.executeQuery("""
                        SELECT name
                        FROM MapNames
                        WHERE map = ?
                        ORDER BY isPrimary DESC
        """, (v['id'],))
    
    names = [x['name'] for x in q]
    
    return Map(db, v['id'], v['mapOrder'], names)


def mapFromName(db: Interface, name: str) -> Map:
    v = db.executeQuery("""
                        SELECT map as ID
                        FROM MapNames
                        WHERE name = ?
    """, (name,))

    if len(v) == 0:
        return None
    
    id = v[0]['ID']
    return (map(db, id))


