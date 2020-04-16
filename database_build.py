import sqlite3

connection = sqlite3.connect(":memory:", detect_types=sqlite3.PARSE_DECLTYPES)

c = connection.cursor()

sqlite3.register_adapter(bool, int)
sqlite3.register_converter("BOOLEAN", lambda v: bool(int(v)))

c.execute(
    """CREATE TABLE restaurant (
        ID INTEGER NOT NULL PRIMARY KEY,
        name TEXT NOT NULL,
        address TEXT,
        city TEXT,
        state TEXT,
        zip_code TEXT,
        veg BOOLEAN,
        vegan BOOLEAN,
        gluten BOOLEAN,
        menu BOOLEAN,
        hours TEXT,
        description TEXT,
    )"""
)
