from tkinter import *


def _login_place_widget(view):
    lbl_user_name = Label(
        view.window, text="Username:", font="None 11", bg="#0080c0",
    )
    view.entry_user_name = Entry(view.window, font="None 11", width=25,)
    lbl_password = Label(
        view.window, text="Password:", font="None 11", bg="#0080c0"
    )
    view.entry_password = Entry(
        view.window, font="None 11", show="*", width=25,
    )
    button_frame = Frame(view.window, bg="#0080c0")
    btn_login = Button(
        button_frame,
        text="Log in",
        font="none 11",
        command=view.controller.btn_login_press,
    )
    btn_cancel = Button(
        button_frame,
        text="Cancel",
        font="none 11",
        command=view.controller.back_to_welcome,
    )
    #         lbl_signup_prompt = Label(
    #             view.window,
    #             text="Haven't got an account? \n \
    # Enter your username, password and click Sign up",
    #             font="None 11",
    #             bg="#0080c0",
    #             height=2,
    #         )
    #         btn_signup = Button(
    #             view.window,
    #             text="Sign up",
    #             font="none 11",
    #             command=view.controller.save_new_user,
    #         )
    view.lbl_login_fail = Label(
        view.window, bg="#0080c0", font="None 11", fg="red",
    )

    button_frame.grid(row=2, column=0, columnspan=3, sticky=(E, W))
    lbl_user_name.grid(row=0, column=0, sticky="w", padx=5, pady=(20, 10))
    view.entry_user_name.grid(row=0, column=1, sticky="we", padx=(0, 50))
    lbl_password.grid(row=1, column=0, sticky="w", padx=5, pady=(10, 30))
    view.entry_password.grid(
        row=1, column=1, sticky="we", padx=(0, 50), pady=(10, 30)
    )
    # btn_login.grid(row=2, column=0, columnspan=2)
    btn_login.grid(row=0, column=0, padx=70)
    """
        lbl_signup_prompt.grid(
            row=3, column=0, columnspan=2, pady=10, sticky="w"
        )
        btn_signup.grid(row=4, column=0, columnspan=2, pady=5)
        """
    view.lbl_login_fail.grid(row=5, column=0, columnspan=2, pady=10)
    # view.lbl_login_fail.grid(row=8, column=0, columnspan=2)
    btn_cancel.grid(row=0, column=1, padx=10, sticky=E)
    # btn_cancel.grid(row=9, column=0, columnspan=2, pady=5)

