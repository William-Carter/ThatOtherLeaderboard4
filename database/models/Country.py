from Interface import Interface
import Continent

class Country:
    def __init__(self, db: Interface, id, name, continent):
        self.db = db
        self.id = id
        self.name = name
        self.continent = Continent.continent(db, continent)