import logging
import syncILs
from database.Interface import Interface

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)


def main(db: Interface):
    with open("ilqueue.txt", "r+") as f:
        lines = f.readlines()
        category, map = lines[0].strip().split(" ")
        syncILs.sync(db, category, map)
        
        lines[-1] += "\n"
        lines.append(lines[0].strip())
        lines.pop(0)
        f.seek(0)
        f.writelines(lines)
        f.truncate()
        




if __name__ == "__main__":
    db = Interface("ThatOtherLeaderboard.db")
    main(db)
