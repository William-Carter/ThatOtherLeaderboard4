from database.Interface import Interface
from database.models import Category
from database.models import IndividualLevelCategory as ilc
def getMainFullGameCategories(db: Interface) -> list[Category.Category]:
    """
    Get the list of main categories

    Returns:
        A list of category objects
    """
    categories = []
    q = db.executeQuery("SELECT id FROM FullGameCategories WHERE isExtension = 0")
    for category in q:
        categories.append(Category.category(db, category['id']))

    return categories


def propagatedCategories(db: Interface, baseCategory: Category.Category) -> list[Category.Category]:
    """
    Get the list of all categories that a given category propagates to

    Parameters:
        baseCategory - the original category object

    Returns:
        A list of category objects
    """
    categories = []
    q = db.executeQuery("SELECT propagatedCategory AS pc FROM FullGameCategoryPropagations WHERE baseCategory = ?", (baseCategory.id,))
    for category in q:
        categories.append(Category.category(db, category['pc']))

    return categories

 
def getMainILCategories(db: Interface) -> list[ilc.IndividualLevelCategory]:
    """
    Get the list of main individual level categories

    Returns:
        A list of category objects
    """
    categories = []
    q = db.executeQuery("SELECT id FROM IndividualLevelCategories WHERE isExtension = 0 ORDER BY id")
    for category in q:
        categories.append(Category.category(db, category['id']))

    return categories


def propagatedILCategories(db: Interface, baseCategory: ilc.IndividualLevelCategory) -> list[ilc.IndividualLevelCategory]:
    """
    Get the list of all categories that a given individual level category propagates to

    Parameters:
        baseCategory - the original individual level category object

    Returns:
        A list of category objects
    """
    categories = []
    q = db.executeQuery("SELECT propagatedCategory AS pc FROM IndividualLevelCategoryPropagations WHERE baseCategory = ?", (baseCategory.id,))
    for category in q:
        categories.append(ilc.individualLevelCategory(db, category['pc']))

    return categories
