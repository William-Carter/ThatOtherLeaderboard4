from database.Interface import Interface
class FullGameRun:
    def __init__(self, db: Interface, id: int, user: int, time: float, date: str):
        self.id = id
        self.user = user
        self.time = time
        self.date = date