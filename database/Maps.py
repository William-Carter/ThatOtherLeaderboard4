from database.Interface import Interface
from database.models import Map
def getMainLevels(db: Interface, includeAdvanced: bool = False) -> list[Map.Map]:
    """
    Returns a list of all main maps (00/01 to escape_02) in the order they appear in-game
    """

    r = db.executeQuery(
            """
            SELECT id
            FROM Maps
            ORDER BY mapOrder ASC
            """)
    
    mapList = [Map.map(db, x['id']) for x in r]
    if not includeAdvanced:
        mapList = mapList[:18]
    
    return mapList
