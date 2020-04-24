from restDataAccess import Model
from view import View


class Controller(model):

    self.model = model

    def validate_owner_login(self, username: str, password: str): -> bool

      login_info = self.model.owner_select_by_name(username)

       if login_info is None:
            return false

        if login_info['password'] == password:
            return True
        else:
            return False


    def validate_admin_login(self, entry_user_name: str, entry_password: str): -> bool
    self._select_by_name(self.USER_TABLE, name)
      username = entry_user_name.get()
      password = entry_password.get()
      login_info = self.model.admin_select(username)

       if login_info is None:
            return false

        if login_info['password'] == password:
            return True
        else:
            return False


    def validate_user_login(self, username: str, password: str): -> bool

      login_info = self.model.user_select_by_name(username)

       if login_info is None:
            return false

        if login_info['password'] == password:
            return True
        else:
            return False

    def display_owner_id(): -> list

        restaurant_list = restaurants_select_all()
        owner_id_list = []

        for restaurant in restaurant_list:
            owner_id_str = restaurant['id'] + ' - ' + restaurant['name']
            owner_id_list.append(owner_id_str)

        return owner_id_list


    def resturant_info(): -> list

        restaurant_list = restaurants_select_all()
        restaurant_info_list = []

        for restaurant in restaurant_list:
            restaurant_info_str = restaurant['id'] + ' - ' + restaurant['name'] +
            ' : '  + restaurant['address'] + restaurant['city'] + restaurant['zip_code']
            restaurant_info_list.append(restaurant_info_str)

        return restaurant_info_list


    def menu_info(): -> list

        menu_list = menus_select_all()
        menu_info_list = []

        for menu in menu_list:
            menu_info_str = restaurant['menu']
            menu_info_list.append(menu_info_str)

        return menu_info_list

    def more_info(): -> list

        list_box.get()

        all_info = self.model.restaurants_select_all()

        everything_format_str = 'Restuaruant ID: ' + restaurant['id'] '\n' +
        'Restuarant name: ' + restaurant['name'] + '\n' +
        'Address: '  + restaurant['address'] + '\n' +
        'City: ' + restaurant['city'] + '\n' +
        'Zip: ' + restaurant['zip_code'] + '\n' +
        'Vegetarian: ' + restaurant['vegetarian'] + '\n' +
        'Vegan:' + restaurant['vegan'] + '\n' +
        'Gluten: ' + restaurant['gluten'] + '\n' +
        'Menu: ' + restaurant['menu'] + '\n' +
        'Hours: ' + restaurant['hours'] + '\n' +
        'Description' + restaurant['description']

        return everything_format_str
