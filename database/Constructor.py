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
	"isPrimary"	INTEGER NOT NULL,
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
    CREATE TABLE "FullGameCategories" (
	"id"	TEXT,
	"isExtension"	INTEGER NOT NULL,
	PRIMARY KEY("id")
    )
    """)

    cursor.execute("""
    CREATE TABLE "FullGameCategoryNames" (
	"category"	TEXT,
	"name"	TEXT UNIQUE,
	"isPrimary"	INTEGER NOT NULL,
	PRIMARY KEY("category","name"),
	FOREIGN KEY("category") REFERENCES "FullGameCategories"("id")
    )
    """)

    cursor.execute("""
    CREATE TABLE "FullGameCategoryPropagations" (
	"baseCategory"	TEXT,
	"propagatedCategory"	TEXT,
	FOREIGN KEY("propagatedCategory") REFERENCES "FullGameCategories"("id"),
	FOREIGN KEY("baseCategory") REFERENCES "FullGameCategories"("id"),
	PRIMARY KEY("baseCategory","propagatedCategory")
    )
    """)
    
    cursor.execute("""
    CREATE TABLE "IndividualLevelCategories" (
	"id"	TEXT,
	"isExtension"	INTEGER NOT NULL,
	PRIMARY KEY("id")
    )
    """)

    cursor.execute("""
    CREATE TABLE "IndividualLevelCategoryNames" (
	"category"	TEXT,
	"name"	TEXT UNIQUE,
	"isPrimary"	INTEGER NOT NULL,
	PRIMARY KEY("category","name"),
	FOREIGN KEY("category") REFERENCES "IndividualLevelCategories"("id")
    )
    """)

    cursor.execute("""
    CREATE TABLE "IndividualLevelCategoryPropagations" (
	"baseCategory"	TEXT,
	"propagatedCategory"	TEXT,
	FOREIGN KEY("propagatedCategory") REFERENCES "IndividualLevelCategories"("id"),
	FOREIGN KEY("baseCategory") REFERENCES "IndividualLevelCategories"("id"),
	PRIMARY KEY("baseCategory","propagatedCategory")
    )
    """)


    cursor.execute("""
    CREATE TABLE "Maps" (
	"id"	TEXT,
	"mapOrder" INTEGER NOT NULL UNIQUE,
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
    CREATE TABLE "Golds" (
	"user"	INTEGER,
    "category" TEXT,
	"map"	TEXT,
	"time"	REAL,
	PRIMARY KEY("user", "category", "map"),
	FOREIGN KEY("map") REFERENCES "Maps"("id"),
	FOREIGN KEY("user") REFERENCES "Users"("id")
    FOREIGN KEY("category") REFERENCES "FullGameCategories"("id")
    )
    """)
    
    cursor.execute("""
	CREATE TABLE "DefaultCommunityGoldEligiblity" (
    "category" TEXT,
    "map" TEXT,
    "eligible" INTEGER NOT NULL,
    PRIMARY KEY("category", "map"),
    FOREIGN KEY("category") REFERENCES "FullGameCategories"("id"),
    FOREIGN KEY("map") REFERENCES "Maps"("id")
    )


	""")
    
    cursor.execute("""
	CREATE TABLE "CommunityGoldEligibility" (
    "user" INTEGER,
    "category" TEXT,
    "map" TEXT,
    "eligible" INTEGER NOT NULL,
    PRIMARY KEY("user", "category", "map"),
    FOREIGN KEY("map") REFERENCES "Maps"("id"),
	FOREIGN KEY("user") REFERENCES "Users"("id")
    FOREIGN KEY("category") REFERENCES "FullGameCategories"("id")
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
	FOREIGN KEY("category") REFERENCES "FullGameCategories"("id"),
	FOREIGN KEY("run") REFERENCES "FullGameRuns"("id"),
	PRIMARY KEY("run","category")
    )
    """)
    
    cursor.execute("""
	CREATE TABLE "RunSegments" (
    "run" INTEGER,
	"map" TEXT,
	"time" REAL,
	PRIMARY KEY("run", "map"),
    FOREIGN KEY("run") REFERENCES "FullGameRuns"("id"),
	FOREIGN KEY("map") REFERENCES "Maps"("id")
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
	FOREIGN KEY("category") REFERENCES "IndividualLevelCategories"("id")
    )
    """)
    
    cursor.execute("""
    CREATE TABLE "SprmValues" (
	"category"	TEXT,
	"a"	REAL NOT NULL,
	"b"	REAL NOT NULL,
	"c"	REAL NOT NULL,
	FOREIGN KEY("category") REFERENCES "FullGameCategories"("id"),
	PRIMARY KEY("category")
	)
    """)
    
    cursor.execute("""
	CREATE TABLE "SetupElements" (
		"id" TEXT,
        "name" TEXT NOT NULL UNIQUE,
        "type" TEXT NOT NULL,
        PRIMARY KEY("id")
    )
    """)
    
    cursor.execute("""
	CREATE TABLE "UserSetups" (
                   "user" INTEGER NOT NULL,
                   "element" TEXT NOT NULL,
                   "value" TEXT NOT NULL,
                   FOREIGN KEY("user") REFERENCES "Users"("id"),
                   FOREIGN KEY("element") REFERENCES "SetupElements"("id"),
                   PRIMARY KEY("user", "element")
    )
	""")


if __name__ == "__main__":
    construct("v4.db")
