from database.Interface import Interface
from database.models import User
from database.models import Category
from database.models import FullGameRun
from database.models import Country
from database.models import Continent
from database.models import Map
from database import ilpoints

def getLeaderboard(db: Interface, category: str) -> list[list[str]]:
    """
    Gets the fullgame leaderboard for a given category

    Parameters:
        category - the id of the category

    Returns:
        A list of rows formatted as [username, time, placement, userid]
    
    """
    r = db.executeQuery("""
                    SELECT Users.name as USER, MIN(fgr.time) as TIME, RANK() OVER (ORDER BY fgr.time) AS PLACEMENT, Users.id as USERID
                    FROM FullGameRunCategories fgrc
                    LEFT JOIN FullGameRuns fgr ON fgrc.run = fgr.id
                    LEFT JOIN Users on fgr.user = Users.id
                    WHERE fgrc.category = ?
                    GROUP BY fgr.user
    """, (category.lower(),))

    output = [[x['USER'], x['TIME'], x['PLACEMENT'], x['USERID']] for x in r]

    return output

def getCountryLeaderboard(db: Interface, category: str, country: str) -> list[list[str]]:
    """
    Gets the fullgame leaderboard for a given category, filtered only to users representing a certain country

    Parameters:
        category - the id of the category
        country - the id of the country

    Returns:
        A list of rows formatted as [username, time]
    
    """
    r = db.executeQuery("""
                    SELECT Users.name as USER, MIN(fgr.time) as TIME, RANK() OVER (ORDER BY fgr.time) AS PLACEMENT, Users.id as USERID
                    FROM FullGameRunCategories fgrc
                    LEFT JOIN FullGameRuns fgr ON fgrc.run = fgr.id
                    LEFT JOIN Users ON fgr.user = Users.id
                    WHERE fgrc.category = ?
                    AND Users.representing = ? 
                    GROUP BY fgr.user
    """, (category, country))

    output = [[x['USER'], x['TIME'], x['PLACEMENT'], x['USERID']] for x in r]

    return output



def getContinentLeaderboard(db: Interface, category: str, continent: str) -> list[list[str]]:
    """
    Gets the fullgame leaderboard for a given category, filtered only to users representing countries in a certain continent

    Parameters:
        category - the id of the category
        continent - the id of the continent

    Returns:
        A list of rows formatted as [username, time]
    
    """

    r = db.executeQuery("""
                    SELECT Users.name as USER, MIN(fgr.time) as TIME, RANK() OVER (ORDER BY fgr.time) AS PLACEMENT, Users.id as USERID
                    FROM FullGameRunCategories fgrc
                    LEFT JOIN FullGameRuns fgr ON fgrc.run = fgr.id
                    LEFT JOIN Users ON fgr.user = Users.id
                    LEFT JOIN Countries ON Users.representing = Countries.id
                    WHERE fgrc.category = ?
                    AND Countries.continent = ? 
                    GROUP BY fgr.user
    """, (category, continent))

    output = [[x['USER'], x['TIME'], x['PLACEMENT'], x['USERID']] for x in r]

    return output


def getAverageRankLeadboard(db: Interface):
    # When I die, I'm not going to heaven. 300ms+ to run this.
    r = db.executeQuery(
        """
        SELECT id, name, AVG(placement) AS avgRank, RANK() OVER (ORDER BY AVG(placement) ASC) as placement
        FROM (
            SELECT id, name, category, placement
            FROM (
            SELECT Users.id AS id, Users.name AS name, FGRC.category, MIN(FGR.time) as fastestRun, RANK() OVER (PARTITION BY FGRC.category ORDER BY FGR.time ASC) as placement, numberOfCategories
            FROM FullGameRunCategories FGRC
            LEFT JOIN FullGameRuns FGR ON FGRC.run = FGR.id
            LEFT JOIN Users ON FGR.user = Users.id
            LEFT JOIN FullGameCategories FGC ON FGRC.category = FGC.id
            LEFT JOIN (
                SELECT id, COUNT(DISTINCT category) AS numberOfCategories
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
                ON Users.id = subquery.id
            WHERE FGC.isExtension = 0

            GROUP BY Users.id, FGRC.category
            ) 
            WHERE numberOfCategories = (SELECT COUNT(DISTINCT id) FROM FullGameCategories WHERE isExtension = 0)
            ) AS PersonalBests
        GROUP BY id
        """)
    
    return r


def getAverageRank(db: Interface, user: User.User):
    arboard = getAverageRankLeadboard(db)
    for ar in arboard:
        if ar['id'] == user.id:
            return [ar['avgRank'], ar['placement']]
        
    return None


def getWorldRecords(db: Interface, includeExtensions: bool = False) -> dict[Category.Category: FullGameRun.FullGameRun]:
    r = db.executeQuery(
        """
        SELECT fgc.id AS category, fgr.id AS runId, MIN(fgr.time) AS record
        FROM FullGameRunCategories fgrc
        LEFT JOIN FullGameRuns fgr ON fgrc.run = fgr.id
        LEFT JOIN FullGameCategories fgc ON fgrc.category = fgc.id
        LEFT JOIN Users ON fgr.user = Users.id
        WHERE fgc.isExtension <= ?
        GROUP BY fgc.id
        """, (includeExtensions,))
    
    if len(r) == 0:
        return None
    
    records = {}
    for record in r:
        category = Category.category(db, record["category"])
        run = FullGameRun.fullGameRunFromId(db, record["runId"])
        records[category] = run

    return records


def getCountryRecords(db: Interface, country: Country.Country, includeExtensions: bool = False) -> dict[Category.Category: FullGameRun.FullGameRun]:
    r = db.executeQuery(
        """
        SELECT fgc.id AS category, fgr.id AS runId, MIN(fgr.time) AS record
        FROM FullGameRunCategories fgrc
        LEFT JOIN FullGameRuns fgr ON fgrc.run = fgr.id
        LEFT JOIN FullGameCategories fgc ON fgrc.category = fgc.id
        LEFT JOIN Users ON fgr.user = Users.id
        WHERE fgc.isExtension <= ?
        AND Users.representing = ?
        GROUP BY fgc.id
        """, (includeExtensions, country.id))
    
    if len(r) == 0:
        return None
    
    records = {}
    for record in r:
        category = Category.category(db, record["category"])
        run = FullGameRun.fullGameRunFromId(db, record["runId"])
        records[category] = run

    return records


def getContinentRecords(db: Interface, continent: Continent.Continent, includeExtensions: bool = False) -> dict[Category.Category: FullGameRun.FullGameRun]:
    r = db.executeQuery(
        """
        SELECT fgc.id AS category, fgr.id AS runId, MIN(fgr.time) AS record
        FROM FullGameRunCategories fgrc
        LEFT JOIN FullGameRuns fgr ON fgrc.run = fgr.id
        LEFT JOIN FullGameCategories fgc ON fgrc.category = fgc.id
        LEFT JOIN Users ON fgr.user = Users.id
        LEFT JOIN Countries ON Users.representing = Countries.id
        WHERE fgc.isExtension <= ?
        AND Countries.continent = ?
        GROUP BY fgc.id
        """, (includeExtensions, continent.id))
    
    if len(r) == 0:
        return None
    
    records = {}
    for record in r:
        category = Category.category(db, record["category"])
        run = FullGameRun.fullGameRunFromId(db, record["runId"])
        records[category] = run

    return records

def getIlLeaderboard(db: Interface, category: Category.Category, map: Map.Map) -> list[list[str]]:
    r = db.executeQuery(
        """
        SELECT Users.name as USER, MIN(ilr.time) as TIME, RANK() OVER (ORDER BY ilr.time) AS PLACEMENT, Users.id as USERID
        FROM IndividualLevelRunCategories ilrc
        LEFT JOIN IndividualLevelRuns ilr ON ilrc.run = ilr.id
        LEFT JOIN Users on ilr.user = Users.id
        WHERE ilrc.category = ?
        AND ilr.map = ?
        GROUP BY ilr.user
        """, (category.id, map.id)
    )

    output = [[x['USER'], x['TIME'], x['PLACEMENT'], x['USERID']] for x in r]

    return output
    
    
def getSumOfIlsRank(db: Interface, category: Category.Category, time: float, includeAdvanced: bool):
    mapsTotal = 24 if includeAdvanced else 18
    r = db.executeQuery(
        """
        SELECT COUNT(soils) as rank
        FROM (
            SELECT name, SUM(pb) as soils, COUNT(pb) as mapsRun
            FROM (
                SELECT Users.id, Users.name, ilrc.category, ilr.map, MIN(time) as pb
                FROM IndividualLevelRunCategories ilrc
                LEFT JOIN IndividualLevelRuns ilr ON ilrc.run = ilr.id
                LEFT JOIN Users ON ilr.user = Users.id
                LEFT JOIN Maps ON ilr.map = Maps.id
                WHERE Maps.mapOrder < ?
                GROUP BY Users.id, ilrc.category, ilr.map
            )
            WHERE category = ?
            GROUP BY id
        )
        WHERE mapsRun = ?
        AND soils < ?
        """, (mapsTotal, category.id, mapsTotal, round(time, 3))
    )

    return r[0]['rank']+1

def getIlPointsLeaderboard(db: Interface, category: Category.Category = None):
    if category:
        categorySpecifier = f"AND ILC.id = '{category.id}'"
    else:
        categorySpecifier = ""

    r = db.executeQuery(
        f"""
        SELECT id, name, SUM(points(placement)) as total
        FROM (
            SELECT Users.id AS id, Users.name AS name, ILRC.category, ILR.map, MIN(ILR.time) as fastestRun, RANK() OVER (PARTITION BY ILRC.category, ILR.map ORDER BY ILR.time ASC) as placement
            FROM IndividualLevelRunCategories ILRC
            LEFT JOIN IndividualLevelRuns ILR ON ILRC.run = ILR.id
            LEFT JOIN Users ON ILR.user = Users.id
            LEFT JOIN IndividualLevelCategories ILC ON ILRC.category = ILC.id
            LEFT JOIN IndividualLevelCategoryActiveMaps ILCAM ON ILC.id = ILCAM.category AND ILR.map = ILCAM.map

            WHERE ILC.isExtension = 0
            AND ILCAM.active = 1
            {categorySpecifier}

            GROUP BY Users.id, ILRC.category, ILR.map
        )
        GROUP BY id
        ORDER BY total DESC
        """,
        customFunctions= [["points", 1, ilpoints.points]]
    )

    output = []
    for row in r:
        output.append([row['name'], str(int(round(row['total'], 0)))])

    return output


def getIlPointsRank(db: Interface, pointsTotal: float, category: Category.Category = None):
    if category:
        categorySpecifier = f"AND ILC.id = '{category.id}'"
    else:
        categorySpecifier = ""

    r = db.executeQuery(
        f"""
        SELECT COUNT(id) as rank
        FROM (
            SELECT id, name, SUM(points(placement)) as total
            FROM (
                SELECT Users.id AS id, Users.name AS name, ILRC.category, ILR.map, MIN(ILR.time) as fastestRun, RANK() OVER (PARTITION BY ILRC.category, ILR.map ORDER BY ILR.time ASC) as placement
                FROM IndividualLevelRunCategories ILRC
                LEFT JOIN IndividualLevelRuns ILR ON ILRC.run = ILR.id
                LEFT JOIN Users ON ILR.user = Users.id
                LEFT JOIN IndividualLevelCategories ILC ON ILRC.category = ILC.id
                LEFT JOIN IndividualLevelCategoryActiveMaps ILCAM ON ILC.id = ILCAM.category AND ILR.map = ILCAM.map

                WHERE ILC.isExtension = 0
                AND ILCAM.active = 1
                {categorySpecifier}

                GROUP BY Users.id, ILRC.category, ILR.map
            )
            GROUP BY id
            ORDER BY total DESC
        )
        WHERE total > ?
        """, (pointsTotal,),
        customFunctions= [["points", 1, ilpoints.points]]
    )

    return r[0]['rank']+1