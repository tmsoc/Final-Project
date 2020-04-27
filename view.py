from tkinter import *

class View:

    font1 = "-family {Segoe UI} -size 14 -weight bold -slant " "italic"

    def __init__(self, root, controller):
        self.window = root
        self.controller = controller
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
        self.var = IntVar()
        radiobtn_admin = Radiobutton(
            top_frame,
            text="Admin",
            font="none 12",
            bg="#0080c0",
            height=2,
            width=5,
            variable=self.var,
            value=1,
        )
        radiobtn_owner = Radiobutton(
            top_frame,
            text="Restaurant Owner",
            font="none 12",
            bg="#0080c0",
            height=2,
            width=14,
            variable=self.var,
            value=2,
        )
        radiobtn_guest = Radiobutton(
            top_frame,
            text="Customer",
            font="none 12",
            bg="#0080c0",
            height=2,
            width=8,
            variable=self.var,
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

    def _admin_login_place_widget(self):
        lbl_user_name = Label(
            self.window, text="Username:", font="None 11", bg="#0080c0",
        )
        self.entry_admin_user_name = Entry(
            self.window,
            font="None 11",
            width=22,
        )
        lbl_password = Label(
            self.window, text="Password:", font="None 11", bg="#0080c0"
        )
        self.entry_password = Entry(
            self.window,
            font="None 11",
            show="*",
            width=22,
        )
        login_button = Button(
            self.window,
            text="Log in",
            font="none 11",
            command=self.controller.validate_admin_login,
        )
        self.lbl_admin_login_fail = Label(
            self.window,
            bg="#0080c0",
            font="None 11",
            fg="red",
        )

        Label(self.window, bg="#0080c0").grid(row=0)
        lbl_user_name.grid(row=1, column=0, sticky="w")
        self.entry_admin_user_name.grid(row=1, column=1, sticky="we")
        Label(self.window, bg="#0080c0").grid(row=2)
        lbl_password.grid(row=3, column=0, sticky="w")
        self.entry_password.grid(row=3, column=1)
        Label(self.window, bg="#0080c0").grid(row=4)
        login_button.grid(row=5, column=1, sticky="NSEW")
        self.lbl_admin_login_fail.grid(
            row=6, column=0, columnspan=3, sticky="e"
        )

    def _owner_login_place_widget(self):
        lbl_user_name = Label(
            self.window, text="Username:", font="None 11", bg="#0080c0",
        )
        self.entry_owner_user_name = Entry(
            self.window,
            font="None 11",
            width=22,
        )
        lbl_password = Label(
            self.window, text="Password:", font="None 11", bg="#0080c0"
        )
        self.entry_owner_password = Entry(
            self.window,
            font="None 11",
            show="*",
            width=22,
        )
        login_button = Button(
            self.window,
            text="Log in",
            font="none 11",
            command=self.controller.validate_owner_login,
        )
        signup_button = Button(
            self.window,
            text="Sign up",
            font="none 11",
            command=self.controller.save_new_user,
        )
        self.lbl_owner_login_fail = Label(
            self.window,
            bg="#0080c0",
            font="None 11",
            fg="red",
        )

        Label(self.window, bg="#0080c0").grid(row=0)
        lbl_user_name.grid(row=1, column=0, sticky="w")
        self.entry_owner_user_name.grid(row=1, column=1, sticky="we")
        Label(self.window, bg="#0080c0").grid(row=2)
        lbl_password.grid(row=3, column=0, sticky="w")
        self.entry_owner_password.grid(row=3, column=1)
        Label(self.window, bg="#0080c0").grid(row=4)
        login_button.grid(row=5, column=1, sticky="NSEW")
        Label(self.window, bg="#0080c0").grid(row=6)
        signup_button.grid(row=7, column=1, sticky="NSEW")
        self.lbl_owner_login_fail.grid(
            row=8, column=0, columnspan=3, sticky="e"
        )

    def _user_login_place_widget(self):
        lbl_user_name = Label(
            self.window, text="Username:", font="None 11", bg="#0080c0",
        )
        self.entry_user_user_name = Entry(
            self.window,
            font="None 11",
            width=22,
        )
        lbl_password = Label(
            self.window, text="Password:", font="None 11", bg="#0080c0"
        )
        self.entry_user_password = Entry(
            self.window,
            font="None 11",
            show="*",
            width=22,
        )
        login_button = Button(
            self.window,
            text="Log in",
            font="none 11",
            command=self.controller.validate_user_login,
        )
        signup_button = Button(
            self.window,
            text="Sign up",
            font="none 11",
            command=self.controller.save_new_user,
        )
        self.lbl_user_login_fail = Label(
            self.window,
            bg="#0080c0",
            font="None 11",
            fg="red",
        )

        Label(self.window, bg="#0080c0").grid(row=0)
        lbl_user_name.grid(row=1, column=0, sticky="w")
        self.entry_user_user_name.grid(row=1, column=1, sticky="we")
        Label(self.window, bg="#0080c0").grid(row=2)
        lbl_password.grid(row=3, column=0, sticky="w")
        self.entry_user_password.grid(row=3, column=1)
        Label(self.window, bg="#0080c0").grid(row=4)
        login_button.grid(row=5, column=1, sticky="NSEW")
        Label(self.window, bg="#0080c0").grid(row=6)
        signup_button.grid(row=7, column=1, sticky="NSEW")
        self.lbl_user_login_fail.grid(
            row=8, column=0, columnspan=3, sticky="e"
        )

    def _admin_place_widget(self):
        self.var = IntVar()
        radiobtn_id = Radiobutton(
            self.window,
            text="Owner ID",
            font="none 12",
            bg="#0080c0",
            height=2,
            width=8,
            variable=self.var,
            value=1,
        )
        radiobtn_info = Radiobutton(
            self.window,
            text="Restaurant Info",
            font="none 12",
            bg="#0080c0",
            height=2,
            width=15,
            variable=self.var,
            value=2,
        )
        radiobtn_menu = Radiobutton(
            self.window,
            text="Menus",
            font="none 12",
            bg="#0080c0",
            height=2,
            width=5,
            variable=self.var,
            value=3,
        )
        btn_list = Button(
            self.window,
            text="Show List",
            font="none 12",
            bg="light grey",
            height=1,
            width=10,
            #command = a function in controller to return a list corresponding
            #to the value of var
        )
        lbl_prompt = Label(bg="#0080c0", font="none 12", text="List: ")
        self.view1_list_box = Listbox(
            self.window, font="none 12", height=12, selectmode="SINGLE"
        )
        btn_info = Button(
            self.window,
            text="More info",
            font="none 12",
            bg="light grey",
            height=1,
            width=10,
            command = self.controller.admin_view_more_info_btn
        )
        btn_update = Button(
            self.window,
            text="Update",
            font="none 12",
            bg="light grey",
            height=1,
            width=10,
        )
        btn_exit = Button(
            self.window,
            text="Exit",
            font="none 12",
            bg="light grey",
            height=1,
            width=10,
            command=self.controller.back_to_welcome
        )
        # ---DELETE ME---
        self.view1_list_box.insert(1, "Press exit to loop")
        # ---DELETE ME---
        
        Label(
            bg="#0080c0", text="Administrative Function", font=self.font1
        ).grid(row=0, columnspan=7)
        Label(bg="#0080c0", height=2, width=5).grid(row=1, column=0)
        radiobtn_id.grid(row=2, column=1)
        radiobtn_info.grid(row=2, column=2)
        radiobtn_menu.grid(row=2, column=3)
        btn_list.grid(row=2, column=5, sticky="e")
        Label(bg="#0080c0", height=2, width=5).grid(row=2, column=4)
        lbl_prompt.grid(row=3, column=1, columnspan=3, sticky="w")
        self.view1_list_box.grid(row=4, column=1, columnspan=4, sticky="we")
        btn_info.grid(row=4, column=5, sticky="e")
        Label(bg="#0080c0").grid(row=5, columnspan=7)
        btn_update.grid(row=6, column=2)
        btn_exit.grid(row=6, column=5)

    def _rest_info_place_widget(self):
        self.rest_info_list = self.controller.restaurant_info()
            
        lbl_prompt_rest_ID = Label(
            text = "Restaurant ID:",
            font = "None 11",
            bg = "#0080c0",
            height = 2
        )        
        lbl_rest_ID = Label(
            text = self.rest_info_list[0],
            font = "None 11",
            bg = "#0080c0",
            width = 50
        )     
        lbl_rest_name = Label(
            text = "Restaurant name:",
            font = "None 11",
            bg = "#0080c0",
            height = 2
        )      
        entry_rest_name = Entry(
            font = "None 11",
            bg = "white",
            width = 50
        )
        lbl_rest_address = Label(
            text = "Address:",
            font = "None 11",
            bg = "#0080c0",
            height = 2
        )
        entry_rest_address = Entry(
            font = "None 11",
            bg = "white",
            width = 50
        )
        lbl_rest_address = Label(
            text = "Address:",
            font = "None 11",
            bg = "#0080c0",
            height = 2
        )
        entry_rest_address = Entry(
            font = "None 11",
            bg = "white",
            width = 50
        )
        lbl_rest_city = Label(
            text = "City:",
            font = "None 11",
            bg = "#0080c0",
            height = 2
        )
        entry_rest_city = Entry(
            font = "None 11",
            bg = "white",
            width = 50
        )        
        lbl_rest_state = Label(
            text = "State:",
            font = "None 11",
            bg = "#0080c0",
            height = 2
        )        
        entry_rest_state = Entry(
            font = "None 11",
            bg = "white",
            width = 50
        )        
        lbl_rest_zip = Label(
            text = "Zip code:",
            font = "None 11",
            bg = "#0080c0",
            height = 2
        )
        entry_rest_zip = Entry(
            font = "None 11",
            bg = "white",
            width = 50
        )        
        lbl_rest_vege = Label(
            text = "Vegetarian:",
            font = "None 11",
            bg = "#0080c0",
            height = 2
        )
        entry_rest_vege = Entry(
            font = "None 11",
            bg = "white",
            width = 50
        )        
        lbl_rest_vegan = Label(
            text = "Vegan:",
            font = "None 11",
            bg = "#0080c0",
            height = 2
        )        
        entry_rest_vegan = Entry(
            font = "None 11",
            bg = "white",
            width = 50
        )        
        lbl_rest_gluten = Label(
            text = "Gluten:",
            font = "None 11",
            bg = "#0080c0",
            height = 2
        )        
        entry_rest_gluten = Entry(
            font = "None 11",
            bg = "white",
            width = 50
        )        
        lbl_rest_menu = Label(
            text = "Menu:",
            font = "None 11",
            bg = "#0080c0",
            height = 2
        )        
        entry_rest_menu = Entry(
            font = "None 11",
            bg = "white",
            width = 50
        )        
        lbl_rest_hours = Label(
            text = "Hours:",
            font = "None 11",
            bg = "#0080c0",
            height = 2
        )        
        entry_rest_hours = Entry(
            font = "None 11",
            bg = "white",
            width = 50
        )        
        lbl_rest_description = Label(
            text = "Description:",
            font = "None 11",
            bg = "#0080c0",
            height = 2
        )        
        entry_rest_description = Entry(
            font = "None 11",
            bg = "white",
            width = 50
        )        
        btn_save = Button(
            text = "Save",
            font = "None 11",
            bg = "light gray",
            #command = call a function in controller to write these entries
            #to data
        )
        btn_close = Button(
            text = "Close",
            font = "None 11",
            bg = "light gray",
            command = self.controller.back_to_admin_view
        )
        entry_rest_name.insert(0, str(self.rest_info_list[1]))
        entry_rest_address.insert(0, str(self.rest_info_list[2]))
        entry_rest_city.insert(0, str(self.rest_info_list[3]))
        entry_rest_state.insert(0, str(self.rest_info_list[4]))
        entry_rest_zip.insert(0, str(self.rest_info_list[5]))
        entry_rest_vege.insert(0, str(self.rest_info_list[6]))
        entry_rest_vegan.insert(0, str(self.rest_info_list[7]))
        entry_rest_gluten.insert(0, str(self.rest_info_list[8]))
        entry_rest_menu.insert(0, str(self.rest_info_list[9]))
        entry_rest_hours.insert(0, str(self.rest_info_list[10]))
        entry_rest_description.insert(0, str(self.rest_info_list[11]))
        
        lbl_prompt_rest_ID.grid(row = 0, column = 0, sticky = "w")
        lbl_rest_ID.grid(row = 0, column = 1, sticky = "w")
        lbl_rest_name.grid(row = 1, column = 0, sticky = "w")
        entry_rest_name.grid(row = 1, column = 1, sticky = "w")
        lbl_rest_address.grid(row = 2, column = 0, sticky = "w")
        entry_rest_address.grid(row = 2, column = 1, sticky = "w")
        lbl_rest_address.grid(row = 2, column = 0, sticky = "w")
        entry_rest_address.grid(row = 2, column = 1, sticky = "w")
        lbl_rest_city.grid(row = 3, column = 0, sticky = "w")
        entry_rest_city.grid(row = 3, column = 1, sticky = "w")
        lbl_rest_state.grid(row = 4, column = 0, sticky = "w")
        entry_rest_state.grid(row = 4, column = 1, sticky = "w")
        lbl_rest_zip.grid(row = 5, column = 0, sticky = "w")
        entry_rest_zip.grid(row = 5, column = 1, sticky = "w")
        lbl_rest_vege.grid(row = 6, column = 0, sticky = "w")
        entry_rest_vege.grid(row = 6, column = 1, sticky = "w")
        lbl_rest_vegan.grid(row = 7, column = 0, sticky = "w")
        entry_rest_vegan.grid(row = 7, column = 1, sticky = "w")
        lbl_rest_gluten.grid(row = 8, column = 0, sticky = "w")
        entry_rest_gluten.grid(row = 8, column = 1, sticky = "w")
        lbl_rest_menu.grid(row = 9, column = 0, sticky = "w")
        entry_rest_menu.grid(row = 9, column = 1, sticky = "w")
        lbl_rest_hours.grid(row = 10, column = 0, sticky = "w")
        entry_rest_hours.grid(row = 10, column = 1, sticky = "w")
        lbl_rest_description.grid(row = 11, column = 0, sticky = "w")
        entry_rest_description.grid(row = 11, column = 1, sticky = "w")
        Label(bg = "#0080c0").grid(row = 12, column = 0, columnspan = 2)
        btn_save.grid(row = 13, column = 0, columnspan = 2)
        Label(bg = "#0080c0").grid(row = 14, column = 0, columnspan = 2)
        btn_close.grid(row = 15, column = 0, columnspan = 2)

    def init_welcome_window(self):
        self.window.title("Where Should We Eat Tonight?")
        self.window.configure(background="light gray")
        self.window.geometry("500x500")
        self.window.resizable(0, 0)
        self._welcome_place_widget()

    def admin_login_window(self):
        self.window.title("Administrator")
        self.window.configure(background="#0080c0")
        self.window.geometry("330x200")
        self.window.resizable(0, 0)
        self._admin_login_place_widget()

    def owner_login_window(self):
        self.window.title("Bussiness Owner")
        self.window.configure(background="#0080c0")
        self.window.geometry("330x250")
        self.window.resizable(0, 0)
        self._owner_login_place_widget()

    def user_login_window(self):
        self.window.title("Customer")
        self.window.configure(background="#0080c0")
        self.window.geometry("330x250")
        self.window.resizable(0, 0)
        self._user_login_place_widget()

    def admin_window(self):
        self.window.title("Admin View")
        self.window.configure(background="#0080c0")
        self.window.geometry("600x500")
        self.window.resizable(0, 0)
        self._admin_place_widget()

    def restaurant_info_window(self):
        self.window.title("Restaurant Information")
        self.window.configure(background="#0080c0")
        self.window.geometry("580x600")
        self.window.resizable(0, 0)
        self._rest_info_place_widget()

#---------These lines below are used for examining my code------------
class Controller:
    def __init__(self, root):
        self.view = View(root, self)

    def welcome_screen_next_button(self):
        choice = self.view.var.get()
        print(f"From Welcome Screen - var = {choice}")
        self.view.clear_frame()
        if choice == 1:
            self.view.admin_login_window()
        elif choice == 2:
            self.view.owner_login_window()
        elif choice == 3:
            self.view.user_login_window()

    def validate_admin_login(self):
        name = self.view.entry_admin_user_name.get()
        password = self.view.entry_password.get()
        print(f"<<< {name} - {password} >>>")
        if name != "python" and password != "python":
            self.view.lbl_admin_login_fail[
                "text"
            ] = 'username and password is "python"'
        else:
            self.view.clear_frame()
            self.view.admin_window()
        
    def validate_owner_login(self):
        name = self.view.entry_owner_user_name.get()
        password = self.view.entry_owner_password.get()
        print(f"<<< {name} - {password} >>>")
        if name != "python" and password != "python":
            self.view.lbl_owner_login_fail[
                "text"
            ] = 'username and password is "python" \n \
                New customer? Click on Sign up'
        else:
            self.view.clear_frame()
            self.view.owner_window()

    def validate_user_login(self):
        name = self.view.entry_user_user_name.get()
        password = self.view.entry_user_password.get()
        print(f"<<< {name} - {password} >>>")
        if name != "python" and password != "python":
            self.view.lbl_user_login_fail[
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
        name = self.view.entry_user_user_name.get()
        password = self.view.entry_user_password.get()
        #write name and password into user table

    def admin_view_more_info_btn(self):
        self.view.clear_frame()
        self.view.restaurant_info_window()

    def restaurant_info(self) -> list:
        a_list = list()
        for each in range(12):
            a_list.append(each)
        return a_list

    def back_to_admin_view(self):
        self.view.clear_frame()
        self.view.admin_window()

if __name__ == "__main__":
    root = Tk()
    controller = Controller(root)
    root.mainloop()
    print("Program Ended")
#-----------Those lines above are used for examining my code------------
