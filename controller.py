from restDataAccess import Model

# from view import View


class Controller:
    def __init__(self, model):
        self.model = model

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
                restaurant["id"]
                + " - "
                + restaurant["name"]
                + " : "
                + restaurant["address"]
                + restaurant["city"]
                + restaurant["zip"]
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
