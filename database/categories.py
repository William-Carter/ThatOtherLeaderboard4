from database.Interface import Interface
from database.models import Category
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

