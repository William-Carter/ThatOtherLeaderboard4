from database.Interface import Interface
from database.models.Category import Category
from database.models.Country import Country
from database.models.Continent import Continent
from database.models import Map
class FullGameRun:
    def __init__(self, db: Interface, id: int, userId: int, time: float, date: str, categories: list[str]):
        self.db = db
        self.id = id
        self.userId = userId
        self.time = time
        self.date = date
        self.categories = categories

    def __str__(self):
        return f"{self.id} - {self.userId} - {self.time} - {self.date} - {self.categories[0]}"

    def getRankInCategory(self, category: Category) -> int:
        rank = self.db.executeQuery("""
            SELECT calculatedRank
            FROM (
                SELECT fgrc.run, MIN(fgr.time), RANK() OVER (ORDER BY MIN(fgr.time) ASC) AS calculatedRank
                FROM FullGameRunCategories fgrc
                LEFT JOIN FullGameRuns fgr ON fgrc.run = fgr.id
                WHERE fgrc.category = ?
                GROUP BY fgr.user
                )
            WHERE run = ?
        """, (category.id, self.id))

        return rank[0]['calculatedRank']
    

    def getRankInCategoryInCountry(self, category: Category, country: Country) -> int:
        rank = self.db.executeQuery("""
            SELECT calculatedRank
            FROM (
                SELECT fgrc.run, MIN(fgr.time), RANK() OVER (ORDER BY MIN(fgr.time) ASC) AS calculatedRank
                FROM FullGameRunCategories fgrc
                LEFT JOIN FullGameRuns fgr ON fgrc.run = fgr.id
                LEFT JOIN Users on fgr.user = Users.id
                WHERE fgrc.category = ?
                AND Users.representing = ?
                GROUP BY fgr.user
                )
            WHERE run = ?
        """, (category.id, country.id, self.id))

        return rank[0]['calculatedRank']
    

    def getRankInCategoryInContinent(self, category: Category, continent: Continent) -> int:
        rank = self.db.executeQuery("""
            SELECT calculatedRank
            FROM (
                SELECT fgrc.run, MIN(fgr.time), RANK() OVER (ORDER BY MIN(fgr.time) ASC) AS calculatedRank
                FROM FullGameRunCategories fgrc
                LEFT JOIN FullGameRuns fgr ON fgrc.run = fgr.id
                LEFT JOIN Users on fgr.user = Users.id
                LEFT JOIN Countries c on Users.representing = c.id
                WHERE fgrc.category = ?
                AND c.continent = ?
                GROUP BY fgr.user
                )
            WHERE run = ?
        """, (category.id, continent.id, self.id))

        return rank[0]['calculatedRank']
    
    def getSegments(self) -> list[list[Map.Map, float]]:
        segments = self.db.executeQuery("""
                                        SELECT map, time 
                                        FROM RunSegments
                                        LEFT JOIN Maps ON RunSegments.map = Maps.id 
                                        WHERE run = ?
                                        ORDER BY Maps.mapOrder ASC

                                        """, (self.id,))


        if len(segments) == 0:
            return None

        mapTimes = [] 
        for segment in segments:
            map = Map.map(self.db, segment["map"])
            time = segment["time"]
            mapTimes.append([map, time])

        return mapTimes


def fullGameRunFromId(db: Interface, id: int) -> FullGameRun:
    v = db.executeQuery("""
                        SELECT id, user, time, date
                        FROM FullGameRuns
                        WHERE id = ?

        """, (id,))
    
    if len(v) == 0:
        return None
    
    v = v[0]

    q = db.executeQuery("""
                        SELECT category, submittedAs
                        FROM FullGameRunCategories
                        WHERE run = ?
                        ORDER BY submittedAs DESC
        """, (id,))
    

    categories = [x['category'] for x in q]

    return FullGameRun(db, v['id'], v['user'], v['time'], v['date'], categories)
    


    

    
    