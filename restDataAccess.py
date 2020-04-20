import sqlite3
from pathlib import Path
import csv

"""
Here is the initial Model build. The data is stored in the external file
"rest_hub_data.db". 

Currently rest_hub_data.db holds data for a table of restaurants and a 
table of reviews. The restaurant table does have initial test data in it, but
the reviews table is still empty.

In the restaurant db, each restaurant has the following fields:
    id - <int> Unique to the restaurant. Populated by the db.
    name - <string>
    address <string>
    city <string>
    state <string>
    zip_code <string>
    vegetarian <bool>
    vegan <bool>
    gluten <bool>
    menu <bool>
    hours <string>
    description <string>


Here is a list of class methods we will be using:
    insert_restaurant(param: dict)
        Inserts a new restaurant into the db. The argument is a
        dictionary of all the attributes of the restaurant.        
        example:    myDict = {"name": "Claim Jumper", "description": "Traditional"}
                    insert_restaurant(myDict)
        The only attribute that has to be in myDict is the 'name' attribute
        DO NOT INCLUDE AN ID.

    select_rest_by_id(id: int)
        Returns a dictionary item for the restaurant with the given id.
    
    select_rest_by_attribute(param: dict, sort_by=None, assending=True)
        Returns a list of restaurant in dictionary form. 
        The param argument will have a list of attributes to select by.
        example:    attDict = {"city": "Costa Mesa", "vegetarian": True}
                    Will return all restaurant that are in Costa Mesa that
                    are vegetarian. 
        If you enter an attribute into the sort_by argument, the returned list will
        be sorted by that filed. Enter assending=False if you want it in desending
        order.

    select_all_rest_data()
        This will return a list of restaurant data in the restaurants table.

    select_rest_names(assending=True)
        Returns a list of all restaurants with their id number.

    update_restaurant(id: int, param: dict)
        Updates any of the attributes for the restaurant with the given
        id number.
        example:    attDict = {"vegetarian": True, "gluten": False}
                    update_restaurant(10, attDict)
                    This will set the vegetarian to True and gluten to False
                    for restaurant with id number 10.

    delete_restaurant(id: int)
        Deletes the restaurant with the given id.

At the bottom of the file, there is a commented export script that
will export all of the db to a csv file in the current directory.
"""


class Model:

    REST_TABLE = "restaurant"
    REVIEW_TABLE = "reviews"
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
        '''
        Returns an sql INSERT string with the 
        VALUES from the given dictionary to the 
        specified given table.
        '''
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
        return f"SELECT * FROM {table}" + " WHERE {}".format(
            " AND ".join(where_param)
        )

    @staticmethod
    def _build_update_string(id: int, table: str, param: dict) -> str:
        '''
        Returns a sql UPDATE string with the SET
        values provided by the given dictionary to
        the specified entry id in the specified table.
        '''
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
        '''
        Returns a sql formatted dictionary item to
        a python standard lib dictionary item
        '''
        if len(data) != 0:
            return [dict(item) for item in data]
        else:
            return None

    def _verify_id(self, id: int) -> bool:
        '''
        Verifies that the given id is a valid
        id in the sql database.
        '''
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

    def select_rest_by_id(self, id: int) -> dict:
        '''
        Returns a restaurant record with the given
        restaurant id. If the given id is not a valid
        id, returns None.
        '''
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

    def select_rest_by_attribute(
        self, param: dict, sort_by=None, assending=True
    ) -> list:
        '''
        Returns a list of all records with the given
        attributes in the param dictionary. If no record
        are found, returns None. 

        records are returned sorted if the sort_by argument
        is supplied with a specified field.
        '''
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
        '''
        Returns a list of all restaurant records. 
        Returns None if no records are found.
        '''
        # queries the restaurant database
        with self.connection:
            self.cur.execute(f"SELECT * FROM {self.REST_TABLE}")
        # returns all records
        return self._sql_to_dict(self.cur.fetchall())

    def select_rest_names(self, assending=True) -> list:
        '''
        Returns a list of all restaurant records with
        id number sorted by restaurant name.
        Returns None if fo records are found.
        '''
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
        '''
        Updates the the restaurant record with the
        given id number the attributes provided by
        the param dictionary. 
        Returns True if update was successful, else
        returns False.
        '''
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
        '''
        Deletes the restaurant record with the
        given id number.
        Returns True if successful, else returns
        False.
        '''
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

    def select_all_tables(self) -> list:
        '''
        Returns the name of all tables in rest_hub_data.db
        '''
        with self.connection:
            self.cur.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            )
        return self._sql_to_dict(self.cur.fetchall())

    def close_connection(self) -> None:
        self.connection.close()


if __name__ == "__main__":
    pass

    # model = Model()
    # all_rest = model.select_all_rest_data()

    # def export_csv(export_data: list, file_path: Path) -> None:
    #     """
    #     Exports a given list of dictionary items
    #     to the provided file path. The file header
    #     is generated from the first element in
    #     the list of dictionary items.
    #     """
    #     keys = export_data[0].keys()
    #     with open(file_path, "w", newline="") as out_file:
    #         writer = csv.DictWriter(out_file, fieldnames=keys)
    #         writer.writeheader()
    #         for item in export_data:
    #             writer.writerow(item)

    # export_csv(all_rest, "export_data.csv")
    # print("export complete")

