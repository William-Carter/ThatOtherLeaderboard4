import sqlite3

def construct(dbPath: str) -> None:
    """
    Constructs the database from scratch
    """
    conn = sqlite3.connect(dbPath)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE "Continents" (
	"id"	TEXT,
	PRIMARY KEY("id")
    )
    """)

    cursor.execute("""
    CREATE TABLE "ContinentNames" (
	"continent"	TEXT,
	"name"	TEXT UNIQUE,
	"isPrimary"	INTEGER NOT NULL,
	FOREIGN KEY("continent") REFERENCES "Continents"("id"),
	UNIQUE("continent","isPrimary"),
	PRIMARY KEY("continent","name")
	)
    """)

    cursor.execute("""
    CREATE TABLE "Countries" (
	"id"	TEXT,
	"continent"	TEXT NOT NULL,
	PRIMARY KEY("id"),
	FOREIGN KEY("continent") REFERENCES "Continents"("id")
    )
    """)

    cursor.execute("""
    CREATE TABLE "CountryNames" (
	"country"	TEXT,
	"name"	TEXT,
	"isPrimary"	INTEGER NOT NULL UNIQUE,
	PRIMARY KEY("country","name"),
	FOREIGN KEY("country") REFERENCES "Countries"("id")
    )
    """)
    

    cursor.execute("""
    CREATE TABLE "Users" (
	"id"	INTEGER NOT NULL UNIQUE,
	"name"	TEXT UNIQUE,
	"discordId"	TEXT UNIQUE,
	"srcId"	TEXT UNIQUE,
	"representing" TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
	FOREIGN KEY("representing") REFERENCES "Countries"("id")
    )

    """)


    cursor.execute("""
    CREATE TABLE "Categories" (
	"id"	TEXT,
	"isIndividualLevel"	INTEGER NOT NULL,
	"isExtension"	INTEGER NOT NULL,
	PRIMARY KEY("id")
    )
    """)

    cursor.execute("""
    CREATE TABLE "CategoryNames" (
	"category"	TEXT,
	"name"	TEXT UNIQUE,
	"isPrimary"	INTEGER NOT NULL,
	PRIMARY KEY("category","name"),
	FOREIGN KEY("category") REFERENCES "Categories"("id")
    )
    """)

    cursor.execute("""
    CREATE TABLE "CategoryPropagations" (
	"baseCategory"	TEXT,
	"propagatedCategory"	TEXT,
	FOREIGN KEY("propagatedCategory") REFERENCES "Categories"("id"),
	FOREIGN KEY("baseCategory") REFERENCES "Categories"("id"),
	PRIMARY KEY("baseCategory","propagatedCategory")
    )
    """)

    cursor.execute("""
    CREATE TABLE "Maps" (
	"id"	TEXT,
	PRIMARY KEY("id")
    )
    """)

    cursor.execute("""
    CREATE TABLE "MapNames" (
	"map"	TEXT,
	"name"	TEXT UNIQUE,
	"isPrimary"	INTEGER NOT NULL,
	FOREIGN KEY("map") REFERENCES "Maps"("id"),
	PRIMARY KEY("map","name")
    )
    """)

    cursor.execute("""
    CREATE TABLE "MapTimes" (
	"user"	INTEGER,
	"type"	TEXT,
    "category" TEXT,
	"map"	TEXT,
	"time"	REAL,
	PRIMARY KEY("user","type", "category", "map"),
	FOREIGN KEY("map") REFERENCES "Maps"("id"),
	FOREIGN KEY("user") REFERENCES "Users"("id")
    FOREIGN KEY("category") REFERENCES "Categories"("id")
    )
    """)

    cursor.execute("""
    CREATE TABLE "FullGameRuns" (
	"id"	INTEGER NOT NULL UNIQUE,
	"user"	INTEGER NOT NULL,
	"time"	REAL NOT NULL,
	"date"	TEXT,
	FOREIGN KEY("user") REFERENCES "Users"("id"),
	PRIMARY KEY("id")
    )
    """)

    cursor.execute("""
    CREATE TABLE "FullGameRunCategories" (
	"run"	INTEGER,
	"category"	TEXT,
	"submittedAs"	INTEGER NOT NULL,
	FOREIGN KEY("category") REFERENCES "Categories"("id"),
	FOREIGN KEY("run") REFERENCES "FullGameRuns"("id"),
	PRIMARY KEY("run","category")
    )
    """)

    cursor.execute("""
	CREATE TABLE "IndividualLevelRuns" (
	"id"	INTEGER NOT NULL UNIQUE,
	"user"	INTEGER NOT NULL,
	"time"	REAL NOT NULL,
	"date"	TEXT,
	"map"	TEXT NOT NULL,
	FOREIGN KEY("user") REFERENCES "Users"("id"),
	FOREIGN KEY("map") REFERENCES "Maps"("id"),
	PRIMARY KEY("id" AUTOINCREMENT)
    )
    """)

    cursor.execute("""
    CREATE TABLE "IndividualLevelRunCategories" (
	"run"	INTEGER,
	"category"	TEXT,
	"submittedAs"	INTEGER NOT NULL,
	PRIMARY KEY("run","category"),
	FOREIGN KEY("run") REFERENCES "IndividualLevelRuns"("id"),
	FOREIGN KEY("category") REFERENCES "Categories"("id")
    )
    """)
    

if __name__ == "__main__":
    construct("ThatOtherLeaderboard.db")
