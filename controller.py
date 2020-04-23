from restDataAccess import Model
from view import View


class Controller(self):

    self.model = Model()

    def validate_owner_login(self, username: str, password: str): -> bool

      login_info = self.model.owner_select_by_name(username)

       if login_info is None:
            return false

        if login_info['password'] == password:
            return True
        else:
            return False


    def validate_admin_login(self, username: str, password: str): -> bool

      login_info = self.model.admin_select_by_name(username)

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
