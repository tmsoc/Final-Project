from tkinter import *


def _welcome_place_widget(view):
    top_frame = Frame(
        master=view.window,
        width=495,
        height=495,
        bg="#0080c0",
        relief="groove",
        borderwidth="2",
    )
    welcome_label = Label(
        top_frame,
        text="Where Should We Eat Tonight?",
        font=view.font1,
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
    view.user_type_var = StringVar(value="user")
    radiobtn_admin = Radiobutton(
        top_frame,
        text="Admin",
        font="none 12",
        bg="#0080c0",
        activebackground="#0080c0",
        height=2,
        width=5,
        variable=view.user_type_var,
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
        variable=view.user_type_var,
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
        variable=view.user_type_var,
        value="user",
    )
    btn_next = Button(
        top_frame,
        text="Next",
        font="none 12",
        bg="light gray",
        height=1,
        width=8,
        command=view.controller.welcome_screen_next_button_press,
    )
    welcome_label.place(x=80, y=50)
    welcome_option_label.place(x=65, y=150)
    top_frame.place(x=3, y=3)
    radiobtn_admin.place(x=150, y=180)
    radiobtn_owner.place(x=150, y=210)
    radiobtn_user.place(x=150, y=240)
    btn_next.place(x=210, y=320)
