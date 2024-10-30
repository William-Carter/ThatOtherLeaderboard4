from database.Interface import Interface
from database.models import Category
from database.models import Map
from database.models import User

def getCommunityGolds(db: Interface, category: Category.Category):
    r = db.executeQuery(
        """
        SELECT mt.map, mt.user, mt.time
        FROM MapTimes mt
        JOIN (
            SELECT smt.category, smt.map, MIN(smt.time) AS cgold
            FROM MapTimes smt
            LEFT JOIN CommunityGoldEligibility scge
            ON smt.user = scge.user
            AND smt.category = scge.category
            AND smt.map = scge.map
            WHERE scge.eligible = 1
            AND smt.category = ?
            AND smt.type = "gold"
            GROUP BY smt.map
            ) AS m ON m.category = mt.category AND m.cgold = mt.time AND m.map = mt.map

        LEFT JOIN Maps
        ON Maps.id = mt.map
        WHERE mt.category = ?
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