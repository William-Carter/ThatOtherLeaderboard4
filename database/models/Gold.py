from database.Interface import Interface
from database.models import User
from database.models import Category
from database.models import Map
class Gold:
    def __init__(self, db: Interface, user: 'User.User', category: Category.Category, level: Map.Map, time: float):
        self.db = db
        self.user = user
        self.category = category
        self.map = level
        self.time = time


    def getRank(self) -> int:
        rank = self.db.executeQuery("""
            SELECT calculatedRank
            FROM (
                SELECT mt.user, MIN(mt.time), RANK() OVER (ORDER BY MIN(mt.time) ASC) AS calculatedRank
                FROM MapTimes mt
                WHERE mt.type = "gold"
                AND mt.category = ?
                AND mt.map = ?
                GROUP BY mt.user
                )
            WHERE user = ?
        """, (self.category.id, self.map.id, self.user.id))

        return rank[0]['calculatedRank']