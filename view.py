from tkinter import *


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

    def _welcome_place_widget(self):
        top_frame = Frame(
            master=self.window,
            width=495,
            height=495,
            bg="#0080c0",
            relief="groove",
            borderwidth="2",
        )
        welcome_label = Label(
            top_frame,
            text="Where Should We Eat Tonight?",
            font=self.font1,
            bg="#0080ff",
            relief="raised",
            height=2,
            width=30,
            disabledforeground="#a3a3a3",
        )
        welcome_option_label = Label(
            top_frame,
            text="Tell us who you are by selecting one of these options",
            font="none 12",
            bg="#0080c0",
            height=2,
            width=40,
        )
        self.user_type_var = IntVar(value=1)
        radiobtn_admin = Radiobutton(
            top_frame,
            text="Admin",
            font="none 12",
            bg="#0080c0",
            activebackground="#0080c0",
            height=2,
            width=5,
            variable=self.user_type_var,
            value=1,
        )
        radiobtn_owner = Radiobutton(
            top_frame,
            text="Restaurant Owner",
            font="none 12",
            bg="#0080c0",
            activebackground="#0080c0",
            height=2,
            width=14,
            variable=self.user_type_var,
            value=2,
        )
        radiobtn_guest = Radiobutton(
            top_frame,
            text="Customer",
            font="none 12",
            bg="#0080c0",
            activebackground="#0080c0",
            height=2,
            width=8,
            variable=self.user_type_var,
            value=3,
        )
        next_btn = Button(
            top_frame,
            text="Next",
            font="none 12",
            bg="light gray",
            height=1,
            width=8,
            command=self.controller.welcome_screen_next_button,
        )
        welcome_label.place(x=80, y=50)
        welcome_option_label.place(x=65, y=150)
        top_frame.place(x=3, y=3)
        radiobtn_admin.place(x=150, y=180)
        radiobtn_owner.place(x=150, y=210)
        radiobtn_guest.place(x=150, y=240)
        next_btn.place(x=210, y=320)

    def _login_place_widget(self):
        lbl_user_name = Label(
            self.window, text="Username:", font="None 11", bg="#0080c0",
        )
        self.entry_user_name = Entry(self.window, font="None 11", width=15,)
        lbl_password = Label(
            self.window, text="Password:", font="None 11", bg="#0080c0"
        )
        self.entry_password = Entry(
            self.window, font="None 11", show="*", width=15,
        )
        login_button = Button(
            self.window,
            text="Log in",
            font="none 11",
            command=self.controller.login_button_press,
        )
        lbl_signup_prompt = Label(
            self.window,
            text="Haven't got an account? \n \
Enter your username, password and click Sign up",
            font="None 11",
            bg="#0080c0",
            height=2,
        )
        signup_button = Button(
            self.window,
            text="Sign up",
            font="none 11",
            # command=self.controller.save_new_user,
        )
        self.lbl_login_fail = Label(
            self.window, bg="#0080c0", font="None 11", fg="red",
        )

        lbl_user_name.grid(row=0, column=0, sticky="w", padx=5, pady=(20, 10))
        self.entry_user_name.grid(row=0, column=1, sticky="we", padx=(0, 50))
        lbl_password.grid(row=1, column=0, sticky="w", padx=5, pady=(10, 30))
        self.entry_password.grid(
            row=1, column=1, sticky="we", padx=(0, 50), pady=(10, 30)
        )
        login_button.grid(row=2, column=0, columnspan=2)
        lbl_signup_prompt.grid(
            row=3, column=0, columnspan=2, pady=10, sticky="w"
        )
        signup_button.grid(row=4, column=0, columnspan=2)
        self.lbl_login_fail.grid(row=8, column=0, columnspan=2)

    def _admin_place_widget(self):
        self.admin_view_var = IntVar(value=1)
        lbl_title = Label(
            bg="#0080c0", text="Administrative Function", font=self.font1
        )
        radiobtn_id = Radiobutton(
            self.window,
            text="Owner ID",
            font="none 12",
            bg="#0080c0",
            activebackground="#0080c0",
            height=2,
            width=8,
            variable=self.admin_view_var,
            value=1,
        )
        radiobtn_info = Radiobutton(
            self.window,
            text="Restaurant Info",
            font="none 12",
            bg="#0080c0",
            activebackground="#0080c0",
            height=2,
            width=15,
            variable=self.admin_view_var,
            value=2,
        )
        radiobtn_menu = Radiobutton(
            self.window,
            text="Menus",
            font="none 12",
            bg="#0080c0",
            activebackground="#0080c0",
            height=2,
            width=5,
            variable=self.admin_view_var,
            value=3,
        )
        btn_list = Button(
            self.window,
            text="Show List",
            font="none 12",
            bg="light grey",
            height=1,
            width=10,
            # command = a function in controller to return a list corresponding
            # to the value of admin_view_var, then output the information in the
            # listbox
        )
        lbl_prompt = Label(bg="#0080c0", font="none 12", text="List: ")

        # -----------------start of tony code---------------------

        table_frame = Frame(self.window, relief="groove")
        table_frame.grid(
            row=2, column=0, columnspan=3, padx=(50, 10), pady=10, sticky="we",
        )

        text_scrollbar = Scrollbar(table_frame)
        self.view1_list_box = Listbox(
            table_frame,
            yscrollcommand=text_scrollbar.set,
            font="none 12",
            height=12,
            width=40,
            selectmode="SINGLE",
        )
        text_scrollbar.config(command=self.view1_list_box.yview)

        self.view1_list_box.grid(row=0, column=0, sticky=(N, S, W, E))
        text_scrollbar.grid(row=0, column=1, sticky=(N, S, E))

        # -------------------end of tony code----------------------
        # self.view1_list_box = Listbox(
        #     self.window, font="none 12", height=12, selectmode="SINGLE"
        # )
        btn_info = Button(
            self.window,
            text="More info",
            font="none 12",
            bg="light grey",
            height=1,
            width=10,
            command=self.controller.admin_view_more_info_btn,
        )
        btn_update = Button(
            self.window,
            text="Menu Update",
            font="none 12",
            bg="light grey",
            height=1,
            width=12,
            # command = a function in controller to return a list of selected
            # restaurant name, address, and its menu, then open a menu window
            command=self.controller.request_menu,
        )
        btn_exit = Button(
            self.window,
            text="Exit",
            font="none 12",
            bg="light grey",
            height=1,
            width=10,
            command=self.controller.back_to_welcome,
        )

        lbl_title.grid(row=0, columnspan=4, pady=10)
        radiobtn_id.grid(row=1, column=0, padx=(50, 10), pady=10)
        radiobtn_info.grid(row=1, column=1, padx=10, pady=10)
        radiobtn_menu.grid(row=1, column=2, padx=10, pady=10)
        btn_list.grid(
            row=1, column=3, padx=(10, 50), pady=10,
        )
        # self.view1_list_box.grid(
        #     row=2, column=0, columnspan=3, padx=(50, 10), pady=10, sticky="we"
        # )
        btn_info.grid(row=2, column=3, padx=(10, 50))
        btn_update.grid(row=3, column=0, columnspan=3, pady=30)
        btn_exit.grid(row=3, column=3, padx=(10, 50), pady=30)

    def _rest_info_place_widget(self, rest_info_list):

        lbl_prompt_rest_ID = Label(
            text="Restaurant ID:", font="None 11", bg="#0080c0", height=2
        )
        lbl_rest_ID = Label(
            text=rest_info_list[0], font="None 11", bg="light gray", width=50
        )
        lbl_rest_name = Label(
            text="Restaurant name:", font="None 11", bg="#0080c0", height=2
        )
        self.entry_rest_name = Entry(font="None 11", bg="white", width=57)
        lbl_rest_address = Label(
            text="Address:", font="None 11", bg="#0080c0", height=2
        )
        self.entry_rest_address = Entry(font="None 11", bg="white", width=57)
        lbl_rest_address = Label(
            text="Address:", font="None 11", bg="#0080c0", height=2
        )
        self.entry_rest_address = Entry(font="None 11", bg="white", width=57)
        lbl_rest_city = Label(
            text="City:", font="None 11", bg="#0080c0", height=2
        )
        self.entry_rest_city = Entry(font="None 11", bg="white", width=57)
        lbl_rest_state = Label(
            text="State:", font="None 11", bg="#0080c0", height=2
        )
        self.entry_rest_state = Entry(font="None 11", bg="white", width=57)
        lbl_rest_zip = Label(
            text="Zip code:", font="None 11", bg="#0080c0", height=2
        )
        self.entry_rest_zip = Entry(font="None 11", bg="white", width=57)
        lbl_rest_vege = Label(
            text="Vegetarian:", font="None 11", bg="#0080c0", height=2
        )
        self.entry_rest_vege = Entry(font="None 11", bg="white", width=57)
        lbl_rest_vegan = Label(
            text="Vegan:", font="None 11", bg="#0080c0", height=2
        )
        self.entry_rest_vegan = Entry(font="None 11", bg="white", width=57)
        lbl_rest_gluten = Label(
            text="Gluten:", font="None 11", bg="#0080c0", height=2
        )
        self.entry_rest_gluten = Entry(font="None 11", bg="white", width=57)
        lbl_rest_menu = Label(
            text="Menu:", font="None 11", bg="#0080c0", height=2
        )
        self.entry_rest_menu = Entry(font="None 11", bg="white", width=57)
        lbl_rest_hours = Label(
            text="Hours:", font="None 11", bg="#0080c0", height=2
        )
        self.entry_rest_hours = Entry(font="None 11", bg="white", width=57)
        lbl_rest_description = Label(
            text="Description:", font="None 11", bg="#0080c0", height=2
        )
        self.entry_rest_description = Entry(
            font="None 11", bg="white", width=57
        )
        btn_save_rest = Button(
            text="Save",
            font="None 11",
            bg="light gray",
            # command = call a function in controller to write these entries
            # to data
        )
        btn_admin_close = Button(
            text="Close",
            font="None 11",
            bg="light gray",
            command=self.controller.back_to_admin_view,
        )
        self.entry_rest_name.insert(0, str(rest_info_list[1]))
        self.entry_rest_address.insert(0, str(rest_info_list[2]))
        self.entry_rest_city.insert(0, str(rest_info_list[3]))
        self.entry_rest_state.insert(0, str(rest_info_list[4]))
        self.entry_rest_zip.insert(0, str(rest_info_list[5]))
        self.entry_rest_vege.insert(0, str(rest_info_list[6]))
        self.entry_rest_vegan.insert(0, str(rest_info_list[7]))
        self.entry_rest_gluten.insert(0, str(rest_info_list[8]))
        self.entry_rest_menu.insert(0, str(rest_info_list[9]))
        self.entry_rest_hours.insert(0, str(rest_info_list[10]))
        self.entry_rest_description.insert(0, str(rest_info_list[11]))

        lbl_prompt_rest_ID.grid(
            row=0, column=0, padx=10, pady=(20, 0), sticky="w"
        )
        lbl_rest_ID.grid(
            row=0, column=1, padx=(0, 20), pady=(20, 0), sticky="w"
        )
        lbl_rest_name.grid(row=1, column=0, padx=10, sticky="w")
        self.entry_rest_name.grid(row=1, column=1, padx=(0, 20), sticky="w")
        lbl_rest_address.grid(row=2, column=0, padx=10, sticky="w")
        self.entry_rest_address.grid(row=2, column=1, sticky="w")
        lbl_rest_address.grid(row=2, column=0, padx=10, sticky="w")
        self.entry_rest_address.grid(row=2, column=1, sticky="w")
        lbl_rest_city.grid(row=3, column=0, padx=10, sticky="w")
        self.entry_rest_city.grid(row=3, column=1, sticky="w")
        lbl_rest_state.grid(row=4, column=0, padx=10, sticky="w")
        self.entry_rest_state.grid(row=4, column=1, sticky="w")
        lbl_rest_zip.grid(row=5, column=0, padx=10, sticky="w")
        self.entry_rest_zip.grid(row=5, column=1, sticky="w")
        lbl_rest_vege.grid(row=6, column=0, padx=10, sticky="w")
        self.entry_rest_vege.grid(row=6, column=1, sticky="w")
        lbl_rest_vegan.grid(row=7, column=0, padx=10, sticky="w")
        self.entry_rest_vegan.grid(row=7, column=1, sticky="w")
        lbl_rest_gluten.grid(row=8, column=0, padx=10, sticky="w")
        self.entry_rest_gluten.grid(row=8, column=1, sticky="w")
        lbl_rest_menu.grid(row=9, column=0, padx=10, sticky="w")
        self.entry_rest_menu.grid(row=9, column=1, sticky="w")
        lbl_rest_hours.grid(row=10, column=0, padx=10, sticky="w")
        self.entry_rest_hours.grid(row=10, column=1, sticky="w")
        lbl_rest_description.grid(row=11, column=0, padx=10, sticky="w")
        self.entry_rest_description.grid(row=11, column=1, sticky="w")
        btn_save_rest.grid(row=12, column=0, columnspan=2, pady=20)
        btn_admin_close.grid(row=13, column=0, columnspan=2, pady=10)

    def _menu_place_widget(self):
        lbl_prompt_name = Label(
            text="Restaurant name:", font="None 11", bg="#0080c0", height=2
        )
        lbl_name = Label(
            font="None 11",
            text=self.controller.menu_info[0],
            bg="light gray",
            width=26,
        )
        lbl_prompt_address = Label(
            text="Restaurant address:", font="None 11", bg="#0080c0", height=2
        )
        lbl_address = Label(
            font="None 11",
            text=self.controller.menu_info[1],
            bg="light gray",
            width=26,
        )
        lbl_menu = Label(
            text="Menu file:", font="None 11", bg="#0080c0", height=2
        )
        self.entry_menu = Entry(font="None 11", bg="white", width=30)
        self.entry_menu.insert(0, self.controller.menu_info[2])

        btn_save_menu = Button(
            text="Save",
            font="None 11",
            bg="light gray",
            width=10
            # command = call a function in controller to write menu entry
            # to menu data
        )
        btn_close_menu = Button(
            text="Close",
            font="None 11",
            bg="light gray",
            width=10,
            command=self.controller.back_to_admin_view,
        )
        lbl_prompt_name.grid(row=0, column=0, padx=5, pady=(10, 0), sticky="w")
        lbl_name.grid(row=0, column=1, pady=(10, 0), sticky="w")
        lbl_prompt_address.grid(row=1, column=0, padx=5, sticky="w")
        lbl_address.grid(row=1, column=1, sticky="w")
        lbl_menu.grid(row=2, column=0, padx=5, sticky="w")
        self.entry_menu.grid(row=2, column=1, sticky="w")
        btn_save_menu.grid(row=3, column=0, columnspan=2, pady=10)
        btn_close_menu.grid(row=4, column=0, columnspan=2, pady=10)

    def init_welcome_window(self):
        self.window.title("Where Should We Eat Tonight?")
        self.window.configure(background="light gray")
        self.window.geometry("500x500")
        self.window.resizable(0, 0)
        self._welcome_place_widget()

    def login_window(self):
        self.window.title("Log in")
        self.window.configure(background="#0080c0")
        self.window.geometry("340x270")
        self.window.resizable(0, 0)
        self._login_place_widget()

    def admin_window(self):
        self.window.title("Admin View")
        self.window.configure(background="#0080c0")
        self.window.geometry("600x500")
        self.window.resizable(0, 0)
        self._admin_place_widget()

    def restaurant_info_window(self, rest_info_list):
        self.window.title("Restaurant Information")
        self.window.configure(background="#0080c0")
        self.window.geometry("630x650")
        self.window.resizable(0, 0)
        self._rest_info_place_widget(rest_info_list)

    def menu_window(self):
        self.window.title("Menu Update")
        self.window.configure(background="#0080c0")
        self.window.geometry("400x250")
        self.window.resizable(0, 0)
        self._menu_place_widget()


"""
#---------These lines below are used for examining my code------------
class Controller:
    def __init__(self, root):
        self.view = View(root, self)

    def welcome_screen_next_button(self):
        self.view.clear_frame()
        self.view.login_window()

    def login_btn(self):
        choice = self.view.user_type_var.get()
        print(f"From Welcome Screen - var = {choice}")
        if choice == 1:
            self.validate_admin_login()
        elif choice == 2:
            self.validate_owner_login()
        elif choice == 3:
            self.validate_user_login()
        
    def validate_admin_login(self):
        name = self.view.entry_user_name.get()
        password = self.view.entry_password.get()
        print(f"<<< {name} - {password} >>>")
        if name != "python" and password != "python":
            self.view.lbl_login_fail[
                "text"
            ] = 'username and password is "python"'
        else:
            self.view.clear_frame()
            self.view.admin_window()
        
    def validate_owner_login(self):
        name = self.view.entry_user_name.get()
        password = self.view.entry_password.get()
        print(f"<<< {name} - {password} >>>")
        if name != "python" and password != "python":
            self.view.lbl_login_fail[
                "text"
            ] = 'username and password is "python"'
        else:
            self.view.clear_frame()
            self.view.owner_window()

    def validate_user_login(self):
        name = self.view.entry_user_name.get()
        password = self.view.entry_password.get()
        print(f"<<< {name} - {password} >>>")
        if name != "python" and password != "python":
            self.view.lbl_login_fail[
                "text"
            ] = 'username and password is "python" \n \
                New customer? Click on Sign up'
        else:
            self.view.clear_frame()
            self.view.owner_window()

    def back_to_welcome(self):
        self.view.clear_frame()
        self.view.init_welcome_window()

    def save_new_user(self):
        name = self.view.entry_user_name.get()
        password = self.view.entry_password.get()
        #call a function to write name and password into suitable table 
        #corresponding to the value of user_type_var

    def admin_view_more_info_btn(self):
        # rest_info_list = rest_info_function()
        # below is just a test------
        rest_info_list = list()
        for each in range(12):
            rest_info_list.append(each)
        #---------------------------
        self.view.clear_frame()
        self.view.restaurant_info_window(rest_info_list)

    def back_to_admin_view(self):
        self.view.clear_frame()
        self.view.admin_window()

    def request_menu(self):
        #call a function in model to select a restaurant, return a list with menu
        self.menu_info = list()
        for each in range(3):
            self.menu_info.append(each)
        self.view.clear_frame()
        self.view.menu_window()

if __name__ == "__main__":
    root = Tk()
    controller = Controller(root)
    root.mainloop()
    print("Program Ended")
#-----------Those lines above are used for examining my code------------
"""
