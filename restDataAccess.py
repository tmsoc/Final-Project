from pathlib import Path
import sqlite3
import csv

"""
* restaurant table - 
    id - <int> Unique to the restaurant. Populated by the db.
    name - <string>
    address - <string>
    city - <string>
    state - <string>
    zip_code - <string>
    vegetarian - <bool>
    vegan - <bool>
    gluten - <bool>
    menu - <bool>
    hours - <string>
    description - <string>

* reviews table - 
    id - <int>
    user - <string>
    review - <string>
    rating - <int>
    date_time - <string>
    key - <int> Unique to the review. Populated by the db

* menus table - 
    id - <int>
    menu_path - <string>
    key - <int> Unique to the menu. Populated by the db

* user table -
    name - <string>
    password - <string>
    zip_code - <string>
    key - <int> Unique to the user. Populated by the db 

* owner table -
    name - <string>
    password - <string>
    restaurants - <string>
    key - <int> Unique to the owner. Populated by the db


* Admin table - 
    name - <string>
    password - <string>

"""


class Model:
    """
    A class used for storing and accessing restaurant 
    information user and various user information 
    to access the information.

    ...

    Methods
    -------
    insert_restaurant(param: dict)
        Inserts a new restaurant into the restaurant table
    
    insert_review(param: dict)
        Inserts a new review into the reviews table
    
    insert_menu(id: int, path: str)

    select_rest_by_id(id: int)
        Returns a dictionary item for the restaurant with the given id
    
    select_review_by_id(id: int)
        Returns a list of all reviews with the given restaurant id
    
    select_menu(id: int)
        Returns a menu record for the given restaurant id
    
    select_rest_by_attribute(param: dict, sort_by=None, assending=True)
        Returns a list of restaurants based on the given attributes 
        in dictionary form 
    
    select_all_rest_data()
        Return all stored restaurant data from the restaurants table.
    
    select_all_reviews()
        Return a list of all review records

    select_all_menus()
        Returns a list of all menu records
    
    select_rest_names(assending=True)
        Returns a list of all restaurants names with their given id number

    update_restaurant(id: int, param: dict)
        Updates all the given attributes from the param argument to
        the restaurant with the given id number
    
    delete_restaurant(id: int)
        Deletes the restaurant with the given id

    delete_review(key: int)
        Deletes the review  record with the given identification key

    delete_menu(key: int)
        Deletes the menu record with the given identification key

    close_connection()
        Closes the database connection
    
    """

    REST_TABLE = "restaurant"
    REVIEW_TABLE = "reviews"
    MENUS_TABLE = "menus"
    USER_TABLE = "user"

    REST_HUB_DB = "rest_hub_data.db"

    sqlite3.register_adapter(bool, int)
    sqlite3.register_converter("BOOLEAN", lambda v: bool(int(v)))

    def __init__(self):
        self.connection = sqlite3.connect(
            self.REST_HUB_DB, detect_types=sqlite3.PARSE_DECLTYPES
        )
        self.connection.row_factory = sqlite3.Row
        self.cur = self.connection.cursor()

    @staticmethod
    def _build_insert_string(table: str, param: dict) -> str:
        """
        Returns an sql INSERT string with the 
        VALUES from the given dictionary to the 
        specified given table.
        """
        column_list = list()
        val_list = list()
        for key in param:
            # stores a list of keys
            column_list.append(key)
            # stores a list of keys following colons
            val_list.append(f":{key}")
            # builds and returns the string
        return "INSERT INTO {} ({}) VALUES ({})".format(
            table, ", ".join(column_list), ", ".join(val_list)
        )

    @staticmethod
    def _build_select_string(table: str, param: dict) -> str:
        """
        Returns an sql SELECT string with the WHERE
        values provided by the given dictionary to
        the given table.
        """
        where_param = list()
        for key in param:
            # stores a list of keys formatted for the WHERE argument
            where_param.append(f"{key}=:{key}")
            # builds and returns the SELECT string
        return "SELECT * FROM {} WHERE {}".format(
            table, " AND ".join(where_param)
        )

    @staticmethod
    def _build_update_string(id: int, table: str, param: dict) -> str:
        """
        Returns a sql UPDATE string with the SET
        values provided by the given dictionary to
        the specified entry id in the specified table.
        """
        set_param = list()
        for key in param:
            # stores a list of key formatted for the SET argument
            set_param.append(f"{key}=:{key}")
            # builds and returns the UPDATE string
        return "UPDATE {} SET {} WHERE id={}".format(
            table, ", ".join(set_param), id
        )

    @staticmethod
    def _sql_to_dict(data) -> list:
        """
        Returns a sql formatted dictionary item to
        a python standard lib dictionary item
        """
        if len(data) != 0:
            return [dict(item) for item in data]
        else:
            return None

    def _verify_id(self, id: int) -> bool:
        """
        Verifies that the given id is a valid
        id in the sql database.
        """
        # selects a list of all ids from the restaurant table
        with self.connection:
            self.cur.execute(f"SELECT id FROM {self.REST_TABLE}")
        query = self._sql_to_dict(self.cur.fetchall())
        # returns True if id is found in the selected list
        if any(item["id"] == id for item in query):
            return True
        # else returns false
        else:
            return False

    def _verify_key(self, table: str, key: int) -> bool:
        """
        Verifies that the given key exists in
        the given table.
        """
        # queries a all keys from the specified table
        with self.connection:
            self.cur.execute(f"SELECT key FROM {table}")
        query = self._sql_to_dict(self.cur.fetchall())
        # if the key exists in the table returns true
        # else returns false
        if any(item["key"] == key for item in query):
            return True
        else:
            return False

    def _select_all_tables(self) -> list:
        """
        Returns the name of all tables in rest_hub_data.db
        """
        with self.connection:
            self.cur.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            )
        return self._sql_to_dict(self.cur.fetchall())

    def insert_restaurant(self, param: dict) -> None:
        """
        Inserts a new restaurant into the database.
        The param argument is a list of all attributes
        to store with the entry.
        """
        # builds an sql INSERT string
        sql_str = self._build_insert_string(self.REST_TABLE, param)
        # inserts the entry into the restaurant database
        with self.connection:
            self.cur.execute(sql_str, param)

    def insert_review(self, param: dict) -> None:
        """
        Inserts a new review into the reviews table.        
        """
        sql_str = self._build_insert_string(self.REVIEW_TABLE, param)
        with self.connection:
            self.cur.execute(sql_str, param)

    def insert_menu(self, id: int, path: str) -> None:
        """
        Stores the given path with the given restaurant id.
        """
        with self.connection:
            self.cur.execute(
                f"INSERT INTO {self.MENUS_TABLE} (id, menu_path) VALUES (?, ?)",
                (id, path),
            )

    def select_rest_by_id(self, id: int) -> dict:
        """
        Returns a restaurant record with the given
        restaurant id. If the given id is not a valid
        id, returns None.
        """
        # queries the record from id
        with self.connection:
            self.cur.execute(
                f"SELECT * FROM {self.REST_TABLE} WHERE id=:id", {"id": id}
            )
        record = self.cur.fetchone()
        # return the record if found
        if record != None:
            return dict(record)
        # else return None
        else:
            return record

    def select_review_by_id(self, id: int) -> list:
        """
        Returns a list of all reviews with the
        given restaurant id. If no reviews are found,
        returns None.
        """
        with self.connection:
            self.cur.execute(
                f"SELECT * FROM {self.REVIEW_TABLE} WHERE id=:id", {"id": id}
            )
        reviews = self.cur.fetchall()
        return self._sql_to_dict(reviews)

    def select_menu(self, id: int) -> str:
        """
        Returns the menu record for the given
        restaurant id. Returns None if no records
        were found.
        """
        with self.connection:
            self.cur.execute(
                f"SELECT * FROM {self.MENUS_TABLE} WHERE id=:id", {"id": id}
            )
        menu = self.cur.fetchone()
        if menu != None:
            return dict(menu)
        else:
            return menu

    def select_rest_by_attribute(
        self, param: dict, sort_by=None, assending=True
    ) -> list:
        """
        Returns a list of all records with the given
        attributes in the param dictionary. If no record
        are found, returns None. 

        records are returned sorted if the sort_by argument
        is supplied with a specified field.
        """
        # builds the sql SELECT string
        sql_str = self._build_select_string(self.REST_TABLE, param)
        # adds the ORDER BY command if sort_by is specified
        if sort_by != None and assending:
            sql_str += f" ORDER BY {sort_by} ASC"
        elif sort_by != None and not assending:
            sql_str += f" ORDER BY {sort_by} DESC"
        # queries the table
        with self.connection:
            self.cur.execute(sql_str, param)
        # returns the record
        return self._sql_to_dict(self.cur.fetchall())

    def select_all_rest_data(self) -> list:
        """
        Returns a list of all restaurant records. 
        Returns None if no records are found.
        """
        # queries the restaurant database
        with self.connection:
            self.cur.execute(f"SELECT * FROM {self.REST_TABLE}")
        # returns all records
        return self._sql_to_dict(self.cur.fetchall())

    def select_all_reviews(self) -> list:
        """
        Returns a list of all review records.
        Returns None if no records are found.
        """
        with self.connection:
            self.cur.execute(f"SELECT * FROM {self.REVIEW_TABLE}")
        return self._sql_to_dict(self.cur.fetchall())

    def select_all_menus(self) -> list:
        """
        Returns a list of all menu records.
        Returns None if no records are found.
        """
        with self.connection:
            self.cur.execute(f"SELECT * FROM {self.MENUS_TABLE}")
        return self._sql_to_dict(self.cur.fetchall())

    def select_rest_names(self, assending=True) -> list:
        """
        Returns a list of all restaurant records with
        id number sorted by restaurant name.
        Returns None if fo records are found.
        """
        # builds the sql SELECT string
        if assending:
            sql_str = (
                f"SELECT id, name FROM {self.REST_TABLE} ORDER BY name ASC"
            )
        else:
            sql_str = (
                f"SELECT id, name FROM {self.REST_TABLE} ORDER BY name DESC"
            )
        # queries the database
        with self.connection:
            self.cur.execute(sql_str)
        # returns all found records
        return self._sql_to_dict(self.cur.fetchall())

    def update_restaurant(self, id: int, param: dict) -> bool:
        """
        Updates the the restaurant record with the
        given id number the attributes provided by
        the param dictionary. 
        Returns True if update was successful, else
        returns False.
        """
        # Verifies the the id number given is valid
        if self._verify_id(id):
            # builds the sql UPDATE string
            sql_str = self._build_update_string(id, self.REST_TABLE, param)
            # updates the record
            with self.connection:
                self.cur.execute(sql_str, param)
            return True
        else:
            return False

    def delete_restaurant(self, id: int) -> bool:
        """
        Deletes the restaurant record with the
        given id number.
        Returns True if successful, else returns
        False.
        """
        # verifies that the id is valid
        if self._verify_id(id):
            # deletes the record
            with self.connection:
                self.cur.execute(
                    f"DELETE FROM {self.REST_TABLE} WHERE id=:id", {"id": id}
                )
            return True
        else:
            return False

    def delete_review(self, key: int) -> bool:
        """
        Deletes the the review with the given
        key. Returns True if deletion was 
        successful, else returns False
        """
        # verifies that the key is in the given table
        if self._verify_key(self.REVIEW_TABLE, key):
            # deletes the record
            with self.connection:
                self.cur.execute(
                    f"DELETE FROM {self.REVIEW_TABLE} WHERE key=:key",
                    {"key": key},
                )
            return True
        else:
            return False

    def delete_menu(self, key: int) -> bool:
        """
        Deletes the menu record with the
        given key.
        """
        if self._verify_key(self.MENUS_TABLE, key):
            with self.connection:
                self.cur.execute(
                    f"DELETE FROM {self.MENUS_TABLE} WHERE key=:key",
                    {"key": key},
                )
            return True
        else:
            return False

    def close_connection(self) -> None:
        self.connection.close()

    def _d_review_table(self):
        self.cur.execute(f"DROP TABLE {self.REVIEW_TABLE}")


if __name__ == "__main__":

    #     def export_csv(export_data: list, file_path: Path) -> None:
    #         """
    #         Exports a given list of dictionary items
    #         to the provided file path. The file header
    #         is generated from the first element in
    #         the list of dictionary items.
    #         """
    #         keys = export_data[0].keys()
    #         with open(file_path, "w", newline="") as out_file:
    #             writer = csv.DictWriter(out_file, fieldnames=keys)
    #             writer.writeheader()
    #             for item in export_data:
    #                 writer.writerow(item)

    #     model = Model()
    #     all_rest = model.select_all_rest_data()
    #     export_csv(all_rest, "export_data.csv")
    #     print("export complete")

    model = Model()
    # id = 2
    # path = "path 2"
    # model.insert_menu(id, path)

    # model.delete_menu(6)

    menus = model.select_all_menus()
    if menus != None:
        for item in menus:
            print(item)

    list_tables = model._select_all_tables()
    for table in list_tables:
        print(table)
