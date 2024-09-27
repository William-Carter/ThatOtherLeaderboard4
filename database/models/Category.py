from database.Interface import Interface

class Category:
    def __init__(self, db: Interface, id: str, isExtension: bool, names: list[str]):
        self.id = id
        self.isExtension = isExtension
        self.names = names
        self.name = names[0]


def category(db: Interface, id: str) -> Category:
    v = db.executeQuery("""
                        SELECT id, isExtension
                        FROM FullGameCategories
                        WHERE id = ?

        """, (id,))
    
    if len(v) == 0:
        return None
    
    v = v[0]

    q = db.executeQuery("""
                        SELECT name, isPrimary
                        FROM FullGameCategoryNames
                        WHERE category = ?
                        ORDER BY isPrimary DESC
        """, (id,))
    

    names = [x['name'] for x in q]

    
    return Category(db, v['id'], v['isExtension'], names)


def categoryFromName(db: Interface, name: str) -> Category:
    v= db.executeQuery("""
                    SELECT FullGameCategories.id AS ID
                    FROM FullGameCategoryNames
                    LEFT JOIN FullGameCategories on FullGameCategoryNames.category = FullGameCategories.id
                    WHERE FullGameCategoryNames.name = ?
    """, (name,))

    if len(v) == 0:
        return None
    
    id = v[0]['ID']
    return (category(db, id))
    
    