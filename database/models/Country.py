from database.Interface import Interface
from database.models import Continent

class Country:
    def __init__(self, db: Interface, id: int, names: list[str], continent: str):
        self.db = db
        self.id = id
        self.names = names
        self.name = names[0]
        self.continent = Continent.continent(db, continent)


def country(db: Interface, id: str) -> Country:
    v = db.executeQuery("""
                        SELECT id, continent
                        FROM Countries
                        WHERE id = ?
        """, (id,))
    
    if len(v) == 0:
        return None
        
    v = v[0]

    q = db.executeQuery("""
                        SELECT name
                        FROM CountryNames
                        WHERE country = ?
                        ORDER BY isPrimary DESC
        """, (v['id'],))
    
    names = [x['name'] for x in q]
    
    return Country(db, v['id'], names, v['continent'])


def countryFromName(db: Interface, name: str) -> Country:
    v = db.executeQuery("""
                        SELECT country as ID
                        FROM CountryNames
                        WHERE name = ?
    """, (name,))

    if len(v) == 0:
        return None
    
    id = v[0]['ID']
    return (country(db, id))


