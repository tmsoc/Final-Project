from tkinter import *


def _user_place_widget(view):
    view.veggie_var = IntVar(value=0)
    # With Check button, value = 0 means unchosen, 1 means chosen
    view.vegan_var = IntVar(value=0)
    view.gluten_free_var = IntVar(value=0)
    lbl_title = Label(bg="#0080c0", text="Customer Function", font=view.font1)
    lbl_search_prompt = Label(
        bg="#0080c0", text="Restaurant name:", font="None 11", height=2
    )
    view.entry_rest_name = Entry(font="None 11", bg="white", width=25)
    btn_search = Button(
        view.window,
        text="Search",
        font="none 12",
        bg="light grey",
        height=1,
        width=10,
        command=view.controller.rest_search,
    )
    table_frame = Frame(view.window, relief="groove")
    text_scrollbar = Scrollbar(table_frame)
    view.view3_list_box = Listbox(
        table_frame,
        yscrollcommand=text_scrollbar.set,
        font="none 12",
        height=12,
        width=40,
        selectmode="SINGLE",
    )
    text_scrollbar.config(command=view.view3_list_box.yview)
    btn_info = Button(
        view.window,
        text="More info",
        font="none 12",
        bg="light grey",
        height=1,
        width=10,
        command=view.controller.user_view_more_info_press,
    )
    checkbtn_veggie = Checkbutton(
        view.window,
        text="Vegetarian",
        font="none 12",
        bg="#0080c0",
        activebackground="#0080c0",
        height=1,
        width=12,
        variable=view.veggie_var,
    )
    checkbtn_vegan = Checkbutton(
        view.window,
        text="Vegan",
        font="none 12",
        bg="#0080c0",
        activebackground="#0080c0",
        height=1,
        width=12,
        variable=view.vegan_var,
    )
    checkbtn_gluten_free = Checkbutton(
        view.window,
        text="Gluten-free",
        font="none 12",
        bg="#0080c0",
        activebackground="#0080c0",
        height=1,
        width=12,
        variable=view.gluten_free_var,
    )
    btn_filter = Button(
        view.window,
        text="Filter",
        font="none 12",
        bg="light grey",
        height=1,
        width=10,
        command=view.controller.rest_filter,
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
    lbl_search_prompt.grid(row=1, column=0, padx=10, pady=10)
    view.entry_rest_name.grid(
        row=1, column=1, columnspan=2, pady=10, sticky="w"
    )
    btn_search.grid(row=1, column=3, padx=10, pady=10)
    table_frame.grid(
        row=2, column=0, columnspan=3, padx=10, pady=10, sticky="we",
    )
    view.view3_list_box.grid(row=0, column=0, sticky=(N, S, W, E))
    text_scrollbar.grid(row=0, column=2, sticky=(N, S, E))
    btn_info.grid(row=2, column=3, padx=10)
    checkbtn_veggie.grid(row=3, column=0, padx=10, pady=10)
    checkbtn_vegan.grid(row=3, column=1, padx=10, pady=10)
    checkbtn_gluten_free.grid(row=3, column=2, padx=10, pady=10)
    btn_filter.grid(row=3, column=3, padx=10, pady=10)
    btn_exit.grid(row=4, column=3, padx=10, pady=10)


def _rest_detail_place_widget(view):
    TEXT_WIDTH = 56
    button_frame = Frame(view.window, background="#0080c0")
    reviews_frame = Frame(view.window, background="#0080c0")
    review_scrollbar = Scrollbar(reviews_frame)
    view.rest_info_dispaly = Text(
        view.window,
        background="#66C5F4",
        width=TEXT_WIDTH,
        wrap=WORD,
        height=15,
        state="disabled",
    )
    view.rest_reviews_display = Text(
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
        background="light grey",
        width=9,
        command=view.controller.exit_button_press,
    )
    menu_open_button = Button(
        button_frame,
        text="Menu",
        background="light grey",
        width=9,
        state="disabled",
        command=view.controller.menu_open_button_press,
    )

    review_scrollbar.grid(row=0, column=1, sticky=(N, S, E, W))
    review_scrollbar.config(command=view.rest_reviews_display.yview)
    reviews_frame.grid(row=2, column=0, padx=10)

    button_frame.grid(column=1, row=0, sticky=(N, S, E, W))
    view.rest_info_dispaly.grid(
        column=0, row=0, rowspan=2, sticky=(N, S, E, W), padx=10, pady=10
    )
    view.rest_reviews_display.grid(column=0, row=0, sticky=(N, S, E, W))
    exit_button.grid(column=0, row=0, sticky=(N, E, S), pady=10)
    menu_open_button.grid(column=0, row=1, sticky=(N, E))

    view.rest_info_dispaly.tag_configure(
        "HEADER", justify="left", font=("Helvetica 15 bold")
    )
    view.rest_info_dispaly.tag_configure(
        "INFORMATION", justify="left", font=("Helvetica  12")
    )
    view.rest_info_dispaly.tag_configure(
        "INFO_BOLD", justify="left", font=("Helvetica  12 bold")
    )

    view.rest_reviews_display.tag_configure(
        "HEADER", justify="left", font=("Helvetica 15 bold")
    )
    view.rest_reviews_display.tag_configure(
        "INFORMATION", justify="left", font=("Helvetica  12")
    )
    view.rest_reviews_display.tag_configure(
        "INFO_BOLD", justify="left", font=("Helvetica  12 bold")
    )
