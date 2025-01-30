from database import Interface
class SetupElement:
    def __init__(self, id: str, name: str, valueType: str):
        self.id = id
        self.name = name
        self.valueType = valueType

    def __eq__(self, other):
        return isinstance(other, SetupElement) and self.id == other.id
    
    def __hash__(self):
        return hash(self.id)



def setupElementFromId(db: Interface.Interface, id: str) -> SetupElement:
    r = db.executeQuery("SELECT id, name, type FROM SetupElements WHERE id = ?", (id,))
    if len(r) == 0:
        return None
    
    se = r[0]
    return SetupElement(se["id"], se["name"], se["type"])

