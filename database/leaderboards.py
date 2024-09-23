from database.Interface import Interface
def getLeaderboard(db: Interface, category: str) -> list[list[str]]:
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
