from tkinter import *


def _admin_place_widget(view):
    lbl_title = Label(
        bg="#0080c0", text="Administrative Function", font=view.font1
    )
    view.admin_view_var = StringVar(value="rest info")
    radiobtn_id = Radiobutton(
        view.window,
        text="Owner ID",
        font="none 12",
        bg="#0080c0",
        activebackground="#0080c0",
        height=2,
        width=8,
        variable=view.admin_view_var,
        value="id",
    )
    radiobtn_info = Radiobutton(
        view.window,
        text="Restaurant Info",
        font="none 12",
        bg="#0080c0",
        activebackground="#0080c0",
        height=2,
        width=15,
        variable=view.admin_view_var,
        value="rest info",
    )
    radiobtn_menu = Radiobutton(
        view.window,
        text="Menus",
        font="none 12",
        bg="#0080c0",
        activebackground="#0080c0",
        height=2,
        width=5,
        variable=view.admin_view_var,
        value="menus",
    )
    btn_list = Button(
        view.window,
        text="Show List",
        font="none 12",
        bg="light grey",
        height=1,
        width=10,
        command=view.controller.btn_list_press,
    )
    lbl_prompt = Label(bg="#0080c0", font="none 12", text="List: ")

    # -----------------start of tony code---------------------

    table_frame = Frame(view.window, relief="groove")
    table_frame.grid(
        row=2, column=0, columnspan=3, padx=(50, 10), pady=10, sticky="we",
    )

    text_scrollbar = Scrollbar(table_frame)
    view.view1_list_box = Listbox(
        table_frame,
        yscrollcommand=text_scrollbar.set,
        font="none 12",
        height=12,
        width=40,
        selectmode="SINGLE",
    )
    text_scrollbar.config(command=view.view1_list_box.yview)

    view.view1_list_box.grid(row=0, column=0, sticky=(N, S, W, E))
    text_scrollbar.grid(row=0, column=1, sticky=(N, S, E))

    # -------------------end of tony code----------------------
    # view.view1_list_box = Listbox(
    #     view.window, font="none 12", height=12, selectmode="SINGLE"
    # )
    btn_info = Button(
        view.window,
        text="More info",
        font="none 12",
        bg="light grey",
        height=1,
        width=10,
        command=view.controller.admin_view_more_info_press,
    )
    btn_menu_update = Button(
        view.window,
        text="Menu Update",
        font="none 12",
        bg="light grey",
        height=1,
        width=12,
        command=view.controller.request_menu,
    )
    btn_exit = Button(
        view.window,
        text="Exit",
        font="none 12",
        bg="light grey",
        height=1,
        width=10,
        command=view.controller.back_to_welcome,
    )

    lbl_title.grid(row=0, columnspan=4, pady=10)
    radiobtn_id.grid(row=1, column=0, padx=(50, 10), pady=10)
    radiobtn_info.grid(row=1, column=1, padx=10, pady=10)
    radiobtn_menu.grid(row=1, column=2, padx=10, pady=10)
    btn_list.grid(
        row=1, column=3, padx=(10, 50), pady=10,
    )
    # view.view1_list_box.grid(
    #     row=2, column=0, columnspan=3, padx=(50, 10), pady=10, sticky="we"
    # )
    btn_info.grid(row=2, column=3, padx=(10, 50))
    btn_menu_update.grid(row=3, column=0, columnspan=3, pady=30)
    btn_exit.grid(row=3, column=3, padx=(10, 50), pady=30)


def _rest_info_place_widget(view):

    lbl_prompt_rest_ID = Label(
        text="Restaurant ID:", font="None 11", bg="#0080c0", height=2
    )
    view.lbl_rest_ID = Label(
        text="", font="None 11", bg="light gray", width=50
    )
    lbl_rest_name = Label(
        text="Restaurant name:", font="None 11", bg="#0080c0", height=2
    )
    view.entry_rest_name = Entry(font="None 11", bg="white", width=57)
    lbl_rest_address = Label(
        text="Address:", font="None 11", bg="#0080c0", height=2
    )
    view.entry_rest_address = Entry(font="None 11", bg="white", width=57)
    lbl_rest_address = Label(
        text="Address:", font="None 11", bg="#0080c0", height=2
    )
    view.entry_rest_address = Entry(font="None 11", bg="white", width=57)
    lbl_rest_city = Label(text="City:", font="None 11", bg="#0080c0", height=2)
    view.entry_rest_city = Entry(font="None 11", bg="white", width=57)
    lbl_rest_state = Label(
        text="State:", font="None 11", bg="#0080c0", height=2
    )
    view.entry_rest_state = Entry(font="None 11", bg="white", width=57)
    lbl_rest_zip = Label(
        text="Zip code:", font="None 11", bg="#0080c0", height=2
    )
    view.entry_rest_zip = Entry(font="None 11", bg="white", width=57)
    lbl_rest_veg = Label(
        text="Vegetarian:", font="None 11", bg="#0080c0", height=2
    )
    view.entry_rest_veg = Entry(font="None 11", bg="white", width=57)
    lbl_rest_vegan = Label(
        text="Vegan:", font="None 11", bg="#0080c0", height=2
    )
    view.entry_rest_vegan = Entry(font="None 11", bg="white", width=57)
    lbl_rest_gluten = Label(
        text="Gluten:", font="None 11", bg="#0080c0", height=2
    )
    view.entry_rest_gluten = Entry(font="None 11", bg="white", width=57)
    lbl_rest_menu = Label(text="Menu:", font="None 11", bg="#0080c0", height=2)
    view.entry_rest_menu = Entry(font="None 11", bg="white", width=57)
    lbl_rest_hours = Label(
        text="Hours:", font="None 11", bg="#0080c0", height=2
    )
    view.entry_rest_hours = Entry(font="None 11", bg="white", width=57)
    lbl_rest_description = Label(
        text="Description:", font="None 11", bg="#0080c0", height=2
    )
    view.entry_rest_description = Entry(font="None 11", bg="white", width=57)
    btn_save_rest = Button(
        text="Save",
        font="None 11",
        bg="light gray",
        command=view.controller.save_rest_press,
    )
    btn_admin_close = Button(
        text="Close",
        font="None 11",
        bg="light gray",
        command=view.controller.back_to_admin_view,
    )

    lbl_prompt_rest_ID.grid(row=0, column=0, padx=10, pady=(20, 0), sticky="w")
    view.lbl_rest_ID.grid(
        row=0, column=1, padx=(0, 20), pady=(20, 0), sticky="w"
    )
    lbl_rest_name.grid(row=1, column=0, padx=10, sticky="w")
    view.entry_rest_name.grid(row=1, column=1, padx=(0, 20), sticky="w")
    lbl_rest_address.grid(row=2, column=0, padx=10, sticky="w")
    view.entry_rest_address.grid(row=2, column=1, sticky="w")
    lbl_rest_address.grid(row=2, column=0, padx=10, sticky="w")
    view.entry_rest_address.grid(row=2, column=1, sticky="w")
    lbl_rest_city.grid(row=3, column=0, padx=10, sticky="w")
    view.entry_rest_city.grid(row=3, column=1, sticky="w")
    lbl_rest_state.grid(row=4, column=0, padx=10, sticky="w")
    view.entry_rest_state.grid(row=4, column=1, sticky="w")
    lbl_rest_zip.grid(row=5, column=0, padx=10, sticky="w")
    view.entry_rest_zip.grid(row=5, column=1, sticky="w")
    lbl_rest_veg.grid(row=6, column=0, padx=10, sticky="w")
    view.entry_rest_veg.grid(row=6, column=1, sticky="w")
    lbl_rest_vegan.grid(row=7, column=0, padx=10, sticky="w")
    view.entry_rest_vegan.grid(row=7, column=1, sticky="w")
    lbl_rest_gluten.grid(row=8, column=0, padx=10, sticky="w")
    view.entry_rest_gluten.grid(row=8, column=1, sticky="w")
    lbl_rest_menu.grid(row=9, column=0, padx=10, sticky="w")
    view.entry_rest_menu.grid(row=9, column=1, sticky="w")
    lbl_rest_hours.grid(row=10, column=0, padx=10, sticky="w")
    view.entry_rest_hours.grid(row=10, column=1, sticky="w")
    lbl_rest_description.grid(row=11, column=0, padx=10, sticky="w")
    view.entry_rest_description.grid(row=11, column=1, sticky="w")
    btn_save_rest.grid(row=12, column=0, columnspan=2, pady=20)
    btn_admin_close.grid(row=13, column=0, columnspan=2, pady=10)


def _menu_place_widget(view):
    lbl_prompt_name = Label(
        text="Restaurant name:", font="None 11", bg="#0080c0", height=2
    )
    lbl_name = Label(
        font="None 11",
        text=view.controller.menu_info[0],
        bg="light gray",
        width=26,
    )
    lbl_prompt_address = Label(
        text="Restaurant address:", font="None 11", bg="#0080c0", height=2
    )
    lbl_address = Label(
        font="None 11",
        text=view.controller.menu_info[1],
        bg="light gray",
        width=26,
    )
    lbl_menu = Label(text="Menu file:", font="None 11", bg="#0080c0", height=2)
    view.entry_menu = Entry(font="None 11", bg="white", width=30)
    view.entry_menu.insert(0, view.controller.menu_info[2])

    btn_save_menu = Button(
        text="Save",
        font="None 11",
        bg="light gray",
        width=10,
        command=view.controller.save_menu_press,
    )
    btn_close_menu = Button(
        text="Close",
        font="None 11",
        bg="light gray",
        width=10,
        command=view.controller.back_to_admin_view,
    )
    lbl_prompt_name.grid(row=0, column=0, padx=5, pady=(10, 0), sticky="w")
    lbl_name.grid(row=0, column=1, pady=(10, 0), sticky="w")
    lbl_prompt_address.grid(row=1, column=0, padx=5, sticky="w")
    lbl_address.grid(row=1, column=1, sticky="w")
    lbl_menu.grid(row=2, column=0, padx=5, sticky="w")
    view.entry_menu.grid(row=2, column=1, sticky="w")
    btn_save_menu.grid(row=3, column=0, columnspan=2, pady=10)
    btn_close_menu.grid(row=4, column=0, columnspan=2, pady=10)
