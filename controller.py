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

    def _get_passwords(self, account_type: str) -> list:
        if account_type == "admin":
            accounts = self.model.admin_select_all()
        elif account_type == "owner":
            accounts = self.model.owners_select_all()
        else:
            accounts = self.model.user_select_all()
        return accounts

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

    # ----------------- VIEW CONTROLS -----------------------

    def begin(self) -> None:
        self.view.begin()

    def display_user_window(self):
        self.view.clear_frame()
        self.view.user_window()

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

    def btn_login_press(self):
        invalid_entry = True
        name = self.view.entry_user_name.get()
        password = self.view.entry_password.get()
        if name != "" and password != "":
            user_type = self.view.user_type_var.get()
            accounts = self._get_passwords(user_type)
            account_key = self._validate_login(accounts, name, password)
            if account_key != -1:
                invalid_entry = False
                self.view.clear_frame()
                if user_type == "admin":
                    self.display_admin_window()
                elif user_type == "owner":
                    # self.view.owner_window()
                    pass
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

        not_valid = True

        if choice == 'id':
            for restaurant in restaurant_names:
                rest_str = (
                    str(restaurant["id"])
                    + " - "
                    + restaurant["name"]
                )
                restaurant_list.append(rest_str)

        elif choice == 'rest info':
            for restaurant in restaurant_names:
                rest_str = (
                    str(restaurant['id'])
                    + ' - '
                    +restaurant["name"]
                    + " - "
                    + restaurant["address"]
                )
                restaurant_list.append(rest_str)

        elif choice == 'menus':
            if menu_list != None:
                for menu in menu_list:
                    not_valid = False
                    rest_str = (
                        str(menus["id"])
                        + " - "
                        + menus["menus"]
                        )
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
            rest_id = selected_rest.split(" ")[0]
            rest_info = self.model.rest_select_by_id(rest_id)
            self.display_rest_detail_window()
            self._insert_rest_info(rest_info)

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
        rest_id = 3

        param_dict = {}
        list_box = self.view.view1_list_box

        name = self.view.entry_rest_name.get()
        address = self.view.entry_rest_address.get()
        address2 = self.view.entry_rest_address.get()
        city = self.view.entry_rest_city.get()
        state = self.view.entry_rest_state.get()
        zip = self.view.entry_rest_zip.get()
        veg = (True if self.view.entry_rest_veg.get() == 'True' else False)
        vegan = (True if self.view.entry_rest_vegan.get() == 'True' else False)
        gluten = (True if self.view.entry_rest_gluten.get() == 'True' else False)
        menu = (True if self.view.entry_rest_menu.get() == 'True' else False)
        hours = self.view.entry_rest_hours.get()
        description = self.view.entry_rest_description.get()

        param_dict = {
        "name" : name,
        'address' : address,
        'city' : city,
        'state' : state,
        'zip_code' : zip,
        'vegetarian' : veg,
        'vegan' : vegan,
        'gluten' : gluten,
        'menu' : menu,
        'hours' : hours,
        'description' : description}

        self.model.update_restaurant(rest_id, param_dict)
        self.back_to_admin_view()


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
        restaurant_list = []

        search = self.view.entry_rest_name.get()
        restaurant_names = self.model.restaurants_select_all()

        not_valid = True
        exists = None

        for restaurant in restaurant_names:
            if search.lower() == restaurant["name"].lower() or search == str(
                restaurant["id"]
            ):
                not_valid = False
                exists = (
                    str(restaurant["id"])
                    + " - "
                    + restaurant["name"]
                    + " : "
                    + restaurant["address"]
                    + f", {restaurant['city']}, "
                    + restaurant["zip_code"]
                )
                restaurant_list.append(exists)
        if not_valid:
            restaurant_list = ["No search results found"]

        results = restaurant_list

        self.view.view3_list_box.delete(0, "end")
        for index, rest in enumerate(results):
            self.view.view3_list_box.insert(index, rest)

    def rest_filter(self):
        """
        based on values of 3 variables veggie_var, van_var and gluten_free_var
        create a list of rest ID, rest name and address, display in the listbox
        """
        restaurant_list = []
        param_dict = {}

        veggie = self.view.veggie_var.get()
        vegan = self.view.vegan_var.get()
        gluten = self.view.gluten_free_var.get()

        if veggie == 0 and vegan == 0 and gluten == 0:
            all_rest_list = self.restaurant_info()
            self.view.view3_list_box.delete(0, "end")
            for index, rest in enumerate(all_rest_list):
                self.view.view3_list_box.insert(index, rest)
        else:
            if veggie == 1:
                param_dict["vegetarian"] = True
            if vegan == 1:
                param_dict["vegan"] = True
            if gluten == 1:
                param_dict["gluten"] = True

            if self.model.rest_select_by_attribute(param_dict) is not None:
                attribute = self.model.rest_select_by_attribute(param_dict)

                for restaurant in attribute:
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
            self.view.view3_list_box.delete(0, "end")
            for index, rest in enumerate(restaurant_list):
                self.view.view3_list_box.insert(index, rest)

    def exit_button_press(self):
        """
        Exit button in restaurant details window
        Gets back to users window
        """
        self.display_user_window()

    def menu_open_button_press(self):
        """
        Opens a menu stored in the menus folder.
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
