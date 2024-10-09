from database.models import User
from database.models import Map
from database.models import Category
from database.Interface import Interface
def upsertMapTimes(db: Interface, user: User.User, type: str, category: Category.Category, mapTimes: list[list[Map.Map|float]]):
    for mapTime in mapTimes:
        db.insertAndFetchRowID(
            """
            INSERT OR IGNORE INTO MapTimes (user, type, category, map, time)
            VALUES (?, ?, ?, ?, ?)
            """,
            (user.id, type, category.id, mapTime[0].id, mapTime[1])
        )
        db.insertAndFetchRowID(
            """
            UPDATE MapTimes
            SET time = ?
            WHERE user = ?
            AND type = ?
            AND category = ?
            AND map = ?
            """,
            (mapTime[1], user.id, type, category.id, mapTime[0].id)
        )

