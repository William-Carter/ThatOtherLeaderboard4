from database.Interface import Interface
from database.models import Category


def calculateSprm(db: Interface, category: Category, time: float) -> float|None:
    """
    Calculate the SPRM value for a certain time in the provided category

    Parameters:
        category - the category object for the category you want to calculate SPRM for

        time - the time you want to calculate SPRM for

    Returns:
        The float SPRM value rounded to two decimal places if the category is valid, None if it isn't
    """
    q = db.executeQuery("SELECT a, b, c FROM sprmValues WHERE category = ?", (category.id,))
    if len(q) == 0:
        return None
    
    a = q[0]['a']
    b = q[0]['b']
    c = q[0]['c']

    return round(a * 10**b * (time**c), 2)
        
def calculateInverseSprm(db: Interface, category: Category, sprm: float) -> float|None:
    """
    Calculate what time a certain sprm value corresponds to for a specific category

    Parameters:
        category - the category object for the category you want to calculate time for

        sprm - the sprm you want to calculate time for

    Returns:
        The float time value rounded to three decimal places if the category is valid, None if it isn't
    """
    
    q = db.executeQuery("SELECT a, b, c FROM sprmValues WHERE category = ?", (category.id,))
    if len(q) == 0:
        return None
    
    a = q[0]['a']
    b = q[0]['b']
    c = q[0]['c']


    return round((sprm/(a*10**b))^(1/c), 3)



def getSprmLeaderboard(db: Interface):
    q = db.executeQuery("""
        SELECT Users.name, ROUND(SUM(score), 2) as sprm
        FROM
        (
            SELECT 
            fgr.user as user, 
            fgrc.category,
            (sv.a * POWER(10, sv.b)) * (POWER(MIN(fgr.time), sv.c)) AS score
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
    """)

    return q