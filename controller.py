from tkinter import filedialog
from tkinter import messagebox  # Should be in the view
from pathlib import Path

from restDataAccess import Model
from view import View


class Controller:

    MENU_DIRECTORY = "SavedMenus"

    def __init__(self, model, view):
        self.model = model
        self.view = View(view, self)
        self._working_directory = self._get_working_directory()

    @staticmethod
    def _get_working_directory() -> Path:
        """Returns a path to the working directory"""
        return Path(__file__).parent.absolute()

    @staticmethod
    def _get_user_file_open_path() -> Path:
        """
        Opens a filedialog window to the
        user to select a file to open/import.
        Returns a Path to the selected file.
        Returns an empty string if user cancles.
        """
        return Path(filedialog.askopenfilename())

    @staticmethod
    def _verify_pdf(file_path: Path) -> bool:
        """
        Verifies that the given file path
        ends with a .pdf file type.
        """
        if file_path.is_file() and file_path.suffix == ".pdf":
            return True
        else:
            return False

    @staticmethod
    def _build_menu_file_name(menu_path: Path, key: int) -> str:
        """
        Returns a string with the follwing format
        <rest id>_<original file name>.pdf
        """
        return str(key) + "_" + menu_path.stem + ".pdf"

    # This method need to be placed in the View
    # once it is merged into the master branch
    @staticmethod
    def display_error_message(message: str) -> None:
        """
        Displays an error message to the user
        with the given message.
        """
        messagebox.showinfo(
            message=message, icon="error", title="Error",
        )

    # This method need to be placed in the View
    # once it is merged into the master branch
    @staticmethod
    def display_message_window(message: str) -> None:
        """
        Displays an info window to the
        user with the given message
        """
        messagebox.showinfo(message=message)

    @staticmethod
    def import_file(import_file_path: Path, save_file_path: Path) -> None:
        """
        Copies the given file path to the given save_file_path.
        """
        with open(import_file_path, "rb") as in_file:
            with open(save_file_path, "wb") as out_file:
                size_to_read = 1000
                data = in_file.read(size_to_read)
                while len(data) > 0:
                    out_file.write(data)
                    data = in_file.read(size_to_read)

    @staticmethod
    def _validate_login(accounts: list, name: str, password: str) -> int:
        """
        Validates if the given name and password
        match a stored username and password. 
        RETURNS: The account key if match, else
        returns -1.
        """
        if accounts != None and len(accounts) != 0:
            for user in accounts:
                if user["name"].lower() == name.lower():
                    if user["password"] == password:
                        return user["key"]
                    else:
                        return -1
        return -1

    def _update_restaurant_menu(self, rest_id: int, menu: str) -> None:
        """
        Updates a restaurant menu information
        in the model. If the menu argument equals
        None, the menu is deleted from the model.
        """
        if menu != None:
            self.model.update_restaurant(rest_id, {"menu": True})
            self.model.menu_insert(rest_id, menu)
        else:
            self.model.update_restaurant(rest_id, {"menu": False})
            menu = self.model.menu_select(rest_id)
            self.model.delete_menu(menu["key"])

    # ----------------- VIEW CONTROLS -----------------------

    def begin(self) -> None:
        self.view.begin()

    def dispaly_admin_window(self):
        self.view.clear_frame()
        self.view.admin_window()
        restaurants = self.restaurant_info()
        for index, rest in enumerate(restaurants):
            self.view.view1_list_box.insert(index, rest)

    def welcome_screen_next_button(self):
        if self.view.user_type_var.get() != 0:
            self.view.clear_frame()
            self.view.login_window()

    def login_button_press(self):
        invalid_entry = True
        name = self.view.entry_user_name.get()
        password = self.view.entry_password.get()
        if name != "" and password != "":
            user_type = self.view.user_type_var.get()
            if user_type == 1:
                accounts = self.model.admin_select_all()
            elif user_type == 2:
                accounts = self.model.owners_select_all()
            else:
                accounts = self.model.user_select_all()

            account_key = self._validate_login(accounts, name, password)
            if account_key != -1:
                invalid_entry = False
                self.view.clear_frame()
                if user_type == 1:
                    self.dispaly_admin_window()
                elif user_type == 2:
                    # self.view.owner_window()
                    pass
                else:
                    # self.view.user_window()
                    pass
        if invalid_entry:
            self.view.lbl_login_fail["text"] = "Invalid username or password"

    def save_new_user(self):
        pass

    def admin_view_more_info_btn(self):
        # rest_info_list = rest_info_function()
        # below is just a test------
        rest_info_list = list()
        for each in range(12):
            rest_info_list.append(each)
        # ---------------------------
        self.view.clear_frame()
        self.view.restaurant_info_window(rest_info_list)

    def request_menu(self):
        # call a function in model to select a restaurant, return a list with menu
        self.menu_info = list()
        for each in range(3):
            self.menu_info.append(each)
        self.view.clear_frame()
        self.view.menu_window()

    def back_to_welcome(self):
        self.view.clear_frame()
        self.view.init_welcome_window()


    def back_to_admin_view(self):
        self.dispaly_admin_window()

    # ---------------- END OF VIEW CONTROLS ---------------------

    def delete_rest_menu(self, rest_id: int) -> None:
        """
        Deletes the menu for the restaurant with
        the given id number
        """
        self._update_restaurant_menu(rest_id, None)

    # We need to determine out how to get restaurant id from View
    # Can make it a class variable and just access it, or have the
    # button pass the id # to the method.
    def import_rest_menu(self, rest_id: int) -> None:
        """
        Imports a pdf restaurant menu for the
        given restaurant id number. The user
        is prompted with a dialog window to select
        the file to import. The file is then copied
        to the SavedMenus directory.
        """
        # gets the file path of the menu to import
        import_file = self._get_user_file_open_path()
        # verifies that the file is a pdf
        if self._verify_pdf(import_file):
            # generates a new filename for the menu
            new_file_name = self._build_menu_file_name(import_file, rest_id)
            # builds the path to import the menu to
            save_to_path = Path(
                self._working_directory / self.MENU_DIRECTORY / new_file_name
            )
            # imports copies the menu
            self.import_file(import_file, save_to_path)
            # stores the changes to the model
            self._update_restaurant_menu(rest_id, new_file_name)
            self.display_message_window("Import Complete")
        # if the selected file is not a pdf, prompt the user
        elif import_file.is_file():
            self.display_error_message("Invalid file type. Must be a .pdf")

    def validate_owner_login(self, username: str, password: str) -> bool:

        login_info = self.model.owner_select_by_name(username)

        if login_info is None:
            return False

        if login_info["password"] == password:
            return True
        else:
            return False

    def validate_admin_login(
        self, entry_user_name: str, entry_password: str
    ) -> bool:
        username = entry_user_name.get()
        password = entry_password.get()
        login_info = self.model.admin_select(username)

        if login_info is None:
            return False

        if login_info["password"] == password:
            return True
        else:
            return False

    def validate_user_login(self, username: str, password: str) -> bool:

        login_info = self.model.user_select_by_name(username)

        if login_info is None:
            return False

        if login_info["password"] == password:
            return True
        else:
            return False

    def display_owner_id(self) -> list:

        restaurant_list = self.model.restaurants_select_all()
        owner_id_list = []

        for restaurant in restaurant_list:
            owner_id_str = restaurant["id"] + " - " + restaurant["name"]
            owner_id_list.append(owner_id_str)

        return owner_id_list

#   def restaurant_info(self) -> list:
#       restaurant_list = self.model.restaurants_select_all()
#       restaurant_info_list = []

#       for restaurant in restaurant_list:
#
#           restaurant_info_str = restaurant['id'] + ' - ' + restaurant['name'] +
#           ' : '  + restaurant['address'] + restaurant['city'] + restaurant['zip_code']
#
#           restaurant_info_str = (
#               str(restaurant["id"])
#               + " - "
#               + restaurant["name"]
#               + " : "
#               + restaurant["address"]
#               + restaurant["city"]
#               + restaurant["zip_code"]
#           )
#
            restaurant_info_list.append(restaurant_info_str)

        return restaurant_info_list

    # def menu_info(self) -> list:

    #     menu_list = self.model.menus_select_all()
    #     menu_info_list = []

    #     for menu in menu_list:
    #         menu_info_str = restaurant["menu"] # This line gives an error
    #         menu_info_list.append(menu_info_str)


    #    return menu_info_list

   #def more_info(): -> list

   #    list_box.get()

   #    all_info = self.model.restaurants_select_all()

   #    everything_format_str = 'Restuaruant ID: ' + restaurant['id'] '\n' +
   #    'Restuarant name: ' + restaurant['name'] + '\n' +
   #    'Address: '  + restaurant['address'] + '\n' +
   #    'City: ' + restaurant['city'] + '\n' +
   #    'Zip: ' + restaurant['zip_code'] + '\n' +
   #    'Vegetarian: ' + restaurant['vegetarian'] + '\n' +
   #    'Vegan:' + restaurant['vegan'] + '\n' +
   #    'Gluten: ' + restaurant['gluten'] + '\n' +
   #    'Menu: ' + restaurant['menu'] + '\n' +
   #    'Hours: ' + restaurant['hours'] + '\n' +
   #    'Description' + restaurant['description']

   #    return everything_format_str
#
   ##     return menu_info_list

