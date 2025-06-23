from database import Interface
from database.models.IndividualLevelCategory import IndividualLevelCategory


class IndividualLevelRun:
    def __init__(self, db: Interface.Interface, id: int, userId: int, time: float, date: str, mapId: str, categories: list[str]):
        self.db = db
        self.id = id
        self.userId = userId
        self.time = time
        self.date = date
        self.mapId = mapId
        self.categories = categories


    def getRankInCategory(self, category: IndividualLevelCategory):
        # TODO: Passing the map into the query is dumb when the map is determined by the run ID, make it not dumb at some point
        rank = self.db.executeQuery("""
            SELECT calculatedRank
            FROM (
                SELECT ilrc.run, MIN(ilr.time), RANK() OVER (ORDER BY MIN(ilr.time) ASC) AS calculatedRank
                FROM IndividualLevelRunCategories ilrc
                LEFT JOIN IndividualLevelRuns ilr ON ilrc.run = ilr.id
                WHERE ilrc.category = ?
                AND ilr.map = ?
                GROUP BY ilr.user
                )
            WHERE run = ?
        """, (category.id, self.mapId, self.id))

        return rank[0]['calculatedRank']

def individualLevelrun(db: Interface, id: str) -> IndividualLevelRun:
    r = db.executeQuery("""
        SELECT id, user, time, date, map
        FROM IndividualLevelRuns
        WHERE id = ?
    """, (id,))

    if len(r) == 0:
        return None
    
    run = r[0]

    r = db.executeQuery("""
        SELECT category
        FROM IndividualLevelRunCategories
        WHERE run = ?
        ORDER BY submittedAs DESC
    """, (id,))

    categories = [x['category'] for x in r]

    return IndividualLevelRun(db, run['id'], run['user'], run['time'], run['date'], run['map'], categories)