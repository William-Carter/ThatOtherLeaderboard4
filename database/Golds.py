from database.Interface import Interface
from database.models import Category
from database.models import Map
from database.models import User


def getCommunityGolds(db: Interface, category: Category.Category) -> list:

    """
    Returns a list of the community golds

    Parameters:
        category - The category you want the comgolds for

    Returns:
        A list in the form [[Map.Map, time, [User.User]]]
    """
    r = db.executeQuery(
        """
        SELECT mt.map, mt.user, mt.time
        FROM Golds mt
        JOIN (
            SELECT smt.category, smt.map, MIN(smt.time) AS cgold
            FROM Golds smt
            LEFT JOIN CommunityGoldEligibility scge
            ON smt.user = scge.user
            AND smt.category = scge.category
            AND smt.map = scge.map
            WHERE scge.eligible = 1
            AND smt.category = ?
            GROUP BY smt.map
            ) AS m ON m.category = mt.category AND m.cgold = mt.time AND m.map = mt.map
        LEFT JOIN Maps ON Maps.id = mt.map
        LEFT JOIN CommunityGoldEligibility cge
        ON mt.user = cge.user
        AND mt.map = cge.map
        AND mt.category = cge.category

        WHERE mt.category = ?
        AND cge.eligible = 1
        ORDER BY Maps.mapOrder
        """, (category.id, category.id))
    
    comgolds = {}
    # {mapId: time: Time, runners: [Runners]}
    for row in r:
        if not row['map'] in comgolds.keys():
            comgolds[row['map']] = {"time": row['time'], "runners": [row['user'],]}
        else:
            comgolds[row['map']]['runners'].append(row['user'])

    # [[Map.Map, time, [runners]]]
    cgolds = []
    for cgold in comgolds.keys():
        mapObj = Map.map(db, cgold)
        runners = [User.userFromId(db, x) for x in comgolds[cgold]["runners"]]
        cgolds.append([mapObj, comgolds[cgold]["time"], runners])

    return cgolds

def getSumOfBestLeaderboard(db: Interface, category: Category.Category) -> list:
    r = db.executeQuery(
        """
        SELECT Users.id, SUM(Golds.time) as sob
        FROM Golds
        LEFT JOIN Users ON Golds.user = Users.id
        WHERE Golds.category = ?
        GROUP BY Users.id
        ORDER BY sob
        """, (category.id,))
    
    sobList = [[User.userFromId(db, sob['id']), sob['sob']] for sob in r]
    return sobList

def getSumOfBestRank(db: Interface, category: Category.Category, sumOfBest: float) -> int:
    r = db.executeQuery("""
    SELECT COUNT(id) AS rank
    FROM (
        SELECT Users.id, SUM(Golds.time) as sob
        FROM Golds
        LEFT JOIN Users ON Golds.user = Users.id
        WHERE Golds.category = ?
        GROUP BY Users.id
        ORDER BY sob
    )
    WHERE sob < ?
    """, (category.id, sumOfBest))

    return r[0]['rank']+1




def getGoldLeaderboard(db: Interface, category: Category.Category, map: Map.Map) -> list:
    """
    Gets the gold leaderboard for a specific map/category combination

    Parameters:
        category - The category object
        map - The map object

    Returns:
        A list of lists in the form [[UserObj, goldTime]], ordered by goldTime
    """
    r = db.executeQuery(
        """
        SELECT Users.id, Golds.time as sob
        FROM Golds
        LEFT JOIN Users ON Golds.user = Users.id
        LEFT JOIN CommunityGoldEligibility cge
        ON Golds.map = cge.map
        AND Golds.category = cge.category
        AND Golds.user = cge.user
        WHERE Golds.category = ?
        AND Golds.map = ?
        AND eligible = 1
        GROUP BY Users.id
        ORDER BY sob
        """, (category.id, map.id))
    
    goldList = [[User.userFromId(db, sob['id']), sob['sob']] for sob in r]
    return goldList

def getDefaultEligibility(db: Interface, map: Map.Map, category: Category.Category) -> int:
    r = db.executeQuery("""
                        SELECT eligible
                        FROM DefaultCommunityGoldEligiblity
                        WHERE category = ?
                        AND map = ?
                        """, (category.id, map.id))[0]
    
    return r["eligible"]
    



def upsertGolds(db: Interface, user: User.User, category: Category.Category, mapTimes: list[list[Map.Map|float]]):
    for mapTime in mapTimes:
        db.insertAndFetchRowID(
            """
            INSERT OR IGNORE INTO Golds (user, category, map, time)
            VALUES (?, ?, ?, ?)
            """,
            (user.id, category.id, mapTime[0].id, mapTime[1])
        )

        db.insertAndFetchRowID(
            """
            INSERT OR IGNORE INTO CommunityGoldEligibility (user, category, map, eligible)
            VALUES (?, ?, ?, ?)
            """,
            (user.id, category.id, mapTime[0].id, getDefaultEligibility(db, mapTime[0], category))
        )

        db.insertAndFetchRowID(
            """
            UPDATE Golds
            SET time = ?
            WHERE user = ?
            AND category = ?
            AND map = ?
            """,
            (mapTime[1], user.id, category.id, mapTime[0].id)
        )
