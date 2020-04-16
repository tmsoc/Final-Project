import sqlite3

con = sqlite3.connect(":memory:", detect_types=sqlite3.PARSE_DECLTYPES)
con.row_factory = sqlite3.Row
c = con.cursor()

sqlite3.register_adapter(bool, int)
sqlite3.register_converter("BOOLEAN", lambda v: bool(int(v)))


class Model:
    pass
