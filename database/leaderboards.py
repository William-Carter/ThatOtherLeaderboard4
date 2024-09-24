from database.Interface import Interface
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