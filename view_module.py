from tkinter import *

def main_window():
    global window, var, font1
    window = Tk()
    window.title("Where Should We Eat Tonight?")
    window.configure(background = "light gray")
    window.geometry("500x500")
    window.resizable(0, 0)

    top_frame = Frame(master=window, width=495, height=495, bg="#0080c0",
                      relief = "groove", borderwidth = "2")
    top_frame.place(x = 3, y = 3)

    font1 = "-family {Segoe UI} -size 14 -weight bold -slant "  \
                "italic"
    Label(top_frame, text = "Where Should We Eat Tonight?", font = font1,
          bg = "#0080ff", relief="raised", height = 2,
          width = 30, disabledforeground="#a3a3a3").place(x = 80, y = 50)

    Label(top_frame, text = "Tell us who you are by selecting one of these options",
          font = "none 12", bg = "#0080c0", height = 2,
          width = 40).place(x = 65, y = 150)

    var = IntVar()
    radiobtn_admin = Radiobutton(top_frame, text = "Admin", font = "none 12",
                                 bg = "#0080c0", height = 2,width = 5,
                                 variable = var, value = 1)
    radiobtn_admin.place(x = 150, y = 180)

    radiobtn_owner = Radiobutton(top_frame, text = "Restaurant Owner", font = "none 12",
                                 bg = "#0080c0", height = 2,width = 14,
                                 variable = var, value = 2)
    radiobtn_owner.place(x = 150, y = 210)

    radiobtn_guest = Radiobutton(top_frame, text = "Customer", font = "none 12",
                                 bg = "#0080c0", height = 2,width = 8,
                                 variable = var, value = 3)
    radiobtn_guest.place(x = 150, y = 240)

    next_btn = Button(top_frame, text = "Next", font = "none 12",
                                 bg = "light gray", height = 1,width = 8,
                      command = next_window)
    next_btn.place(x = 210, y = 320)

    window.mainloop()

def destroy_window(view):
    view.destroy()
    
def next_window():
    global window, var
    destroy_window(window)
    option = var.get()
    if option == 1:
        admin_login()
        
    elif option == 2:
        owner_login()

    elif option == 3:
        customer_view()

def view1_label(label, var):
    if var == 1:
        label.config(text = "Restaurant owner ID - Restaurant name:")
    elif var == 2:
        label.config(text = "Restaurant Info:")
    elif var == 3:
        label.config(text = "Restaurant - Menu:")
    
def destroy_view1():
    global view1
    view1.destroy()
    
def admin_view():
    global login1, font1, view1

    destroy_window(login1)

    view1 = Tk()
    view1.title("Admin View")
    view1.configure(background = "#0080c0")
    view1.geometry("600x500")
    view1.resizable(0, 0)

    Label(bg = "#0080c0", text = "Administrative Function",
          font = font1).grid(row = 0,columnspan = 7)

    Label(bg = "#0080c0", height = 2, width = 5).grid(row = 1,column = 0)

    view1_var = IntVar()
    
    radiobtn_id = Radiobutton(view1, text = "Owner ID", font = "none 12",
                                 bg = "#0080c0", height = 2,width = 8,
                                 variable = view1_var, value = 1)
    radiobtn_id.grid(row = 2, column  = 1)

    radiobtn_info = Radiobutton(view1, text = "Restaurant Info", font = "none 12",
                                 bg = "#0080c0", height = 2,width = 15,
                                 variable = view1_var, value = 2)
    radiobtn_info.grid(row = 2, column  = 2)

    radiobtn_menu = Radiobutton(view1, text = "Menus", font = "none 12",
                                 bg = "#0080c0", height = 2,width = 5,
                                 variable = view1_var, value = 3)
    radiobtn_menu.grid(row = 2, column  = 3)

    Label(bg = "#0080c0", height = 2, width = 5).grid(row = 2,column = 4)
    
    btn_list = Button(view1, text = "Show List", font = "none 12",
                                 bg = "light grey", height = 1, width = 10,
                      command = lambda : view1_label(lbl_prompt, view1_var))
    btn_list.grid(row = 2, column = 5, sticky = "e")

    lbl_prompt = Label(bg = "#0080c0", font = "none 12")
    lbl_prompt.grid(row = 3, column = 1, columnspan = 2)

    list_box = Listbox(view1, font = "none 12", height = 12,
                       selectmode = "SINGLE")
    list_box.grid(row = 4, column = 1, columnspan = 4, sticky = "we")

    btn_info = Button(view1, text = "More info", font = "none 12",
                                 bg = "light grey", height = 1, width = 10)
    btn_info.grid(row = 4, column = 5, sticky = "e")

    Label(bg = "#0080c0").grid(row = 5,columnspan = 7)
    
    btn_update = Button(view1, text = "Update", font = "none 12",
                                 bg = "light grey", height = 1, width = 10)
    btn_update.grid(row = 6, column = 2)

    btn_exit = Button(view1, text = "Exit", font = "none 12",
                                 bg = "light grey", height = 1, width = 10,
                      command = destroy_view1)
    btn_exit.grid(row = 6, column = 5)
    
    view1.mainloop()
    
def admin_login():
    global login1
    login1 = Tk()
    login1.title("Administrator")
    login1.configure(background = "#0080c0")
    login1.geometry("330x200")
    login1.resizable(0, 0)

    Label(bg = "#0080c0").grid(row = 0)
    user_name = StringVar()
    lbl_user_name = Label(login1, text = "Username:", font = "None 11",
          bg = "#0080c0")
    lbl_user_name.grid(row = 1, column = 0, sticky = "w")
    
    entry_user_name = Entry(login1, font = "None 11", textvariable = user_name,
                            width = 22)
    entry_user_name.grid(row = 1, column = 1, sticky = "we")

    Label(bg = "#0080c0").grid(row = 2)

    password = StringVar()
    lbl_password = Label(login1, text = "Password:", font = "None 11",
          bg = "#0080c0")
    lbl_password.grid(row = 3, column = 0)

    entry_password = Entry(login1, font = "None 11", textvariable = password,
                           show='*', width = 22)
    entry_password.grid(row = 3,column = 1)

    Label(bg = "#0080c0").grid(row = 4)
    Button(login1, text = "Log in", font = "none 11", command = admin_view).grid(row = 5, column = 1, sticky = "NSEW")
    
    login1.mainloop()

def owner_login():
    view2 = Tk()
    view2.title("Bussiness Owner")
    view2.configure(background = "light gray")
    view2.geometry("300x200")
    view2.resizable(0, 0)

    view2.mainloop()
    
def customer_view():
    view3 = Tk()
    view3.title("Customer")
    view3.configure(background = "light gray")
    view3.geometry("500x500")
    view3.resizable(0, 0)

    view3.mainloop()
                    

if __name__ == "__main__":
    main_window()
