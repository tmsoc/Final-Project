import sqlite3

connection = sqlite3.connect(":memory:", detect_types=sqlite3.PARSE_DECLTYPES)
connection.row_factory = sqlite3.Row
c = connection.cursor()

sqlite3.register_adapter(bool, int)
sqlite3.register_converter("BOOLEAN", lambda v: bool(int(v)))

REST_TABLE = "restaurant"
REVIEW_TABLE = "reviews"

c.execute(
    """CREATE TABLE restaurant (
        id INTEGER NOT NULL PRIMARY KEY,
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
        description TEXT
    )"""
)

# @staticmethod
def _build_insert_string(table: str, param: dict) -> str:
    column_list = list()
    val_list = list()
    for key in param:
        column_list.append(key)
        val_list.append(f":{key}")
    return "INSERT INTO {} ({}) VALUES ({})".format(
        table, ", ".join(column_list), ", ".join(val_list)
    )


# @staticmethod
def _build_select_string(table: str, param: dict) -> str:
    """
    Builds an sql SELECT STRING from the
    given dictionary.
    """
    where_param = list()
    for key in param:
        where_param.append(f"{key}=:{key}")
    return f"SELECT * FROM {table}" + " WHERE {}".format(
        " AND ".join(where_param)
    )


# @staticmethod
def _build_update_string(id: int, table: str, param: dict) -> str:
    set_param = list()
    for key in param:
        set_param.append(f"{key}=:{key}")
    return "UPDATE {} SET {} WHERE id={}".format(
        table, ", ".join(set_param), id
    )


# @staticmethod
def _sql_to_dict(data) -> list:
    return [dict(item) for item in data]


def _verify_id(id: int) -> bool:
    c.execute(f"SELECT id FROM {REST_TABLE}")
    query = _sql_to_dict(c.fetchall())
    if any(item["id"] == id for item in query):
        return True
    else:
        return False


def insert_restaurant(param: dict) -> None:
    sql_str = _build_insert_string(REST_TABLE, param)
    c.execute(sql_str, param)


def select_rest_by_id(id: int):
    c.execute(f"SELECT * FROM {REST_TABLE} WHERE id=:id", {"id": id})
    return dict(c.fetchone())


def select_rest_by_attribute(
    param: dict, sort_by=None, assending=True
) -> list:
    sql_str = _build_select_string(REST_TABLE, param)
    if sort_by != None and assending:
        sql_str += f" ORDER BY {sort_by} ASC"
    elif sort_by != None and not assending:
        sql_str += f" ORDER BY {sort_by} DESC"
    c.execute(sql_str, param)
    return _sql_to_dict(c.fetchall())


def select_all_rest_data() -> None:
    c.execute(f"SELECT * FROM {REST_TABLE}")
    return _sql_to_dict(c.fetchall())


def select_rest_names(assending=True) -> list:
    if assending:
        sql_str = f"SELECT id, name FROM {REST_TABLE} ORDER BY name ASC"
    else:
        sql_str = f"SELECT id, name FROM {REST_TABLE} ORDER BY name DESC"
    c.execute(sql_str)
    return _sql_to_dict(c.fetchall())


def update_restaurant(id: int, param: dict) -> bool:
    if _verify_id(id):
        sql_str = _build_update_string(id, REST_TABLE, param)
        c.execute(sql_str, param)
        return True
    else:
        return False


def delete_restaurant(id: int) -> bool:
    if _verify_id(id):
        c.execute(f"DELETE FROM {REST_TABLE} WHERE id=:id", {"id": id})
        return True
    else:
        return False


data = {
    "name": "Panera Bread",
    "description": "Sandwiches, Salad, Soup",
    "veg": True,
    "vegan": True,
    "gluten": True,
}
insert_restaurant(data)
data = {
    "name": "Peet's coffee",
    "description": "Coffee & Tea",
    "veg": True,
    "vegan": True,
    "gluten": False,
}
insert_restaurant(data)
data = {
    "name": "Millions of Chicken",
    "description": "Halal, Chicken Shop, Mediterranean",
    "veg": True,
    "vegan": False,
    "gluten": True,
}
insert_restaurant(data)
data = {
    "name": "The Crack Shack",
    "description": "Chicken Shop",
    "veg": True,
    "vegan": False,
    "gluten": False,
}
insert_restaurant(data)
data = {
    "name": "The Halal Guys",
    "description": "Halal, Middle Eastern Mediterranean",
    "veg": False,
    "vegan": False,
    "gluten": False,
}
insert_restaurant(data)
data = {
    "name": "Seabirds Kitchen",
    "description": "Vegan, Vegetarian, Gluten-Free",
    "veg": True,
    "vegan": True,
    "gluten": True,
}
insert_restaurant(data)


if __name__ == "__main__":
    # print(_verify_id(10))

    # filter_s = {"veg": True, "vegan": True, "gluten": True}
    # filtered_data = select_rest_by_attribute(filter_s, "name", False)

    # all_data = select_all_rest_data()

    rest_names = select_rest_names(True)

    for rest in rest_names:
        print(rest)
    print(end="\n")

    # new_items = {"city": "Costa Mesa", "state": "CA"}
    # update_restaurant(3, new_items)
    delete_restaurant(4)

    rest_names = select_rest_names(True)
    for rest in rest_names:
        print(rest)
    print(end="\n")

    # print(select_rest_by_id(3))
