from tkinter import *

import winUser as uw
import winWelcome as ww
import winLogIn as lw
import winAdmin as aw


class View:

    font1 = "-family {Segoe UI} -size 14 -weight bold -slant " "italic"

    def __init__(self, root, controller):
        self.window = root
        self.controller = controller

    def begin(self) -> None:
        self.init_welcome_window()

    def clear_frame(self):
        for widget in self.window.winfo_children():
            widget.destroy()

    @staticmethod
    def set_display_read_only(display):
        """Sets the display to ready only"""
        display["state"] = "disabled"

    @staticmethod
    def set_display_write_enable(display):
        """Sets the display to write enable"""
        display["state"] = "normal"

    def init_welcome_window(self):
        self.window.title("Where Should We Eat Tonight?")
        self.window.configure(background="light gray")
        self.window.geometry("500x500")
        self.window.resizable(0, 0)
        ww._welcome_place_widget(self)

    def login_window(self):
        self.window.title("Log in")
        self.window.configure(background="#0080c0")
        self.window.geometry("340x200")
        self.window.resizable(0, 0)
        lw._login_place_widget(self)

    def admin_window(self):
        self.window.title("Admin View")
        self.window.configure(background="#0080c0")
        self.window.geometry("600x500")
        self.window.resizable(0, 0)
        aw._admin_place_widget(self)

    def restaurant_info_window(self):
        self.window.title("Restaurant Information")
        self.window.configure(background="#0080c0")
        self.window.geometry("630x650")
        self.window.resizable(0, 0)
        aw._rest_info_place_widget(self)

    def menu_window(self):
        self.window.title("Menu Update")
        self.window.configure(background="#0080c0")
        self.window.geometry("400x250")
        self.window.resizable(0, 0)
        aw._menu_place_widget(self)

    def user_window(self):
        self.window.title("Customer View")
        self.window.configure(background="#0080c0")
        self.window.geometry("600x500")
        self.window.resizable(0, 0)
        uw._user_place_widget(self)

    def rest_detail_Window(self):
        self.window.title("Restaurant Information")
        self.window.geometry("569x600")
        self.window.configure(background="#0080c0")
        self.window.resizable(0, 0)
        uw._rest_detail_place_widget(self)
