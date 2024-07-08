from Interface import Interface
import Continent

class Country:
    def __init__(self, db: Interface, id: int, name: str, continent: str):
        self.db = db
        self.id = id
        self.name = name
        self.continent = Continent.continent(db, continent)


def country(db: Interface, id: str) -> Country:
    v = db.executeQuery("""
                        SELECT * FROM Countries WHERE id = ?
        """, id)[0]
    
    return Country(db, v['id'], v['name'], v['continent'])