from database.Interface import Interface

class IndividualLevelCategory:
    def __init__(self, db: Interface, id: int, isExtension: bool, names: list[str]):
        self.db = db
        self.id = id
        self.isExtension = isExtension
        self.names = names
        self.name = names[0]

    def __eq__(self, other):
        return isinstance(other, IndividualLevelCategory) and self.id == other.id
    
    def __hash__(self):
        return hash(self.id)




def individualLevelCategory(db: Interface, id: str) -> IndividualLevelCategory:
    r = db.executeQuery("""
        SELECT id, isExtension
        FROM IndividualLevelCategories
        WHERE id = ?
    """, (id,))

    if len(r) == 0:
        return None
    
    ilCat = r[0]

    r = db.executeQuery("""
        SELECT name
        FROM IndividualLevelCategoryNames
        WHERE category = ?
        ORDER BY isPrimary DESC
    """, (id,))

    names = [x['name'] for x in r]

    return IndividualLevelCategory(db, ilCat['id'], ilCat['isExtension'], names)



def individualLevelCategoryFromName(db: Interface, name: str) -> IndividualLevelCategory:
    r = db.executeQuery("""
        SELECT category
        FROM IndividualLevelCategoryNames
        WHERE name = ?
    """, (name,))

    if len(r) == 0:
        return None
    
    return individualLevelCategory(db, r[0]['id'])


    


