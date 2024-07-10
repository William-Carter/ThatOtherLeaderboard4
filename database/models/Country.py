from database.Interface import Interface
from database.models import Continent

class Country:
    def __init__(self, db: Interface, id: int, name: str, continent: str):
        self.db = db
        self.id = id
        self.name = name
        self.continent = Continent.continent(db, continent)


def country(db: Interface, id: str) -> Country:
    v = db.executeQuery("""
                        SELECT Countries.id, CountryNames.name, Countries.continent
                        FROM CountryNames
                        LEFT JOIN Countries ON CountryNames.country = Countries.id
                        WHERE CountryNames.isPrimary = 1
                        AND Countries.id = ?
        """, (id,))
    
    if len(v) == 0:
        return None
    
    v = v[0]
    
    return Country(db, v['id'], v['name'], v['continent'])