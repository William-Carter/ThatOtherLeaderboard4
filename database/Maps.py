from database.Interface import Interface
from database.models import Map
def getMainLevels(db: Interface) -> list[Map.Map]:
    """
    Returns a list of all main level ids (00/01 to escape_02) in the order they appear in-game
    """

    r = db.executeQuery(
            """
            SELECT id
            FROM Maps
            ORDER BY mapOrder ASC
            """)
    
    return [Map.map(db, x['id']) for x in r]