from tkinter import *
import tkinter as tk
import tkinter.messagebox
import tkinter.font as font


'''This help buttons would be located at the bottum right
corner through all the windows in the program.
There are 3 types of users in this program. The admin who
has all power to edit/update almost all information in the
database. The owner, who may upload and update their own
restaurant for users to search. And the guest user who may
search restaurants based on dietary restrictions, see
reviews, add reviews, search for hours, menus, and all
restaurant information.'''

# global space variable for help display message
filename = 'faq.txt'
space = '\n'

# creates the size, title, and background color of the app
root = tk.Tk()
root.geometry('200x200')
root.title('Project 6')
root.configure(bg='Moccasin')

# sets fonts
click_font = font.Font(family='Comic Sans MS', size=20)
exit_font = font.Font(family='Comic Sans MS', size=12)

guide_dict = {}


def read_line(filename: str) -> list:
# turn each line in the file to a list of string, and
# the content to list of lists
    global guide_dict
    try:
        with open(filename, 'r') as guide_info:
            lines = guide_info.readlines()
            
            header = None
            l = []

            for line in lines:
                if header is None:
                    header = line.strip()
                else:
                    l.append(line)
                    l.append(space)

                if line.isspace():
                    guide_dict[header] = l
                    l = []
                    header = None

            if header is not None:
                guide_dict[header] = l
                
    except FileNotFoundError as error:
        new_filename = input("File not found. please input a new file name")
        read_line(new_file)



def create_window():
    'Creates new window for user to select user type help'
    window = tk.Toplevel(root)
    window.geometry('300x200')
    window.title('User type Help')
    window.configure(bg='pink')

    # Creates button for admin help information
    admin_button = Button(window, text="Admin Help", command=admin_box)
    admin_button.place(relx=0.5, rely=0.2, anchor=CENTER)
    admin_button['font'] = click_font

    # creates button for owner help info
    owner_button = Button(window, text="Owner Help", command=owner_box)
    owner_button.place(relx=0.5, rely=0.5, anchor=CENTER)
    owner_button['font'] = click_font

    # creates button for guest help info
    guest_button = Button(window, text="Guest Help", command=guest_box)
    guest_button.place(relx=0.5, rely=0.8, anchor=CENTER)
    guest_button['font'] = click_font

    # creates an exit button
    exit_button = Button(window, text='Exit Program', command=exit_program)
    exit_button.place(relx=1.0, rely=1.0, anchor=SE)
    exit_button['font'] = exit_font


def admin_box():
    'Returns Q and A for admin in dict'
    user_list = guide_dict['ADMIN:']

    user_str = ''

    #converts dict into a str
    for each in user_list:
        user_str += each

    tkinter.messagebox.showinfo("Admin FAQS", user_str)


def owner_box():
    'Returns Q and A for owner in dict'
    user_list = guide_dict['OWNER:']

    user_str = ''

    #converts dict into a str
    for each in user_list:
        user_str += each

    tkinter.messagebox.showinfo("Owner FAQs", user_str)


def guest_box():
    'Returns Q and A for guest in dict'
    user_list = guide_dict['GUEST:']

    user_str = ''

    #converts dict into a str
    for each in user_list:
        user_str += each

    tkinter.messagebox.showinfo("Guest FAQs", user_str)


def exit_program():
    'exits the program'
    root.destroy()

# Creates a button that when clicked runs the message_box function
message_button = Button(root, text="Help", command=create_window)

# Centers the message button and establishes font
message_button.place(relx=0.5, rely=0.5, anchor=CENTER)
message_button['font'] = click_font

# Creates and implements an exit button on buttom corner
exit_button = Button(root, text='Exit Program', command=exit_program)
exit_button.place(relx=1.0, rely=1.0, anchor=SE)
exit_button['font'] = exit_font

if __name__ == '__main__':
    # continuous loop to run the program
    read_line(filename)
    root.mainloop()
