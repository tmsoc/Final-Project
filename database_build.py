import sqlite3

connection = sqlite3.connect(":memory:", detect_types=sqlite3.PARSE_DECLTYPES)
connection.row_factory = sqlite3.Row
c = connection.cursor()

sqlite3.register_adapter(bool, int)
sqlite3.register_converter("BOOLEAN", lambda v: bool(int(v)))

REST_TABLE = "restaurant"
REVIEW_TABLE = "reviews"

data = {
    "name": "Al Forno Caffe",
    "address": "1525 Mesa Verde E",
    "city": "Costa Mesa",
    "state": "CA",
    "zip_code": "92626",
    "vegetarian": False,
    "vegan": False,
    "gluten": False,
    "menu": None,
    "hours": None,
    "description": "Italian",
}
# model.insert_restaurant(data)


# self.cur.execute(
#     """CREATE TABLE restaurant (
#         id INTEGER NOT NULL PRIMARY KEY,
#         name TEXT NOT NULL,
#         address TEXT,
#         city TEXT,
#         state TEXT,
#         zip_code TEXT,
#         vegetarian BOOLEAN,
#         vegan BOOLEAN,
#         gluten BOOLEAN,
#         menu BOOLEAN,
#         hours TEXT,
#         description TEXT
#     )"""
# )

# self.cur.execute(
#     """CREATE TABLE reviews (
#         id INTEGER,
#         rating INTEGER,
#         review TEXT,
#         date_time TEXT
#     )"""
# )
