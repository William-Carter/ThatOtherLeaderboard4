from database.Interface import Interface
from database.models.Category import Category
from database.models import User

from database.sprmFuncs import inbounds_20251120 as inbounds, glitchless_20251120 as glitchless, unrestricted_20251120 as unrestricted, legacy_20251120 as legacy, oob_20251120 as oob


def getFunc(category: str):
    catFuncs = {
        "glitchless": glitchless,
        "inbounds": inbounds,
        "oob": oob,
        "legacy": legacy,
        "unrestricted": unrestricted
    }

    return catFuncs[category]

def calculateSprm(db: Interface, category: Category, time: float) -> float|None:
    """
    Calculate the SPRM value for a certain time in the provided category

    Parameters:
        category - the category object for the category you want to calculate SPRM for

        time - the time you want to calculate SPRM for

    Returns:
        The float SPRM value rounded to two decimal places if the category is valid, None if it isn't
    """
    func = getFunc(category.id)
    return float(func.func(time))
        
def calculateInverseSprm(db: Interface, category: Category, sprm: float) -> float|None:
    """
    Calculate what time a certain sprm value corresponds to for a specific category

    Parameters:
        category - the category object for the category you want to calculate time for

        sprm - the sprm you want to calculate time for

    Returns:
        The float time value rounded to three decimal places if the category is valid, None if it isn't
    """
    
    func = getFunc(category.id)
    return float(func.inv(sprm))

def calcSprmFromId(category: str, time: float) -> float|None:
    func = getFunc(category)
    return float(func.func(time))


def getSprmLeaderboard(db: Interface):
    q = db.executeQuery("""
        SELECT Users.id, Users.name, ROUND(SUM(score), 2) as sprm, RANK() OVER (ORDER BY SUM(score) DESC) AS placement
        FROM
        (
            SELECT 
            fgr.user as user, 
            fgrc.category,
            SPRM(fgrc.category, MIN(fgr.time)) AS score
            FROM FullGameRunCategories fgrc
            LEFT JOIN FullGameRuns fgr ON fgrc.run = fgr.id
            LEFT JOIN FullGameCategories fgc ON fgrc.category = fgc.id
            LEFT JOIN sprmValues sv ON fgc.id = sv.category
            WHERE fgc.isExtension = 0
            GROUP BY fgr.user, fgrc.category
        ) AS subquery
        LEFT JOIN Users ON subquery.user = Users.id
        GROUP BY Users.id
        ORDER BY sprm DESC
    """, customFunctions=[["SPRM", 2, calcSprmFromId]])

    return q


def getSprmPlacement(db: Interface, user: User.User):
    sprmBoard = getSprmLeaderboard(db)
    for sprm in sprmBoard:
        if user.id == sprm['id']:
            return [sprm['sprm'], sprm['placement']]
        
    return None
    