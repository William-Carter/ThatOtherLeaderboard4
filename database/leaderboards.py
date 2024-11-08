from database.Interface import Interface
from database.models import User
def getLeaderboard(db: Interface, category: str) -> list[list[str]]:
    """
    Gets the fullgame leaderboard for a given category

    Parameters:
        category - the id of the category

    Returns:
        A list of rows formatted as [username, time]
    
    """
    r = db.executeQuery("""
                    SELECT Users.name as USER, MIN(fgr.time) as TIME
                    FROM FullGameRunCategories fgrc
                    LEFT JOIN FullGameRuns fgr ON fgrc.run = fgr.id
                    LEFT JOIN Users on fgr.user = Users.id
                    WHERE fgrc.category = ?
                    GROUP BY fgr.user
                    ORDER BY fgr.time
    """, (category.lower(),))

    output = [[x['USER'], x['TIME']] for x in r]

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
                    SELECT Users.name as USER, MIN(fgr.time) as TIME
                    FROM FullGameRunCategories fgrc
                    LEFT JOIN FullGameRuns fgr ON fgrc.run = fgr.id
                    LEFT JOIN Users ON fgr.user = Users.id
                    WHERE fgrc.category = ?
                    AND Users.representing = ? 
                    GROUP BY fgr.user
                    ORDER BY fgr.time
    """, (category, country))

    output = [[x['USER'], x['TIME']] for x in r]

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
                    SELECT Users.name as USER, MIN(fgr.time) as TIME
                    FROM FullGameRunCategories fgrc
                    LEFT JOIN FullGameRuns fgr ON fgrc.run = fgr.id
                    LEFT JOIN Users ON fgr.user = Users.id
                    LEFT JOIN Countries ON Users.representing = Countries.id
                    WHERE fgrc.category = ?
                    AND Countries.continent = ? 
                    GROUP BY fgr.user
                    ORDER BY fgr.time
    """, (category, continent))

    output = [[x['USER'], x['TIME']] for x in r]

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