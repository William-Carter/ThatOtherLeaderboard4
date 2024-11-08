from database import Interface
from database.models import User
def getAmcLeaderboard(db: Interface.Interface):
    r = db.executeQuery(
        """
        SELECT Name, AMCTotal, RANK() OVER (ORDER BY AMCTotal ASC) AS amcRank
        FROM (
            SELECT Name, ROUND(SUM(fastestRun), 3) AS AMCTotal, COUNT(DISTINCT category) AS numberOfCategories
            FROM (
                SELECT Users.id AS id, Users.name AS Name, FGRC.category, MIN(FGR.time) as fastestRun
                FROM FullGameRunCategories FGRC
                LEFT JOIN FullGameRuns FGR ON FGRC.run = FGR.id
                LEFT JOIN Users ON FGR.user = Users.id
                LEFT JOIN FullGameCategories FGC ON FGRC.category = FGC.id
                WHERE FGC.isExtension = 0
                GROUP BY Users.id, FGRC.category) AS fastestRunsForRunners
                GROUP BY id
            ) AS subquery
        WHERE numberOfCategories = (SELECT COUNT(DISTINCT id) FROM FullGameCategories WHERE isExtension = 0)
        ORDER BY AMCTotal
    """)

    return r


def getAmc(db: Interface.Interface, user: User.User):
    amcBoard = getAmcLeaderboard(db)
    for amc in amcBoard:
        if amc['Name'] == user.name: # Using the name here is fucking stupid but it should be fine
            return [amc['AMCTotal'], amc['amcRank']]
        

    return None