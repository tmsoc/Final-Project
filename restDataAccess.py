from pathlib import Path
import sqlite3
import csv


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
    
    insert_user(name: str, password: str, birth_date, zip_code=None)

    insert_owner(self, name: str, password: str, restaurants: str)

    select_rest_by_id(id: int)
        Returns a dictionary item for the restaurant with the given id
    
    select_review_by_id(id: int)
        Returns a list of all reviews with the given restaurant id
    
    select_menu(id: int)
        Returns a menu record for the given restaurant id

    select_user_by_name(name: str)
    
    select_rest_by_attribute(param: dict, sort_by=None, assending=True)
        Returns a list of restaurants based on the given attributes 
        in dictionary form 
    
    select_all_rest_data()
        Return all stored restaurant data from the restaurants table.
    
    select_all_reviews()
        Return a list of all review records

    select_all_menus()
        Returns a list of all menu records
    
    select_all_users()
        Returns a list of all user records
    
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
    
    delete_user(self, key: int)
        Deletes the user record with the given identification key

    close_connection()
        Closes the database connection
    
    """

    REST_TABLE = "restaurant"
    REVIEW_TABLE = "reviews"
    MENUS_TABLE = "menus"
    USER_TABLE = "user"
    OWNER_TABLE = "owner"
    ADMIN_TABLE = "admin"
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

    def _select_all_table_records(self, table: str) -> list:
        """
        Returns a list of all items in a table.
        """
        with self.connection:
            self.cur.execute(f"select * FROM {table}")
        return self._sql_to_dict(self.cur.fetchall())

    def _select_all_tables(self) -> list:
        """
        Returns the name of all tables in rest_hub_data.db
        """
        with self.connection:
            self.cur.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            )
        return self._sql_to_dict(self.cur.fetchall())

    def _select_by_name(self, table: str, name: str):
        """
        Selects a record by name field
        """
        with self.connection:
            self.cur.execute(
                f"SELECT * FROM {table} WHERE name=:name", {"name": name},
            )
        record = self.cur.fetchone()
        if record != None:
            return dict(record)
        else:
            return record

    def _delete_by_key(self, table: str, key: int) -> bool:
        """
        Deletes the record with the given key
        in the specified table. Return True if
        delete was successful, False if failed.
        """
        if self._verify_key(table, key):
            with self.connection:
                self.cur.execute(
                    f"DELETE FROM {table} WHERE key=:key", {"key": key},
                )
            return True
        else:
            return False

    def restaurant_insert(self, param: dict) -> None:
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

    def review_insert(self, param: dict) -> None:
        """
        Inserts a new review into the reviews table.        
        """
        sql_str = self._build_insert_string(self.REVIEW_TABLE, param)
        with self.connection:
            self.cur.execute(sql_str, param)

    def menu_insert(self, id: int, path: str) -> None:
        """
        Stores the given path with the given restaurant id.
        """
        with self.connection:
            self.cur.execute(
                f"INSERT INTO {self.MENUS_TABLE} (id, menu_path) VALUES (?, ?)",
                (id, path),
            )

    def user_insert(
        self, name: str, password: str, birth_date: str, zip_code=None
    ) -> None:
        """Stores a user information"""
        with self.connection:
            self.cur.execute(
                f"""INSERT INTO {self.USER_TABLE} 
                (name, password, birth_date, zip_code) 
                VALUES (?, ?, ?, ?)""",
                (name, password, birth_date, zip_code),
            )

    def owner_insert(self, name: str, password: str, restaurants: str) -> None:
        """Stores a owner information"""
        with self.connection:
            self.cur.execute(
                f"""INSERT INTO {self.OWNER_TABLE} 
                (name, password, restaurants) VALUES (?, ?, ?)""",
                (name, password, restaurants),
            )

    def rest_select_by_id(self, id: int) -> dict:
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

    def review_select_by_id(self, id: int) -> list:
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

    def admin_select(self) -> dict:
        with self.connection:
            self.cur.execute(f"SELECT * FROM {self.ADMIN_TABLE}")
        return dict(self.cur.fetchone())

    def menu_select(self, id: int) -> str:
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

    def user_select_by_name(self, name: str):
        """
        Returns a user record with the given name.
        """
        return self._select_by_name(self.USER_TABLE, name)

    def owner_select_by_name(self, name: str):
        """
        Returns an owner record with the given name.
        """
        return self._select_by_name(self.OWNER_TABLE, name)

    def rest_select_by_attribute(
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

    def restaurants_select_all(self) -> list:
        """
        Returns a list of all restaurant records. 
        Returns None if no records are found.
        """
        return self._select_all_table_records(self.REST_TABLE)

    def reviews_select_all(self) -> list:
        """
        Returns a list of all review records.
        Returns None if no records are found.
        """
        return self._select_all_table_records(self.REVIEW_TABLE)

    def menus_select_all(self) -> list:
        """
        Returns a list of all menu records.
        Returns None if no records are found.
        """
        return self._select_all_table_records(self.MENUS_TABLE)

    def usert_select_all(self) -> list:
        """
        Returns a list of all user records.
        Returns None if no records are found.
        """
        return self._select_all_table_records(self.USER_TABLE)

    def owners_select_all(self) -> list:
        """
        Returns a list of all owner records.
        Returns None if no records are found.
        """
        return self._select_all_table_records(self.OWNER_TABLE)

    def rest_select_names(self, assending=True) -> list:
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
        return self._delete_by_key(self.REVIEW_TABLE, key)

    def delete_menu(self, key: int) -> bool:
        """
        Deletes the menu record with the
        given key.
        """
        return self._delete_by_key(self.MENUS_TABLE, key)

    def delete_user(self, key: int) -> bool:
        """
        Deletes the user record with the
        given key.
        """
        self._delete_by_key(self.USER_TABLE, key)

    def delete_owner(self, key: int) -> bool:
        """
        Deletes the owner record with the
        given key.
        """
        return self._delete_by_key(self.OWNER_TABLE, key)

    def close_connection(self) -> None:
        self.connection.close()


# if __name__ == "__main__":

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
#     all_rest = model.select_all_restaurants()
#     export_csv(all_rest, "export_data.csv")
#     print("export complete")
