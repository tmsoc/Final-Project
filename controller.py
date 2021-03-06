from datetime import date
from pathlib import Path
import subprocess

from restDataAccess import Model
from view import View


class Controller:

    MENU_DIRECTORY = "SavedMenus"
    _active_rest_id = int()
    _active_account_id = int()
    _active_restaurant_list = list()
    _menu_info = list()

    def __init__(self, model, view):
        self.model = model
        self.view = View(view, self)
        self._working_directory = self._get_working_directory()

    def begin(self) -> None:
        self.view.begin()

    # ----------------- PRIVATE METHODS -----------------------

    @staticmethod
    def _get_working_directory() -> Path:
        """Returns a path to the working directory"""
        return Path(__file__).parent.absolute()

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
        """
        Returns a restaurant records in string
        format.
        """
        rest_str = ""
        rest_str += restaurant["name"].lower()
        rest_str += restaurant["address"].lower()
        rest_str += restaurant["city"].lower()
        rest_str += restaurant["state"].lower()
        rest_str += restaurant["zip_code"].lower()
        rest_str += restaurant["description"].lower()
        return rest_str

    @staticmethod
    def _rest_gen_format_list(restaurants: list):
        """
        Formats a restaurant record to be viewed
        in the general display window.
        """
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
        """
        Returns a list of account username and
        passwords that meet the given searchable
        user name
        """
        if account_type == "admin":
            return self.model.admin_select_search_name(name)
        elif account_type == "owner":
            return self.model.owner_select_search_name(name)
        else:  # user type
            return self.model.user_select_search_name(name)

    def _get_list_box_selection(self, list_box) -> str:
        """
        Returns a string of the selected item
        in the specified list box.
        """
        rest_info = None
        index = list_box.curselection()
        if len(index) != 0:
            rest_info = list_box.get(index[0])
        if (
            rest_info == "No Restaurants on File"
            or rest_info == "No search results found"
            or rest_info == "No owners on file"
            or rest_info == "Sorry no menus available"
        ):
            rest_info = None
        return rest_info

    def _populate_rest_details_window(self, restaurant: dict) -> None:
        """
        Popultats all the entry fields with
        the given restaurant record.
        """
        self.view.entry_rest_ID["state"] = "normal"
        self.view.entry_rest_menu["state"] = "normal"

        self.view.entry_rest_ID.insert(0, restaurant["id"])
        self.view.entry_rest_name.insert(0, restaurant["name"])
        self.view.entry_rest_address.insert(0, restaurant["address"])
        self.view.entry_rest_city.insert(0, restaurant["city"])
        self.view.entry_rest_state.insert(0, restaurant["state"])
        self.view.entry_rest_zip.insert(0, restaurant["zip_code"])
        self.view.entry_rest_description.insert(0, restaurant["description"])
        if restaurant["menu"]:
            self.view.entry_rest_menu.insert(0, "On File")
            self.view.btn_edit_menu["text"] = "Delete Menu"
        else:
            self.view.entry_rest_menu.insert(0, "None")

        self.view.entry_rest_ID["state"] = "readonly"
        self.view.entry_rest_menu["state"] = "readonly"

        if restaurant["vegetarian"]:
            self.view.veggie_edit_var.set(1)
        if restaurant["vegan"]:
            self.view.vegan_edit_var.set(1)
        if restaurant["gluten"]:
            self.view.gluten_edit_var.set(1)

    def _build_dietary_options(self, restaurant):
        """
        Builds a string of dietary options for
        the given restaurant.
        """
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
        """
        Calculates the average review rating for
        for the restaurant with the given id number.
        Returns rating in string format rounded to
        the nearest fifth.
        """
        reviews = self.model.review_select_by_id(rest_id)
        if reviews != None:
            sum = 0
            for review in reviews:
                sum += review["rating"]
            average = sum / len(reviews)
            # average review is rounded to nearest fifth
            return str(round(average * 2) / 2)
        else:
            return "No Reviews"

    def _insert_rest_gen_info(self, rest, display):
        """
        Inserts the restaurant information into
        the user restaurant more information window.
        """
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
        """
        Inserts the restaurant review information into
        the user restaurant more information window.
        """
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

    def _read_rest_edit_window(self) -> dict:
        name = self.view.entry_rest_name.get()
        address = self.view.entry_rest_address.get()
        city = self.view.entry_rest_city.get()
        state = self.view.entry_rest_state.get()
        zip_code = self.view.entry_rest_zip.get()
        veg = True if self.view.veggie_edit_var.get() == 1 else False
        vegan = True if self.view.vegan_edit_var.get() == 1 else False
        gluten = True if self.view.gluten_edit_var.get() == 1 else False
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
            "description": description,
        }
        return param_dict

    def _user_window_print_list(self, item_list: list):
        """
        Prints the provided list of strings to
        the general display window list box.
        """
        self.view.view3_list_box.delete(0, "end")
        for index, item in enumerate(item_list):
            self.view.view3_list_box.insert(index, item)

    def _restaurant_validate_entry(self, rest_info: dict) -> bool:
        """
        Verifies that the given restaurant
        information has a valid zip code
        and is not a duplicate restaurant.
        """
        zip_code = rest_info["zip_code"]
        new_rest_city = {"city": rest_info["city"]}
        rest_in_same_city = self.model.rest_select_by_attribute(new_rest_city)
        if not zip_code.isnumeric() or len(zip_code) != 5:
            self.view.display_error_message("Invalid Zip Code")
            return False
        if rest_in_same_city != None:
            for existing in rest_in_same_city:
                if (
                    rest_info["name"] == existing["name"]
                    and rest_info["address"] == existing["address"]
                ):
                    self.view.display_error_message(
                        "Duplicate Restaurant Found"
                    )
                    return False
        return True

    def _add_rest_to_owner_list(self, rest_id: int, owner_key: int):
        """
        Adds the given restaurant id
        to the given owner id record
        """
        owner = self.model.owner_select_by_key(owner_key)
        rest_list = owner["restaurants"]
        if len(rest_list) > 0:
            rest_list += f",{rest_id}"
        else:
            rest_list = str(rest_id)
        self.model.update_owner(owner_key, {"restaurants": rest_list})

    def _delete_menu_file(self, rest_id: int, file_path: Path):
        """
        Deletes a menu file from the saved menus
        directory, updates the database, and prompts
        the user that file has been deleted or that
        the file was not found.
        """
        abs_file_path = Path(
            self._working_directory / self.MENU_DIRECTORY / file_path
        )
        if abs_file_path.is_file():
            self.delete_rest_menu(rest_id)
            abs_file_path.unlink()
            self.view.display_message_window("Menu Deleted")
            return True
        else:
            self.view.display_error_message("Menu File Not Found")
            return False

    def _delete_all_rest_reviews(self, rest_id: int):
        """
        Deletes all reviews for the restaurant
        with the given restaurant id.
        """
        reviews_list = self.model.review_select_by_id(rest_id)
        if reviews_list != None:
            for review in reviews_list:
                self.model.delete_review(review["key"])

    def _delete_rest_from_owner(self, owner_key: int, rest_id: int):
        """
        Removes a restaurant id from an
        owners restaurant id list.
        """
        owner = self.model.owner_select_by_key(owner_key)
        owned_rest_str = owner["restaurants"]
        if len(owned_rest_str) != 0:
            rest_list = owned_rest_str.split(",")
            rest_list.remove(str(rest_id))
            owned_rest_str = ",".join(rest_list)
            self.model.update_owner(owner_key, {"restaurants": owned_rest_str})

    def get_owner_from_rest_id(self, rest_id):
        """
        Returns the owner key of the owner
        that owns the given restaurant id.    
        """
        owner_list = self.model.owners_select_all()
        for owner in owner_list:
            rest_list = owner["restaurants"].split(",")
            if str(rest_id) in rest_list:
                return owner["key"]
        return None

    # ----------------- VIEW WINDOW METHODS -----------------------

    def display_user_window(self):
        self.view.clear_frame()
        self.view.user_window()
        self.rest_dietary_filter()

    def display_login_window(self):
        self.view.clear_frame()
        self.view.login_window()

    def display_admin_window(self):
        self.view.clear_frame()
        self.view.admin_window()
        restaurants = self.restaurant_info()
        for index, rest in enumerate(restaurants):
            self.view.view1_list_box.insert(index, rest)

    def display_owner_window(self):
        self.view.clear_frame()
        self.view.owner_window()

    def display_rest_detail_window(self):
        self.view.clear_frame()
        self.view.rest_detail_Window()

    def display_new_rest_window(self):
        self.view.clear_frame()
        self.view.new_rest_window()

    def back_to_welcome(self):
        self.view.clear_frame()
        self.view.init_welcome_window()

    def back_to_admin_view(self):
        self.display_admin_window()

    def back_to_owner_view(self):
        self.display_owner_window()
        self.display_owner_restaurant_list()

    def display_add_review_window(self):
        self.view.clear_frame()
        self.view.review_window()

    # ----------------- VIEW BUTTON PRESS METHODS -----------------------

    def welcome_screen_next_button_press(self):
        if self.view.user_type_var.get() == "user":
            self.display_user_window()
        else:
            self.display_login_window()

    def password_return_press(self, event):
        self.btn_login_press()

    def btn_login_press(self):
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
                    self._active_account_id = account_key
                    self.display_owner_window()
                    self.display_owner_restaurant_list()
        if invalid_entry:
            self.view.lbl_login_fail["text"] = "Invalid username or password"

    def owner_edit_info_press(self):
        """
        calls restaurant_info_window() to open a new window, entries filled with
        information of the restaurant selected in the listbox
        """
        list_box = self.view.view2_list_box
        selected_rest = self._get_list_box_selection(list_box)
        if selected_rest != None:
            self._active_rest_id = int(selected_rest.split(" ")[0])
            rest_info = self.model.rest_select_by_id(self._active_rest_id)
            self.view.clear_frame()
            self.view.owner_restaurant_edit_window()
            self._populate_rest_details_window(rest_info)

    def delete_rest_press(self):
        """
        open a messagebox to confirm that owner really wants to delete the
        restaurant selected in the listbox. If yes, call a function in model
        to delete the restaurant from dataset
        """
        user_type = self.view.user_type_var.get()
        if user_type == "admin":
            list_box = self.view.view1_list_box
        elif user_type == "owner":
            list_box = self.view.view2_list_box
        selected_rest = self._get_list_box_selection(list_box)
        if selected_rest != None:
            self._active_rest_id = int(selected_rest.split(" ")[0])
            self._active_account_id = self.get_owner_from_rest_id(
                self._active_rest_id
            )
            restaurant = self.model.rest_select_by_id(self._active_rest_id)
            rest_name = restaurant["name"]
            title = "Confirm Deletion"
            message = (
                f"Are you sure you wish to delete\nall records for {rest_name}"
            )
            confirmed = self.view.display_confirm_action(message, title)
            if confirmed:
                # delete menu
                if restaurant["menu"]:
                    menu = self.model.menu_select(self._active_rest_id)
                    abs_menu_path = Path(
                        self._working_directory
                        / self.MENU_DIRECTORY
                        / menu["menu_path"]
                    )
                    abs_menu_path.unlink()
                    self.delete_rest_menu(self._active_rest_id)
                # Delete reviews
                self._delete_all_rest_reviews(self._active_rest_id)
                # delete from owner
                self._delete_rest_from_owner(
                    self._active_account_id, self._active_rest_id
                )
                # delete restaurant
                self.model.delete_restaurant(self._active_rest_id)
                # update screen
                if user_type == "admin":
                    self.display_admin_window()
                elif user_type == "owner":
                    self.display_owner_restaurant_list()

    def btn_list_press(self):
        """
        returns a list corresponding to the value of admin_view_var, then
        output the information in the listbox
        if user clicks on radio button ID -> admin_view_var = "id"
           -> show in the list box:
           (line1) owner ID 1 - rest name 1
           (line2) owner ID 1 - rest name 1
           (line3) owner ID 1 - rest name 2
           (line4) owner ID 2 - rest name 1
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
        output_display_list = []

        menu_list = self.model.menus_select_all()
        restaurant_names = self.model.restaurants_select_all()
        choice = self.view.admin_view_var.get()

        if choice == "id":
            owner_list = self.display_owner_id()
            if owner_list != None:
                output_display_list = owner_list.copy()
            else:
                output_display_list.append("No owners on file")

        elif choice == "rest info":
            for restaurant in restaurant_names:
                rest_str = (
                    str(restaurant["id"])
                    + " - "
                    + restaurant["name"]
                    + " - "
                    + restaurant["address"]
                )
                output_display_list.append(rest_str)

        elif choice == "menus":
            not_valid = True
            if menu_list != None:
                for menu in menu_list:
                    not_valid = False
                    rest_str = str(menu["id"]) + " - " + menu["menu_path"]
                    output_display_list.append(rest_str)
            if not_valid:
                answer = "Sorry no menus available"
                output_display_list.append(answer)

        self.view.view1_list_box.delete(0, "end")
        results = output_display_list
        for index, rest in enumerate(results):
            self.view.view1_list_box.insert(index, rest)

    def admin_view_more_info_press(self):
        """
        Loads the admins restaurant more info
        windows with the selected restaurant.
        """
        admin_view_var = self.view.admin_view_var.get()
        list_box = self.view.view1_list_box
        selected_rest = self._get_list_box_selection(list_box)
        if selected_rest != None and admin_view_var != "id":
            self._active_rest_id = int(selected_rest.split(" ", 1)[0])
            rest_info = self.model.rest_select_by_id(self._active_rest_id)
            self.view.clear_frame()
            self.view.admin_restaurant_info_window()
            self._populate_rest_details_window(rest_info)
        elif selected_rest != None:
            rest_name = {"name": selected_rest.split(" : ")[-1]}
            rest_info = self.model.rest_select_by_attribute(rest_name)[0]
            self.view.clear_frame()
            self.view.admin_restaurant_info_window()
            self._populate_rest_details_window(rest_info)

    def user_view_more_info_press(self):
        """
        Loads the user restaurant more info
        windows with the selected restaurant.
        """
        list_box = self.view.view3_list_box
        selected_rest = self._get_list_box_selection(list_box)
        if selected_rest != None:
            self._active_rest_id = int(selected_rest.split(" ", 1)[0])
            rest_info = self.model.rest_select_by_id(self._active_rest_id)
            self.display_rest_detail_window()
            self._insert_rest_info(rest_info)

    def btn_menu_update_press(self):
        """
        calls a function in model to select a restaurant, returns a list of
        rest name, address and menu; pass the list to menu_window() in view
        """
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
        param_dict = self._read_rest_edit_window()
        self.model.update_restaurant(self._active_rest_id, param_dict)
        self.view.display_message_window("Save Complete")

    def btn_upload_menu_press(self):
        """
        Gets a file path from the user and
        stores the path into the menu field
        in the new menus window in admin
        controls
        """
        uploaded_menu = self.view.get_user_file_open_path()
        if uploaded_menu.is_file():
            self.view.entry_menu["state"] = "normal"
            self.view.entry_menu.delete(0, "end")
            self.view.entry_menu.insert(0, uploaded_menu)
            self.view.entry_menu["state"] = "readonly"

    def save_menu_press(self):
        """
        updates the new menu file name in entry_menu into menu db
        """
        import_file = Path(self.view.entry_menu.get())
        rest_id = self._menu_info[0]
        self.import_menu(rest_id, import_file)
        self.back_to_admin_view()

    def user_clear_search_press(self):
        """Clears the restaurant search entry field"""
        self.view.user_search_field.delete(0, "end")

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
        menu_record = self.model.menu_select(self._active_rest_id)
        menu_path = menu_record["menu_path"]
        abs_menu_path = Path(
            self._working_directory / self.MENU_DIRECTORY / menu_path
        )
        self._open_local_file(abs_menu_path)

    def btn_save_review_press(self):
        """
        Save review to reviews table
        """
        review = self.view.entry_user_review.get("1.0", "end-1c")
        rating = self.view.rating_variable.get()
        name = self.view.entry_username.get()
        rest_id = self._active_rest_id
        today = date.today()
        today = today.strftime("%m/%d/%Y")

        if len(name) != 0 and len(review) != 0 and rating != 0:
            message = "Are you sure you would like to submit this review"
            title = "Review submit"
            confirmation = self.view.display_confirm_action(message, title)
            if confirmation:
                param_dict = {
                    "id": rest_id,
                    "user": name,
                    "review": review,
                    "rating": rating,
                    "date_time": today,
                }
                self.model.review_insert(param_dict)
                rest_info = self.model.rest_select_by_id(self._active_rest_id)
                self.display_rest_detail_window()
                self._insert_rest_info(rest_info)
        else:
            message = "Please enter in all information"
            self.view.display_error_message(message)

    def btn_cancel_review_press(self):
        """
        Returns the reviews page back to the
        user restaurant information page.
        """
        rest_info = self.model.rest_select_by_id(self._active_rest_id)
        self.display_rest_detail_window()
        self._insert_rest_info(rest_info)

    def rest_info_edit_menu_press(self):
        """
        Imports or deletes an menu for the active
        restaurant.

        If no menu is on file, method
        imports a pdf restaurant menu for the
        active restaurant id number. The user
        is prompted with a dialog window to select
        the file to import. The file is then copied
        to the SavedMenus directory.

        If a menu is on file, the menu is deleted
        from the SaveMenus directory.
        """
        restaurant = self.model.rest_select_by_id(self._active_rest_id)
        if restaurant["menu"] == True:
            message = "Are you sure you wish to delete this Menu?"
            title = "Delete File"
            confirmation = self.view.display_confirm_action(message, title)
            if confirmation:
                menu_file = self.model.menu_select(self._active_rest_id)
                complete = self._delete_menu_file(
                    self._active_rest_id, Path(menu_file["menu_path"])
                )
                if complete:
                    self.view.entry_rest_menu["state"] = "normal"
                    self.view.entry_rest_menu.delete(0, "end")
                    self.view.entry_rest_menu.insert(0, "None")
                    self.view.entry_rest_menu["state"] = "readonly"
                    self.view.btn_edit_menu["text"] = "Add Menu"
        else:
            import_file = self.view.get_user_file_open_path()
            complete = self.import_menu(self._active_rest_id, import_file)
            if complete:
                self.view.entry_rest_menu["state"] = "normal"
                self.view.entry_rest_menu.delete(0, "end")
                self.view.entry_rest_menu.insert(0, "On File")
                self.view.entry_rest_menu["state"] = "readonly"
                self.view.btn_edit_menu["text"] = "Delete Menu"

    def exit_user_window_press(self):
        self._active_restaurant_list.clear()
        self.back_to_welcome()

    # ----------------- GENERAL CONTROL METHODS -----------------------

    def get_owner_rest_list(self):
        """
        Returns a list of restaurant ids for
        the from the active account id.
        """
        restaurant_owner = self.model.owner_select_by_key(
            self._active_account_id
        )
        restaurant_list_str = restaurant_owner["restaurants"]
        if restaurant_list_str == "":
            return None
        return restaurant_list_str.split(",")

    def display_owner_restaurant_list(self):
        """
        Inserts the list of restaurants into
        the general display for the active account
        id.
        """
        self._active_restaurant_list.clear()
        self.view.view2_list_box.delete(0, "end")
        restaurant_id_list = self.get_owner_rest_list()
        if restaurant_id_list != None:
            for id in restaurant_id_list:
                restaurant = self.model.rest_select_by_id(id)
                self._active_restaurant_list.append(restaurant)
            rest_list = self._rest_gen_format_list(
                self._active_restaurant_list
            )
        else:
            rest_list = ["No Restaurants on File"]
        for index, rest in enumerate(rest_list):
            self.view.view2_list_box.insert(index, rest)

    def rest_search(self, *args):
        """
        Pulls a list of key words from the
        restaurant search field and prints the
        list of restaurants that contain the
        key words.
        """
        search_field = self.view.user_search_field.get().lower()
        search_items = search_field.split(" ")
        results = []
        if search_field == "":
            results = self._active_restaurant_list
        else:
            for rest in self._active_restaurant_list:
                rest_str = self._rest_dict_to_str(rest)
                for item in search_items:
                    if item in rest_str and item != "":
                        results.append(rest)
                        break

        if len(results) == 0:
            rest_list = ["No search results found"]
        else:
            rest_list = self._rest_gen_format_list(results)

        self._user_window_print_list(rest_list)

    def rest_dietary_filter(self):
        """
        based on values of 3 variables veggie_var, van_var and gluten_free_var
        create a list of rest ID, rest name and address, display in the listbox
        """
        param_dict = {}

        veggie = self.view.veggie_var.get()
        vegan = self.view.vegan_var.get()
        gluten = self.view.gluten_free_var.get()

        if veggie == 0 and vegan == 0 and gluten == 0:
            self._active_restaurant_list = self.model.restaurants_select_all()
        else:
            if veggie == 1:
                param_dict["vegetarian"] = True
            if vegan == 1:
                param_dict["vegan"] = True
            if gluten == 1:
                param_dict["gluten"] = True

            self._active_restaurant_list = self.model.rest_select_by_attribute(
                param_dict
            )
        self.rest_search()

    def save_new_rest_press(self):
        """
        get all information of the new restaurant from entries in the window
        to dataset
        """
        rest_info = self._read_rest_edit_window()
        if (
            rest_info["name"] == ""
            or rest_info["address"] == ""
            or rest_info["city"] == ""
            or rest_info["state"] == ""
            or rest_info["zip_code"] == ""
            or rest_info["description"] == ""
        ):
            self.view.display_error_message("All text fields are required")
        else:
            valid_entry = self._restaurant_validate_entry(rest_info)
            if valid_entry:
                # stores the new restaurant
                self.model.restaurant_insert(rest_info)
                # adds restaurant to owners list of restaurants
                saved_rest = self.model.rest_select_by_attribute(rest_info)
                new_id = int(saved_rest[0]["id"])
                self._add_rest_to_owner_list(new_id, self._active_account_id)
                # prompts the user
                self.view.btn_save_new_rest["state"] = "disabled"
                self.view.display_message_window("Restaurant Saved")

    def delete_rest_menu(self, rest_id: int) -> None:
        """
        Deletes the menu for the restaurant with
        the given id number
        """
        self._update_restaurant_menu(rest_id, None)

    def import_menu(self, rest_id: int, file_path: Path):
        if self._verify_pdf(file_path):
            already_exists = self.model.menu_select(rest_id)
            if already_exists != None:
                self.delete_rest_menu(rest_id)

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
            self.view.display_message_window("Import Complete")
            return True
        # if the selected file is not a pdf, prompt the user
        elif file_path.is_file():
            self.view.display_error_message(
                "Invalid file type. Must be a .pdf"
            )
            return False

    def display_owner_id(self) -> list:
        owner_list = []
        all_owners = self.model.owners_select_all()
        if all_owners != None:
            for owner in all_owners:
                owned_rest_str = owner["restaurants"]
                if len(owned_rest_str) != 0:
                    rest_list = owned_rest_str.split(",")
                    for rest_id in rest_list:
                        restaurant = self.model.rest_select_by_id(rest_id)
                        display_str = (
                            str(owner["key"])
                            + f" - {owner['name']} : "
                            + restaurant["name"]
                        )
                        owner_list.append(display_str)
        else:
            owner_list.append("No owners on file")
        return owner_list

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
