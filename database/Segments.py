from database.models import FullGameRun
from database.models import Map
from database.Interface import Interface
def upsertSegments(db: Interface, run: FullGameRun.FullGameRun, mapTimes: list[list[Map.Map|float]]):
    for mapTime in mapTimes:
        db.insertAndFetchRowID(
            """
            INSERT OR IGNORE INTO RunSegments (run, map, time)
            VALUES (?, ?, ?)
            """,
            (run.id, mapTime[0].id, mapTime[1])
        )

        db.insertAndFetchRowID(
            """
            UPDATE RunSegments
            SET time = ?
            WHERE run = ?
            AND map = ?
            """,
            (mapTime[1], run.id, mapTime[0].id)
        )
    
