from database.Interface import Interface
from database.models import User
from database.models import Category
from database.models import Map
class Gold:
    def __init__(self, db: Interface, user: 'User.User', category: Category.Category, level: Map.Map, time: float, eligible: bool):
        self.db = db
        self.user = user
        self.category = category
        self.map = level
        self.time = time
        self.eligible = bool(eligible)


    def getRank(self) -> int:
        if not self.eligible:
            return -1

        rank = self.db.executeQuery("""
            SELECT calculatedRank
            FROM (
                SELECT mt.user, MIN(mt.time), RANK() OVER (ORDER BY MIN(mt.time) ASC) AS calculatedRank
                FROM Golds mt
                LEFT JOIN CommunityGoldEligibility cge
                ON cge.user = mt.user
                AND cge.category = mt.category
                AND cge.map = mt.map
                WHERE mt.category = ?
                AND mt.map = ?
                AND cge.eligible = 1
                GROUP BY mt.user
                )
            WHERE user = ?
        """, (self.category.id, self.map.id, self.user.id))

        return rank[0]['calculatedRank']
    

    def toggleEligible(self) -> bool:
        self.eligible = not self.eligible
        i = int(self.eligible)
        self.db.insertAndFetchRowID(
            """
            UPDATE CommunityGoldEligibility
            SET eligible = ?
            WHERE user = ?
            AND category = ?
            AND map = ?
            """, (i, self.user.id, self.category.id, self.map.id))
        
        return self.eligible

