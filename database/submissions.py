import database.categories
import UI.durations

from database.Interface import Interface

from database.models import FullGameRun
from database.models import IndividualLevelRun
from database.models.User import User
from database.models.Category import Category
from database.models.IndividualLevelCategory import IndividualLevelCategory
from database.models.Map import Map

def submitFullGameRun(db: Interface, user: User, time: float, date: str, category: Category) -> FullGameRun.FullGameRun:
    time = UI.durations.correctToTick(time)
    

    runId = db.insertAndFetchRowID("""
        INSERT INTO FullGameRuns (user, time, date)
        VALUES (?, ?, ?)
        """, (user.id, time, date))
    
    categories = database.categories.propagatedCategories(db, category)
    for currentCategory in categories:
        submittedAs = currentCategory == category
        db.insertAndFetchRowID("""
        INSERT INTO FullGameRunCategories (run, category, submittedAs)
        VALUES (?, ?, ?)
        """, (runId, currentCategory.id, submittedAs))


    run = FullGameRun.fullGameRunFromId(db, runId)

    return run


def deleteFullGameRun(db: Interface, runId: int):
    db.insertAndFetchRowID(
        """
        DELETE FROM FullGameRunCategories
        WHERE run = ?
        """, (runId,))
    
    db.insertAndFetchRowID(
        """
        DELETE FROM FullGameRuns
        WHERE id = ?
        """, (runId,)
    )


def submitIndividualLevelRun(db: Interface, user: User, time: float, date: str, map: Map, category: IndividualLevelCategory) -> IndividualLevelRun.IndividualLevelRun:
    time = UI.durations.correctToTick(time)

    runId = db.insertAndFetchRowID("""
        INSERT INTO IndividualLevelRuns (user, time, date, map)
        VALUES (?, ?, ?, ?)
    """, (user.id, time, date, map.id))


    categories = database.categories.propagatedILCategories(db, category)

    for currentCategory in categories:
        submittedAs = currentCategory == category
        db.insertAndFetchRowID("""
        INSERT INTO IndividualLevelRunCategories (run, category, submittedAs)
        VALUES (?, ?, ?)
        """, (runId, currentCategory.id, submittedAs))


    run = IndividualLevelRun.individualLevelrun(db, runId)
    return run


def deleteIndividualLevelRun(db: Interface, runId: int):
    db.insertAndFetchRowID(
        """
        DELETE FROM IndividualLevelRunCategories
        WHERE run = ?
        """, (runId,))
    
    db.insertAndFetchRowID(
        """
        DELETE FROM IndividualLevelRuns
        WHERE id = ?
        """, (runId,)
    )