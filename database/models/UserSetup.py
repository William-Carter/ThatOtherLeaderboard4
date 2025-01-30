from database.models import User
from database.models import SetupElement

class UserSetup:
    def __init__(self, user: 'User.User', element: SetupElement.SetupElement, value: str):
        self.user = user
        self.element = element
        if element.valueType == "num":
            self.value = float(value)
        else:
            self.value = value
