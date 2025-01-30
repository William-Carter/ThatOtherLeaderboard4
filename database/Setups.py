from database import Interface
from database.models import User
from database.models import SetupElement
def upsertUserSetup(db: Interface.Interface, user: User.User, element: SetupElement.SetupElement, value: str):
    db.insertAndFetchRowID("""
        INSERT OR IGNORE INTO UserSetups (user, element, value)
        VALUES (?, ?, ?)
    """, (user.id, element.id, value))

    db.insertAndFetchRowID("""
        UPDATE UserSetups 
        SET value = ?
        WHERE user = ?
        AND element = ?
    """, (value, user.id, element.id))