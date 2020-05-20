from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from pathlib import Path


class View:

    font1 = "-family {Segoe UI} -size 14 -weight bold -slant " "italic"

    def __init__(self, root, controller):
        self.window = root
        self.controller = controller
        self.window.iconbitmap("Food-Dome.ico")
        self.window.resizable(0, 0)

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

    @staticmethod
    def display_error_message(message: str) -> None:
        """
        Displays an error message to the user
        with the given message.
        """
        messagebox.showinfo(
            message=message, icon="error", title="Error",
        )

    @staticmethod
    def display_message_window(message: str) -> None:
        """
        Displays an info window to the
        user with the given message
        """
        messagebox.showinfo(message=message)

    @staticmethod
    def display_confirm_action(message: str, title: str) -> bool:
        """
        Prompts the to confirm the current
        action. Returns True if user selects
        Yes, Returns False if user selects No.
        """
        return messagebox.askyesno(
            message=message, icon="warning", title=title
        )

    @staticmethod
    def get_user_file_open_path() -> Path:
        """
        Opens a filedialog window to the
        user to select a file to open/import.
        Returns a Path to the selected file.
        Returns an empty string if user cancles.
        """
        return Path(filedialog.askopenfilename())

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
        self.user_type_var = StringVar(value="user")
        radiobtn_admin = Radiobutton(
            top_frame,
            text="Admin",
            font="none 12",
            bg="#0080c0",
            activebackground="#0080c0",
            height=2,
            width=5,
            variable=self.user_type_var,
            value="admin",
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
            value="owner",
        )
        radiobtn_user = Radiobutton(
            top_frame,
            text="Customer",
            font="none 12",
            bg="#0080c0",
            activebackground="#0080c0",
            height=2,
            width=8,
            variable=self.user_type_var,
            value="user",
        )
        btn_next = Button(
            top_frame,
            text="Next",
            font="none 12",
            bg="light gray",
            height=1,
            width=8,
            command=self.controller.welcome_screen_next_button_press,
        )
        welcome_label.place(x=80, y=50)
        welcome_option_label.place(x=65, y=150)
        top_frame.place(x=3, y=3)
        radiobtn_admin.place(x=150, y=180)
        radiobtn_owner.place(x=150, y=210)
        radiobtn_user.place(x=150, y=240)
        btn_next.place(x=210, y=320)

    def _login_place_widget(self):

        lbl_user_name = Label(
            self.window, text="Username:", font="None 11", bg="#0080c0",
        )
        self.entry_user_name = Entry(self.window, font="None 11", width=25,)
        lbl_password = Label(
            self.window, text="Password:", font="None 11", bg="#0080c0"
        )
        self.entry_password = Entry(
            self.window, font="None 11", show="*", width=25,
        )
        self.entry_password.bind(
            "<Return>", self.controller.password_return_press
        )
        button_frame = Frame(self.window, bg="#0080c0")
        btn_login = Button(
            button_frame,
            text="Log in",
            font="none 11",
            command=self.controller.btn_login_press,
        )
        btn_cancel = Button(
            button_frame,
            text="Cancel",
            font="none 11",
            command=self.controller.back_to_welcome,
        )
        self.lbl_login_fail = Label(
            self.window, bg="#0080c0", font="None 11", fg="red",
        )

        button_frame.grid(row=2, column=0, columnspan=3, sticky=(E, W))
        lbl_user_name.grid(row=0, column=0, sticky="w", padx=5, pady=(20, 10))
        self.entry_user_name.grid(row=0, column=1, sticky="we", padx=(0, 50))
        lbl_password.grid(row=1, column=0, sticky="w", padx=5, pady=(10, 30))
        self.entry_password.grid(
            row=1, column=1, sticky="we", padx=(0, 50), pady=(10, 30)
        )
        btn_login.grid(row=0, column=0, padx=70)
        """
        lbl_signup_prompt.grid(
            row=3, column=0, columnspan=2, pady=10, sticky="w"
        )
        btn_signup.grid(row=4, column=0, columnspan=2, pady=5)
        """
        self.lbl_login_fail.grid(row=5, column=0, columnspan=2, pady=10)
        btn_cancel.grid(row=0, column=1, padx=10, sticky=E)

    def _admin_place_widget(self):

        lbl_title = Label(
            bg="#0080c0", text="Administrative Function", font=self.font1
        )
        self.admin_view_var = StringVar(value="rest info")
        radiobtn_id = Radiobutton(
            self.window,
            text="Owner ID",
            font="none 12",
            bg="#0080c0",
            activebackground="#0080c0",
            height=2,
            width=8,
            variable=self.admin_view_var,
            value="id",
            command=self.controller.btn_list_press,
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
            value="rest info",
            command=self.controller.btn_list_press,
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
            value="menus",
            command=self.controller.btn_list_press,
        )
        btn_list = Button(
            self.window,
            text="Show List",
            font="none 12",
            bg="light grey",
            height=1,
            width=10,
            command=self.controller.btn_list_press,
            state="disabled",
        )
        lbl_prompt = Label(bg="#0080c0", font="none 12", text="List: ")

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

        btn_info = Button(
            self.window,
            text="More info",
            font="none 12",
            bg="light grey",
            height=1,
            width=10,
            command=self.controller.admin_view_more_info_press,
        )
        btn_menu_update = Button(
            self.window,
            text="Menu Update",
            font="none 12",
            bg="light grey",
            height=1,
            width=12,
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
        btn_info.grid(row=2, column=3, padx=(10, 50))
        btn_menu_update.grid(row=3, column=0, columnspan=3, pady=30)
        btn_exit.grid(row=3, column=3, padx=(10, 50), pady=30)

    def _menu_place_widget(self):

        lbl_prompt_name = Label(
            text="Restaurant name:", font="None 11", bg="#0080c0", height=2
        )
        lbl_name = Label(
            font="None 11",
            text=self.controller._menu_info[0],
            bg="light gray",
            width=26,
        )
        lbl_prompt_address = Label(
            text="Restaurant address:", font="None 11", bg="#0080c0", height=2
        )
        lbl_address = Label(
            font="None 11",
            text=self.controller._menu_info[1],
            bg="light gray",
            width=26,
        )
        lbl_menu = Label(
            text="Menu file:", font="None 11", bg="#0080c0", height=2
        )
        self.entry_menu = Entry(font="None 11", bg="white", width=30)
        btn_upload_menu = Button(
            text="Select Menu",
            font="None 11",
            bg="light gray",
            width=10,
            command=self.controller.get_path,
        )
        btn_save_menu = Button(
            text="Save",
            font="None 11",
            bg="light gray",
            width=10,
            command=self.controller.save_menu_press,
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
        btn_upload_menu.grid(row=3, column=0, columnspan=2, pady=10)
        btn_save_menu.grid(row=4, column=0, columnspan=2, pady=10)
        btn_close_menu.grid(row=5, column=0, columnspan=2, pady=10)

    def _user_place_widget(self):

        self.veggie_var = IntVar(value=0)
        self.vegan_var = IntVar(value=0)
        self.gluten_free_var = IntVar(value=0)
        lbl_title = Label(
            bg="#0080c0", text="Customer Function", font=self.font1
        )
        lbl_search_prompt = Label(
            bg="#0080c0", text="Restaurant Search:", font="None 11", height=2
        )
        self.search_variable = StringVar()
        self.search_variable.trace_add("write", self.controller.rest_search)
        self.user_search_field = Entry(
            font="None 11",
            bg="white",
            width=35,
            textvariable=self.search_variable,
        )
        btn_search = Button(
            self.window,
            text="Clear",
            font="none 12",
            bg="light grey",
            height=1,
            width=10,
            command=self.controller.user_clear_search,
        )
        table_frame = Frame(self.window, relief="groove")
        text_scrollbar = Scrollbar(table_frame)
        self.view3_list_box = Listbox(
            table_frame,
            yscrollcommand=text_scrollbar.set,
            font="none 12",
            height=12,
            width=48,
            selectmode="SINGLE",
        )
        text_scrollbar.config(command=self.view3_list_box.yview)
        btn_info = Button(
            self.window,
            text="More info",
            font="none 12",
            bg="light grey",
            height=1,
            width=10,
            command=self.controller.user_view_more_info_press,
        )
        checkbtn_veggie = Checkbutton(
            self.window,
            text="Vegetarian",
            font="none 12",
            bg="#0080c0",
            activebackground="#0080c0",
            height=1,
            width=12,
            variable=self.veggie_var,
            command=self.controller.rest_dietary_filter,
        )
        checkbtn_vegan = Checkbutton(
            self.window,
            text="Vegan",
            font="none 12",
            bg="#0080c0",
            activebackground="#0080c0",
            height=1,
            width=12,
            variable=self.vegan_var,
            command=self.controller.rest_dietary_filter,
        )
        checkbtn_gluten_free = Checkbutton(
            self.window,
            text="Gluten-free",
            font="none 12",
            bg="#0080c0",
            activebackground="#0080c0",
            height=1,
            width=12,
            variable=self.gluten_free_var,
            command=self.controller.rest_dietary_filter,
        )
        btn_exit = Button(
            self.window,
            text="Exit",
            font="none 12",
            bg="light grey",
            height=1,
            width=10,
            command=self.controller.exit_user_window,
        )

        lbl_title.grid(row=0, columnspan=4, pady=10)
        lbl_search_prompt.grid(row=1, column=0, padx=10, pady=10)
        self.user_search_field.grid(
            row=1, column=1, columnspan=2, pady=10, sticky="w"
        )
        btn_search.grid(row=1, column=3, padx=10, pady=10)
        table_frame.grid(
            row=2, column=0, columnspan=3, padx=10, pady=10, sticky="we",
        )
        self.view3_list_box.grid(row=0, column=0, sticky=(N, S, W, E))
        text_scrollbar.grid(row=0, column=1, sticky=(N, S, E))
        btn_info.grid(row=2, column=3, padx=10)
        checkbtn_veggie.grid(row=3, column=0, padx=10, pady=10)
        checkbtn_vegan.grid(row=3, column=1, padx=10, pady=10)
        checkbtn_gluten_free.grid(row=3, column=2, padx=10, pady=10)
        btn_exit.grid(row=3, column=3, padx=10, pady=10)

    def _rest_detail_place_widget(self):

        TEXT_WIDTH = 56
        button_frame = Frame(self.window, background="#0080c0")
        reviews_frame = Frame(self.window, background="#0080c0")
        review_scrollbar = Scrollbar(reviews_frame)
        self.rest_info_dispaly = Text(
            self.window,
            background="#66C5F4",
            width=TEXT_WIDTH,
            wrap=WORD,
            height=15,
            state="disabled",
        )
        self.rest_reviews_display = Text(
            reviews_frame,
            yscrollcommand=review_scrollbar.set,
            background="#66C5F4",
            width=TEXT_WIDTH,
            wrap=WORD,
            height=20,
            state="disabled",
        )
        exit_button = Button(
            button_frame,
            text="Exit",
            font="none 12",
            background="light grey",
            width=9,
            command=self.controller.exit_button_press,
        )
        self.menu_open_button = Button(
            button_frame,
            text="Open Menu",
            font="none 12",
            background="light grey",
            width=9,
            state="disabled",
            command=self.controller.menu_open_button_press,
        )
        user_add_review_button = Button(
            button_frame,
            text="Add Review",
            font="none 12",
            background="light grey",
            width=9,
            state="disabled",
            command=self.controller.user_add_review_button_press,
        )

        review_scrollbar.grid(row=0, column=1, sticky=(N, S, E, W))
        review_scrollbar.config(command=self.rest_reviews_display.yview)
        reviews_frame.grid(row=2, column=0, padx=10)

        button_frame.grid(column=1, row=0, sticky=(N, S, E, W))
        self.rest_info_dispaly.grid(
            column=0, row=0, rowspan=2, sticky=(N, S, E, W), padx=10, pady=10
        )
        self.rest_reviews_display.grid(column=0, row=0, sticky=(N, S, E, W))
        exit_button.grid(column=0, row=0, sticky=(N, E, S), pady=10)
        self.menu_open_button.grid(column=0, row=1, sticky=(N, E))
        user_add_review_button.grid(column=0, row=2, sticky=(N, E), pady=10)

        self.rest_info_dispaly.tag_configure(
            "HEADER", justify="left", font=("Helvetica 15 bold")
        )
        self.rest_info_dispaly.tag_configure(
            "INFORMATION", justify="left", font=("Helvetica  12")
        )
        self.rest_info_dispaly.tag_configure(
            "INFO_BOLD", justify="left", font=("Helvetica  12 bold")
        )

        self.rest_reviews_display.tag_configure(
            "HEADER", justify="left", font=("Helvetica 15 bold")
        )
        self.rest_reviews_display.tag_configure(
            "INFORMATION", justify="left", font=("Helvetica  12")
        )
        self.rest_reviews_display.tag_configure(
            "INFO_BOLD", justify="left", font=("Helvetica  12 bold")
        )

    def _owner_place_widget(self):

        lbl_title = Label(
            bg="#0080c0", text="Bussiness Owner Function", font=self.font1
        )
        btn_create_rest = Button(
            self.window,
            text="Create New Restaurant",
            font="none 12",
            bg="light grey",
            height=1,
            width=18,
            command=self.controller.display_new_rest_window,
        )

        table_frame = Frame(self.window, relief="groove")
        text_scrollbar = Scrollbar(table_frame)
        self.view2_list_box = Listbox(
            table_frame,
            yscrollcommand=text_scrollbar.set,
            font="none 12",
            height=12,
            width=55,
            selectmode="SINGLE",
        )
        text_scrollbar.config(command=self.view2_list_box.yview)

        self.view2_list_box.grid(row=0, column=0, sticky=(N, S, W, E))
        text_scrollbar.grid(row=0, column=1, sticky=(N, S, E))

        btn_edit = Button(
            self.window,
            text="Edit Info",
            font="none 12",
            bg="light grey",
            height=1,
            width=8,
            command=self.controller.owner_edit_info_press,
        )
        btn_delete = Button(
            self.window,
            text="Delete",
            font="none 12",
            bg="light grey",
            height=1,
            width=8,
            command=self.controller.delete_rest_press,
        )
        btn_exit = Button(
            self.window,
            text="Exit",
            font="none 12",
            bg="light grey",
            height=1,
            width=8,
            command=self.controller.back_to_welcome,
        )

        lbl_title.grid(row=0, columnspan=4, pady=10)
        btn_create_rest.grid(
            row=1, column=0, columnspan=3, padx=(20, 5), pady=10
        )

        table_frame.grid(
            row=2,
            column=0,
            columnspan=3,
            rowspan=2,
            padx=(20, 10),
            pady=10,
            sticky="we",
        )
        btn_edit.grid(row=2, column=3)
        btn_delete.grid(
            row=3, column=3, columnspan=3, sticky="n",
        )
        btn_exit.grid(row=4, column=3, pady=10)

    def _new_rest_place_widget(self, new_restaurant: bool):

        dietary_options_frame = LabelFrame(
            self.window, text="Dietary Options", bg="#0080c0"
        )

        self.veggie_edit_var = IntVar(value=0)
        self.vegan_edit_var = IntVar(value=0)
        self.gluten_edit_var = IntVar(value=0)

        self.veggie_edit_check_btn = Checkbutton(
            dietary_options_frame,
            text="Vegetarian",
            font="none 12",
            bg="#0080c0",
            activebackground="#0080c0",
            height=1,
            width=12,
            variable=self.veggie_edit_var,
        )
        self.vegan_edit_check_btn = Checkbutton(
            dietary_options_frame,
            text="Vegan",
            font="none 12",
            bg="#0080c0",
            activebackground="#0080c0",
            height=1,
            width=12,
            variable=self.vegan_edit_var,
        )
        self.gluten_edit_check_btn = Checkbutton(
            dietary_options_frame,
            text="Gluten-free",
            font="none 12",
            bg="#0080c0",
            activebackground="#0080c0",
            height=1,
            width=12,
            variable=self.gluten_edit_var,
        )

        self.rest_edit_button_frame = Frame(self.window, background="#0080c0")

        if not new_restaurant:
            lbl_prompt_rest_ID = Label(
                text="Restaurant ID:", font="None 11", bg="#0080c0", height=2
            )
            self.entry_rest_ID = Entry(
                font="None 11", bg="white", width=57, state="readonly"
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
        lbl_rest_description = Label(
            text="Description:", font="None 11", bg="#0080c0", height=2
        )
        self.entry_rest_description = Entry(
            font="None 11", bg="white", width=57
        )

        if new_restaurant:
            lbl_rest_name.grid(
                row=1, column=0, padx=10, pady=(20, 0), sticky="w"
            )
            self.entry_rest_name.grid(
                row=1, column=1, padx=(0, 20), pady=(20, 0), sticky="w"
            )
        else:
            lbl_rest_name.grid(row=1, column=0, padx=10, sticky="w")
            self.entry_rest_name.grid(
                row=1, column=1, padx=(0, 20), sticky="w"
            )

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
        lbl_rest_description.grid(row=6, column=0, padx=10, sticky="w")
        self.entry_rest_description.grid(row=6, column=1, sticky="w")

        if not new_restaurant:
            lbl_prompt_rest_ID.grid(
                row=0, column=0, padx=10, pady=(20, 0), sticky="w"
            )
            self.entry_rest_ID.grid(
                row=0, column=1, padx=(0, 20), pady=(20, 0), sticky="w"
            )
            lbl_rest_menu = Label(
                text="Menu:", font="None 11", bg="#0080c0", height=2
            )
            self.entry_rest_menu = Entry(
                font="None 11", bg="white", width=57, state="readonly",
            )

            lbl_rest_menu.grid(row=7, column=0, padx=10, sticky="w")
            self.entry_rest_menu.grid(row=7, column=1, sticky="w")

        dietary_options_frame.grid(
            row=8, column=0, columnspan=2, pady=10, padx=10, sticky="we"
        )

        self.rest_edit_button_frame.grid(
            row=9, column=0, columnspan=2, pady=10, padx=10, sticky="we"
        )

        dietary_options_frame.columnconfigure(0, weight=1)
        dietary_options_frame.columnconfigure(1, weight=1)
        dietary_options_frame.columnconfigure(2, weight=1)

        self.veggie_edit_check_btn.grid(row=0, column=0, pady=10)
        self.vegan_edit_check_btn.grid(row=0, column=1, pady=0)
        self.gluten_edit_check_btn.grid(row=0, column=2, pady=10)

    def init_welcome_window(self):
        """
        Welcome Window
        """
        self.window.title("Where Should We Eat Tonight?")
        self.window.configure(background="light gray")
        self.window.geometry("500x500")
        self._welcome_place_widget()

    def login_window(self):
        """
        Login Window
        """
        self.window.title("Log in")
        self.window.configure(background="#0080c0")
        self.window.geometry("340x200")
        self._login_place_widget()

    def admin_window(self):
        """
        Main Admin Window
        """
        self.window.title("Admin View")
        self.window.configure(background="#0080c0")
        self.window.geometry("600x500")
        self._admin_place_widget()

    def menu_window(self):
        """
        From Admin Win.
        Window to upload a menu
        Can be used within Rest owner add info
        """
        self.window.title("Menu Update")
        self.window.configure(background="#0080c0")
        self.window.geometry("400x290")
        self._menu_place_widget()

    def user_window(self):
        """
        Main User Window
        """
        self.window.title("Customer View")
        self.window.configure(background="#0080c0")
        self.window.geometry("600x500")
        self._user_place_widget()

    def rest_detail_Window(self):
        """
        From user window
        restaurant details with reviews
        """
        self.window.title("Restaurant Information")
        self.window.geometry("590x600")
        self.window.configure(background="#0080c0")
        self._rest_detail_place_widget()

    def owner_window(self):
        """
        Main Owner window
        """
        self.window.title("Bussiness Owner View")
        self.window.configure(background="#0080c0")
        self.window.geometry("650x450")
        self._owner_place_widget()

    def new_rest_window(self):
        """
        From Owner window
        Window to create new restaurants
        """
        self.window.title("New Restaurant")
        self.window.configure(background="#0080c0")
        self.window.geometry("630x430")
        self._new_rest_place_widget(True)
        self.btn_save_new_rest = Button(
            self.rest_edit_button_frame,
            text="Save",
            font="None 11",
            bg="light gray",
            width=8,
            command=self.controller.save_new_rest_press,
        )
        btn_new_rest_close = Button(
            self.rest_edit_button_frame,
            text="Close",
            font="None 11",
            bg="light gray",
            width=8,
            command=self.controller.back_to_owner_view,
        )
        self.rest_edit_button_frame.columnconfigure(0, weight=1)
        self.rest_edit_button_frame.columnconfigure(1, weight=1)
        self.btn_save_new_rest.grid(row=0, column=0, pady=10)
        btn_new_rest_close.grid(row=0, column=1, pady=10)

    def admin_restaurant_info_window(self):
        """
        From admin window
        Window to modify a restaurant entry
        """
        self.window.title("Restaurant Information")
        self.window.configure(background="#0080c0")
        self.window.geometry("630x500")
        self._new_rest_place_widget(False)
        self.btn_edit_menu = Button(
            self.rest_edit_button_frame,
            text="Add Menu",
            font="None 11",
            bg="light gray",
            width=10,
            command=self.controller.rest_info_edit_menu_press,
        )
        btn_save_rest = Button(
            self.rest_edit_button_frame,
            text="Save",
            font="None 11",
            bg="light gray",
            width=10,
            command=self.controller.save_rest_press,
        )
        btn_new_rest_close = Button(
            self.rest_edit_button_frame,
            text="Close",
            font="None 11",
            bg="light gray",
            width=10,
            command=self.controller.back_to_admin_view,
        )
        self.rest_edit_button_frame.columnconfigure(0, weight=1)
        self.rest_edit_button_frame.columnconfigure(1, weight=1)
        self.rest_edit_button_frame.columnconfigure(2, weight=1)
        self.btn_edit_menu.grid(row=0, column=0, pady=10)
        btn_save_rest.grid(row=0, column=1, pady=10)
        btn_new_rest_close.grid(row=0, column=2, pady=10)

    def owner_restaurant_edit_window(self):
        """
        From Owner window
        Window to modify a restaurant entry
        """
        self.window.title("Restaurant Information")
        self.window.configure(background="#0080c0")
        self.window.geometry("630x500")
        self._new_rest_place_widget(False)
        self.btn_edit_menu = Button(
            self.rest_edit_button_frame,
            text="Add Menu",
            font="None 11",
            bg="light gray",
            width=10,
            command=self.controller.rest_info_edit_menu_press,
        )
        btn_save_rest = Button(
            self.rest_edit_button_frame,
            text="Save",
            font="None 11",
            bg="light gray",
            width=10,
            command=self.controller.save_rest_press,
        )
        btn_new_rest_close = Button(
            self.rest_edit_button_frame,
            text="Close",
            font="None 11",
            bg="light gray",
            width=10,
            command=self.controller.back_to_owner_view,
        )
        self.rest_edit_button_frame.columnconfigure(0, weight=1)
        self.rest_edit_button_frame.columnconfigure(1, weight=1)
        self.rest_edit_button_frame.columnconfigure(2, weight=1)
        self.btn_edit_menu.grid(row=0, column=0, pady=10)
        btn_save_rest.grid(row=0, column=1, pady=10)
        btn_new_rest_close.grid(row=0, column=2, pady=10)
