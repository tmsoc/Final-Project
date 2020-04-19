import sqlite3


class Model:

    REST_TABLE = "restaurant"
    REVIEW_TABLE = "reviews"
    REST_HUB_DB = "rest_hub_data.db"

    sqlite3.register_adapter(bool, int)
    sqlite3.register_converter("BOOLEAN", lambda v: bool(int(v)))

    def __init__(self):
        self.connection = sqlite3.connect(
            ":memory:", detect_types=sqlite3.PARSE_DECLTYPES
        )
        self.connection.row_factory = sqlite3.Row
        self.cur = self.connection.cursor()

        # self.cur.execute(
        #     """CREATE TABLE restaurant (
        #         id INTEGER NOT NULL PRIMARY KEY,
        #         name TEXT NOT NULL,
        #         address TEXT,
        #         city TEXT,
        #         state TEXT,
        #         zip_code TEXT,
        #         veg BOOLEAN,
        #         vegan BOOLEAN,
        #         gluten BOOLEAN,
        #         menu BOOLEAN,
        #         hours TEXT,
        #         description TEXT
        #     )"""
        # )

    @staticmethod
    def _build_insert_string(table: str, param: dict) -> str:
        column_list = list()
        val_list = list()
        for key in param:
            column_list.append(key)
            val_list.append(f":{key}")
        return "INSERT INTO {} ({}) VALUES ({})".format(
            table, ", ".join(column_list), ", ".join(val_list)
        )

    @staticmethod
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

    @staticmethod
    def _build_update_string(id: int, table: str, param: dict) -> str:
        set_param = list()
        for key in param:
            set_param.append(f"{key}=:{key}")
        return "UPDATE {} SET {} WHERE id={}".format(
            table, ", ".join(set_param), id
        )

    @staticmethod
    def _sql_to_dict(data) -> list:
        return [dict(item) for item in data]

    def _verify_id(self, id: int) -> bool:
        with self.connection:
            self.cur.execute(f"SELECT id FROM {self.REST_TABLE}")
        query = self._sql_to_dict(self.cur.fetchall())
        if any(item["id"] == id for item in query):
            return True
        else:
            return False

    def insert_restaurant(self, param: dict) -> None:
        sql_str = self._build_insert_string(self.REST_TABLE, param)
        with self.connection:
            self.cur.execute(sql_str, param)

    def select_rest_by_id(self, id: int):
        with self.connection:
            self.cur.execute(
                f"SELECT * FROM {self.REST_TABLE} WHERE id=:id", {"id": id}
            )
            return dict(self.cur.fetchone())

    def select_rest_by_attribute(
        self, param: dict, sort_by=None, assending=True
    ) -> list:
        sql_str = self._build_select_string(self.REST_TABLE, param)
        if sort_by != None and assending:
            sql_str += f" ORDER BY {sort_by} ASC"
        elif sort_by != None and not assending:
            sql_str += f" ORDER BY {sort_by} DESC"
        with self.connection:
            self.cur.execute(sql_str, param)
        return self._sql_to_dict(self.cur.fetchall())

    def select_all_rest_data(self) -> None:
        with self.connection:
            self.cur.execute(f"SELECT * FROM {self.REST_TABLE}")
        return self._sql_to_dict(self.cur.fetchall())

    def select_rest_names(self, assending=True) -> list:
        if assending:
            sql_str = (
                f"SELECT id, name FROM {self.REST_TABLE} ORDER BY name ASC"
            )
        else:
            sql_str = (
                f"SELECT id, name FROM {self.REST_TABLE} ORDER BY name DESC"
            )
        with self.connection:
            self.cur.execute(sql_str)
        return self._sql_to_dict(self.cur.fetchall())

    def update_restaurant(self, id: int, param: dict) -> bool:
        if self._verify_id(id):
            sql_str = self._build_update_string(id, self.REST_TABLE, param)
            with self.connection:
                self.cur.execute(sql_str, param)
            return True
        else:
            return False

    def delete_restaurant(self, id: int) -> bool:
        if self._verify_id(id):
            with self.connection:
                self.cur.execute(
                    f"DELETE FROM {self.REST_TABLE} WHERE id=:id", {"id": id}
                )
            return True
        else:
            return False


if __name__ == "__main__":

    model = Model()

    data = {
        "name": "Panera Bread",
        "description": "Sandwiches, Salad, Soup",
        "veg": True,
        "vegan": True,
        "gluten": True,
    }
    model.insert_restaurant(data)
    data = {
        "name": "Peet's coffee",
        "description": "Coffee & Tea",
        "veg": True,
        "vegan": True,
        "gluten": False,
    }
    model.insert_restaurant(data)
    data = {
        "name": "Millions of Chicken",
        "description": "Halal, Chicken Shop, Mediterranean",
        "veg": True,
        "vegan": False,
        "gluten": True,
    }
    model.insert_restaurant(data)
    data = {
        "name": "The Crack Shack",
        "description": "Chicken Shop",
        "veg": True,
        "vegan": False,
        "gluten": False,
    }
    model.insert_restaurant(data)
    data = {
        "name": "The Halal Guys",
        "description": "Halal, Middle Eastern Mediterranean",
        "veg": False,
        "vegan": False,
        "gluten": False,
    }
    model.insert_restaurant(data)
    data = {
        "name": "Seabirds Kitchen",
        "description": "Vegan, Vegetarian, Gluten-Free",
        "veg": True,
        "vegan": True,
        "gluten": True,
    }
    model.insert_restaurant(data)

    print("upload complete")

    def print_q(results):
        for item in results:
            print(item)
        print()

    all_rest = model.select_all_rest_data()
    print_q(all_rest)

    filter_s = {"veg": True, "vegan": True, "gluten": True}
    filtered_data = model.select_rest_by_attribute(filter_s)
    print_q(filtered_data)

    names_only = model.select_rest_names()
    print_q(names_only)

    print(model.select_rest_by_id(3))
    new_items = {"city": "Costa Mesa", "state": "CA"}
    model.update_restaurant(3, new_items)
    print(model.select_rest_by_id(3), end="\n\n")

    model.delete_restaurant(1)
    model.delete_restaurant(3)
    model.delete_restaurant(5)
    print_q(model.select_rest_names())
