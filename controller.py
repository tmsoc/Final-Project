from tkinter import filedialog
from tkinter import messagebox  # Should be in the view
from pathlib import Path
import subprocess

from restDataAccess import Model
from view import View


class Controller:

    MENU_DIRECTORY = "SavedMenus"
    _active_rest_id = int()  # Not used yet
    _active_owner_id = int()  # Not used yet
    _menu_info = list()
    _master_search_list = list()

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
    def _open_local_file(file_path: Path) -> None:
        """
        function used to open files
        """
        subprocess.Popen(str(file_path), shell=True)

    def _validate_login(
        self, account_type: str, name: str, password: str
    ) -> int:
        """
        Validates if the given name and password
        match a stored username and password.
        RETURNS: The account key if match, else
        returns -1.
        """
        account = self._get_password(account_type, name)
        if account != None:
            if account["password"] == password:
                return account["key"]
        return -1

    @staticmethod
    def _rest_dict_to_str(restaurant: dict):
        rest_str = ""
        rest_str += restaurant["name"].lower()
        rest_str += restaurant["address"].lower()
        rest_str += restaurant["city"].lower()
        rest_str += restaurant["state"].lower()
        rest_str += restaurant["zip_code"].lower()
        rest_str += restaurant["description"].lower()
        return rest_str

    @staticmethod
    def _user_rest_format_list(restaurants: list):
        restaurant_list = []
        for restaurant in restaurants:
            format = (
                str(restaurant["id"])
                + " - "
                + restaurant["name"]
                + " : "
                + restaurant["address"]
                + f", {restaurant['city']}, "
                + restaurant["zip_code"]
            )
            restaurant_list.append(format)
        return restaurant_list

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

    def _get_password(self, account_type: str, name: str):
        if account_type == "admin":
            return self.model.admin_select_search_name(name)
        elif account_type == "owner":
            return self.model.owner_select_search_name(name)
        else:  # user type
            return self.model.user_select_search_name(name)

    def _get_list_box_selection(self, list_box) -> str:
        rest_info = None
        index = list_box.curselection()
        if len(index) != 0:
            rest_info = list_box.get(index[0])
        return rest_info

    def _populate_admin_details_table(self, restaurant: dict) -> None:
        self.view.lbl_rest_ID["text"] = restaurant["id"]
        self.view.entry_rest_name.insert(0, restaurant["name"])
        self.view.entry_rest_address.insert(0, restaurant["address"])
        self.view.entry_rest_city.insert(0, restaurant["city"])
        self.view.entry_rest_state.insert(0, restaurant["state"])
        self.view.entry_rest_zip.insert(0, restaurant["zip_code"])
        self.view.entry_rest_veg.insert(0, str(restaurant["vegetarian"]))
        self.view.entry_rest_vegan.insert(0, str(restaurant["vegan"]))
        self.view.entry_rest_gluten.insert(0, str(restaurant["gluten"]))
        self.view.entry_rest_menu.insert(0, str(restaurant["menu"]))
        self.view.entry_rest_hours.insert(0, str(restaurant["hours"]))
        self.view.entry_rest_description.insert(
            0, str(restaurant["description"])
        )

    def _build_dietary_options(self, restaurant):
        if (
            restaurant["vegetarian"] != True
            and restaurant["vegan"] != True
            and restaurant["gluten"] != True
        ):
            dietary_options = "No dietary options available"
        else:
            dietary_options_list = []
            if restaurant["vegetarian"] == True:
                dietary_options_list.append("Vegetarian")
            if restaurant["vegan"] == True:
                dietary_options_list.append("Vegan")
            if restaurant["gluten"] == True:
                dietary_options_list.append("Gluten")
            dietary_options = ", ".join(dietary_options_list)
        return dietary_options

    def _get_average_review(self, rest_id: int) -> str:
        reviews = self.model.review_select_by_id(rest_id)
        if reviews != None:
            sum = 0
            for review in reviews:
                sum += review["rating"]
            average = sum / len(reviews)
            return str(round(average * 2) / 2)
        else:
            return "No Reviews"

    def _insert_rest_gen_info(self, rest, display):
        INDENT = "\n    "
        rest_address = (
            f"""{INDENT}{rest['address']}"""
            f"""{INDENT}{rest['city']}, """
            f"""{rest['state']} {rest['zip_code']}"""
        )
        dietary_options = self._build_dietary_options(rest)
        menu = "Yes" if rest["menu"] else "No"
        avg_review = self._get_average_review(rest["id"])

        self.view.set_display_write_enable(display)
        display.insert("end", rest["name"], "HEADER")
        display.insert("end", f"{INDENT}{rest['description']}", "INFORMATION")
        display.insert("end", rest_address, "INFORMATION")
        display.insert("end", f"{INDENT}Rating: {avg_review}", "INFORMATION")
        display.insert("end", f"\n{INDENT}Dietary Options:", "INFO_BOLD")
        display.insert("end", f"{INDENT}{dietary_options}", "INFORMATION")
        display.insert("end", f"\n{INDENT}Menu on File:", "INFO_BOLD")
        display.insert("end", f"{INDENT}{menu}", "INFORMATION")
        self.view.set_display_read_only(display)

    def _insert_rest_reviews(self, rest_id, display):
        reviews = self.model.review_select_by_id(rest_id)
        self.view.set_display_write_enable(display)
        if reviews != None:
            for review in reviews:
                display.insert("end", f"{review['user']}  ", "HEADER")
                display.insert(
                    "end", f"{review['date_time']}\n", "INFORMATION"
                )
                display.insert(
                    "end", f"{review['rating']} Stars\n", "INFO_BOLD"
                )
                display.insert("end", f"{review['review']}\n\n", "INFORMATION")
        else:
            display.insert("end", "  No Reviews on file", "INFORMATION")
        self.view.set_display_read_only(display)

    def _insert_rest_info(self, rest) -> None:
        rest_info_win = self.view.rest_info_dispaly
        rest_review_win = self.view.rest_reviews_display

        self._insert_rest_gen_info(rest, rest_info_win)
        self._insert_rest_reviews(rest["id"], rest_review_win)

        if rest["menu"] == True:
            self.view.menu_open_button["state"] = "normal"

    # ----------------- VIEW CONTROLS -----------------------

    def begin(self) -> None:
        self.view.begin()

    def display_user_window(self):
        self.view.clear_frame()
        self.view.user_window()
        self.rest_dietary_filter()
        # self.rest_search()

    def display_login_window(self):
        self.view.clear_frame()
        self.view.login_window()

    def display_admin_window(self):
        self.view.clear_frame()
        self.view.admin_window()
        restaurants = self.restaurant_info()
        for index, rest in enumerate(restaurants):
            self.view.view1_list_box.insert(index, rest)

    def display_rest_detail_window(self):
        self.view.clear_frame()
        self.view.rest_detail_Window()

    def welcome_screen_next_button_press(self):
        if self.view.user_type_var.get() == "user":
            self.display_user_window()
        else:
            self.display_login_window()

    def btn_login_press(self, event):
        invalid_entry = True
        name = self.view.entry_user_name.get()
        password = self.view.entry_password.get()
        if name != "" and password != "":
            user_type = self.view.user_type_var.get()
            search_name = name.lower()
            account_key = self._validate_login(
                user_type, search_name, password
            )
            if account_key != -1:
                invalid_entry = False
                self.view.clear_frame()
                if user_type == "admin":
                    self.display_admin_window()
                elif user_type == "owner":
                    # self.view.owner_window()
                    self.back_to_welcome()
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
        restaurant_list = []

        menu_list = self.model.menus_select_all()
        restaurant_names = self.model.restaurants_select_all()
        choice = self.view.admin_view_var.get()

        if choice == "id":
            for restaurant in restaurant_names:
                rest_str = str(restaurant["id"]) + " - " + restaurant["name"]
                restaurant_list.append(rest_str)

        elif choice == "rest info":
            for restaurant in restaurant_names:
                rest_str = (
                    str(restaurant["id"])
                    + " - "
                    + restaurant["name"]
                    + " - "
                    + restaurant["address"]
                )
                restaurant_list.append(rest_str)

        elif choice == "menus":
            not_valid = True
            if menu_list != None:
                for menu in menu_list:
                    not_valid = False
                    rest_str = str(menu["id"]) + " - " + menu["menu_path"]
                    restaurant_list.append(rest_str)
            if not_valid:
                answer = "Sorry no menus available"
                restaurant_list.append(answer)

        self.view.view1_list_box.delete(0, "end")
        results = restaurant_list
        for index, rest in enumerate(results):
            self.view.view1_list_box.insert(index, rest)

    def admin_view_more_info_press(self):
        list_box = self.view.view1_list_box
        selected_rest = self._get_list_box_selection(list_box)
        if selected_rest != None:
            rest_id = selected_rest.split(" ")[0]
            rest_info = self.model.rest_select_by_id(rest_id)
            self.view.clear_frame()
            self.view.restaurant_info_window()
            self._populate_admin_details_table(rest_info)

    def user_view_more_info_press(self):
        """

        """
        list_box = self.view.view3_list_box
        selected_rest = self._get_list_box_selection(list_box)
        if selected_rest != None:
            rest_id = int(selected_rest.split(" ", 1)[0])
            rest_info = self.model.rest_select_by_id(rest_id)
            self.display_rest_detail_window()
            self._insert_rest_info(rest_info)
            self.active_rest_id = rest_id

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
        # self.menu_info = []

        list_box = self.view.view1_list_box
        selected_rest = self._get_list_box_selection(list_box)
        if selected_rest != None:
            rest_id = int(selected_rest.split(" ")[0])
            given_menu = str(self.model.menu_select(rest_id))
            restaurant_info = self.model.rest_select_by_id(rest_id)
            address = restaurant_info["address"]
            self._menu_info.append(rest_id)
            self._menu_info.append(address)
            self._menu_info.append(given_menu)
            self.view.clear_frame()
            self.view.menu_window()

    def save_rest_press(self):
        """
        writes the texts in entries into db
        """
        rest_id = self.view.lbl_rest_ID["text"]

        param_dict = {}
        # list_box = self.view.view1_list_box

        name = self.view.entry_rest_name.get()
        address = self.view.entry_rest_address.get()
        # address2 = self.view.entry_rest_address.get()
        city = self.view.entry_rest_city.get()
        state = self.view.entry_rest_state.get()
        zip_code = self.view.entry_rest_zip.get()
        veg = True if self.view.entry_rest_veg.get() == "True" else False
        vegan = True if self.view.entry_rest_vegan.get() == "True" else False
        gluten = True if self.view.entry_rest_gluten.get() == "True" else False
        # NEED TO SWITCH MENU TO LABEL OR READONLY
        hours = self.view.entry_rest_hours.get()
        description = self.view.entry_rest_description.get()

        param_dict = {
            "name": name,
            "address": address,
            "city": city,
            "state": state,
            "zip_code": zip_code,
            "vegetarian": veg,
            "vegan": vegan,
            "gluten": gluten,
            "hours": hours,
            "description": description,
        }

        self.model.update_restaurant(rest_id, param_dict)
        self.back_to_admin_view()

    def get_path(self):
        uploaded_menu = self._get_user_file_open_path()
        if self._verify_pdf(uploaded_menu):
            self.view.entry_menu.delete(0, "end")
            self.view.entry_menu.insert(0, uploaded_menu)

    def save_menu_press(self):
        """
        updates the new menu file name in entry_menu into menu db
        """
        import_file = Path(self.view.entry_menu.get())
        rest_id = self._menu_info[0]
        already_exists = self.model.menu_select(rest_id)

        if already_exists != None:
            self.delete_rest_menu(rest_id)
            print("false")

        self.import_menu(rest_id, import_file)

        self.back_to_admin_view()

    def rest_search(self, *args):
        search_field = self.view.user_search_field.get().lower()
        search_items = search_field.split(" ")
        results = []
        if search_field == "":
            results = self._master_search_list
        else:
            for rest in self._master_search_list:
                rest_str = self._rest_dict_to_str(rest)
                for item in search_items:
                    if item in rest_str and item != "":
                        results.append(rest)
                        break

        if len(results) == 0:
            rest_list = ["No search results found"]
        else:
            rest_list = self._user_rest_format_list(results)

        self.user_window_print_list(rest_list)

    def user_clear_search(self):
        self.view.user_search_field.delete(0, "end")

    def user_window_print_list(self, item_list: list):
        self.view.view3_list_box.delete(0, "end")
        for index, item in enumerate(item_list):
            self.view.view3_list_box.insert(index, item)

    def rest_dietary_filter(self):
        """
        based on values of 3 variables veggie_var, van_var and gluten_free_var
        create a list of rest ID, rest name and address, display in the listbox
        """
        # restaurant_list = []
        param_dict = {}

        veggie = self.view.veggie_var.get()
        vegan = self.view.vegan_var.get()
        gluten = self.view.gluten_free_var.get()

        if veggie == 0 and vegan == 0 and gluten == 0:
            self._master_search_list = self.model.restaurants_select_all()
        else:
            if veggie == 1:
                param_dict["vegetarian"] = True
            if vegan == 1:
                param_dict["vegan"] = True
            if gluten == 1:
                param_dict["gluten"] = True

            self._master_search_list = self.model.rest_select_by_attribute(
                param_dict
            )
        self.rest_search()

    def exit_button_press(self):
        """
        Exit button in restaurant details window
        Gets back to users window
        """
        self.display_user_window()

    def menu_open_button_press(self):
        """
        Opens a menu of the active restaurant
        stored in the menus folder.
        """
        menu_record = self.model.menu_select(self.active_rest_id)
        menu_path = menu_record["menu_path"]
        abs_menu_path = Path(
            self._working_directory / self.MENU_DIRECTORY / menu_path
        )
        self._open_local_file(abs_menu_path)

    def user_add_review_button_press(self):
        """
        Add review to the user screen
        """
        pass

    def exit_user_window(self):
        self._master_search_list.clear()
        self.back_to_welcome()

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
        import_file = self._get_user_file_open_path()
        self.import_menu(rest_id, import_file)

    def import_menu(self, rest_id: int, file_path: Path) -> None:
        if self._verify_pdf(file_path):
            # generates a new filename for the menu
            new_file_name = self._build_menu_file_name(file_path, rest_id)
            # builds the path to import the menu to
            save_to_path = Path(
                self._working_directory / self.MENU_DIRECTORY / new_file_name
            )
            # imports copies the menu
            self.import_file(file_path, save_to_path)
            # stores the changes to the model
            self._update_restaurant_menu(rest_id, new_file_name)
            self.display_message_window("Import Complete")
        # if the selected file is not a pdf, prompt the user
        elif file_path.is_file():
            self.display_error_message("Invalid file type. Must be a .pdf")

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
                + f", {restaurant['city']}, "
                + restaurant["zip_code"]
            )
            restaurant_info_list.append(restaurant_info_str)

        return restaurant_info_list
