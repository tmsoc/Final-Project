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

    def display_user_window(self):
        self.view.clear_frame()
        self.view.user_window()

    def display_admin_window(self):
        self.view.clear_frame()
        self.view.admin_window()
        restaurants = self.restaurant_info()
        for index, rest in enumerate(restaurants):
            self.view.view1_list_box.insert(index, rest)

    def welcome_screen_next_button_press(self):
        if self.view.user_type_var.get() != 0:
            self.view.clear_frame()
            self.view.login_window()

    def login_button_press(self):
        invalid_entry = True
        name = self.view.entry_user_name.get()
        password = self.view.entry_password.get()
        if name != "" and password != "":
            user_type = self.view.user_type_var.get()
            if user_type == "admin":
                accounts = self.model.admin_select_all()
            elif user_type == "owner":
                accounts = self.model.owners_select_all()
            else:
                accounts = self.model.user_select_all()

            account_key = self._validate_login(accounts, name, password)
            if account_key != -1:
                invalid_entry = False
                self.view.clear_frame()
                if user_type == "admin":
                    self.display_admin_window()
                elif user_type == "owner":
                    # self.view.owner_window()
                    pass
                else:
                    self.view.user_window()

        if invalid_entry:
            self.view.lbl_login_fail["text"] = "Invalid username or password"

    def save_new_user(self):
        """
        this method retrieves the texts from entry_user_name and 
        entry_password, write these new information to account db
        """
        pass

    def btn_list_press(self):
        """
        returns a list corresponding to the value of admin_view_var, then 
        output the information in the listbox
        if user clicks on radio button ID -> admin_view_var = "id"
           -> show in the list box:
           (line1) owner ID 1 - rest name 1 - rest address 1
           (line2) owner ID 1 - rest name 1 - rest address 2
           (line3) owner ID 1 - rest name 2 - rest address 1
           (line4) owner ID 2 - rest name 1 - rest address 1
           ...
        if user clicks on radio button Restaurant info 
        -> admin_view_var = "rest info"
            -> show in the list box:
            (line1) rest ID - rest name - rest address
            ...
        if user clicks on radio button Menus -> admin_view_var = "menus"
            -> show in the list box:
           (line1) rest name 1 - rest address 1 - menu name 1
           ...
        """
        pass

    def admin_view_more_info_press(self):
        """
        This method creates a list that has all information of one restaurant
        that user clicks on in the listbox, then opens a new window through
        admin_view_restaurant_info_window() in view class, passes this list into
        the method
        
        rest_info_list = list()
        ....
        self.view.clear_frame()
        self.view.admin_view_restaurant_info_window(rest_info_list)
        """
        pass

    def user_view_more_info_press(self):
        """
        This method creates a list that has all information of one restaurant
        that user clicks on in the listbox, then opens a new window through
        user_view_restaurant_info_window() in view class, passes this list into 
        the method
        
        rest_info_list = list()
        ....
        self.view.clear_frame()
        self.view.user_view_restaurant_info_window(rest_info_list)
        """
        pass

    def request_menu(self):
        """
        calls a function in model to select a restaurant, returns a list of
        rest name, address and menu; pass the list to menu_window() in view
        to open menu window
        self.menu_info = list()
        ...
        self.view.clear_frame()
        self.view.menu_window()
        """
        pass

    def save_rest_press(self):
        """
        writes the texts in entries into db
        """
        pass

    def save_menu_press(self):
        """
        updates the new menu file name in entry_menu into menu db
        """
        pass

    def rest_search(self):
        """
        search rest based on entry_rest_name then insert the list of 
        restaurants which have the same name into the listbox
        """
        pass

    def rest_filter(self):
        """
        based on values of 3 variables veggie_var, van_var and gluten_free_var
        create a list of rest ID, rest name and address, display in the listbox
        """
        pass

    def back_to_welcome(self):
        self.view.clear_frame()
        self.view.init_welcome_window()

    def back_to_admin_view(self):
        self.display_admin_window()

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

    def restaurant_info(self) -> list:
        restaurant_list = self.model.restaurants_select_all()
        restaurant_info_list = []

        for restaurant in restaurant_list:
            restaurant_info_str = (
                str(restaurant["id"])
                + " - "
                + restaurant["name"]
                + " : "
                + restaurant["address"]
                + restaurant["city"]
                + restaurant["zip_code"]
            )
            restaurant_info_list.append(restaurant_info_str)

        return restaurant_info_list

    # def menu_info(self) -> list:

    #     menu_list = self.model.menus_select_all()
    #     menu_info_list = []

    #     for menu in menu_list:
    #         menu_info_str = restaurant["menu"] # This line gives an error
    #         menu_info_list.append(menu_info_str)

    #     return menu_info_list
