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
space = '\n'

# creates the size, title, and background color of the app
root = tk.Tk()
root.geometry('200x200')
root.title('Project 6')
root.configure(bg='Moccasin')

# sets fonts
click_font = font.Font(family='Comic Sans MS', size=20)
exit_font = font.Font(family='Comic Sans MS', size=12)


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


def admin_box():
    'Creates a message box with FAQ to be displayed'

    question1 = 'What if I do not have an account? \n'
    answer1 = ('You will need a pass key to create an account to ' +
               'ensure that you are authorized to use the system. \n')

    question2 = 'How do I see all information on a given resturaunt?\n'
    answer2 = ('You are able to filter your search through the ' +
               'restuarant name, owner ID, or menu. Once you have ' +
               'filtered your search, select the restaurant to see ' +
               'all the information in the database on it.\n')

    question3 = 'How do I edit/update information?\n'
    answer3 = ('Simply select the restaurant you would like to edit ' +
               'and at the bottum of the page, there will be an ' +
               'update button that will allow you to update/edit/delete' +
               ' the information on the screen.\n')

    question4 = 'How can I edit reviews?\n'
    answer4 = ('Unfortunately for customer authenticity, you are unable ' +
               'to edit the reviews, however you may delete them. Just ' +
               'go to the edit tab and there will be an option underneath ' +
               'the reviews that allows you to delete selected reviews.\n')
    # puts all Q and A into one
    question_answer = (question1 + space + answer1 + space +
                       question2 + space + answer2 + space +
                       question3 + space + answer3 + space +
                       question4 + space + answer4)

    tkinter.messagebox.showinfo("Admin FAQS", question_answer)


def owner_box():
    'Creates owner FAQ window to be displayed'

    question1 = 'How can I include my resturarant? \n'
    answer1 = ('Select the create an account button after selecting ' +
               'owner view. Input all the data asked for including ' +
               'name, email, and resturant info. Please also upload a ' +
               'pdf file for your resturant menu. You will then be ' +
               'allowed to create a username and ID and be given a ' +
               'Restaurant ID. PLease store this information. \n')

    question2 = "How do I edit my restaurant information?\n"
    answer2 = ('Once logged in, at the bottum of the page, there ' +
               'will be an option to edit the information on the screen.')

    question3 = 'Can I see reviews?\n'
    answer3 = 'Yes you may see your reviews at the bottum of the page\n'

    question4 = 'Can I edit my reviews?\n'
    answer4 = ('Unforuntatley that is the only information that you as an ' +
               'owner do not have access to edit. This is to ensure that ' +
               'guests are able to view your restuarant in the full ' +
               ' with custoimer authenticity.\n')

    # puts all Q and A into one
    question_answer = (question1 + space + answer1 + space +
                       question2 + space + answer2 + space +
                       question3 + space + answer3 + space +
                       question4 + space + answer4)

    tkinter.messagebox.showinfo("Owner FAQs", question_answer)


def guest_box():
    'Creates a FAQS box to be displayed when ran'
    question1 = 'What is this for? \n'
    answer1 = ('This app helps those with dietary restrictions ' +
               'locate a resturant that fit their needs. \n')

    question2 = 'How do I search? \n'
    answer2 = ('At the top right corner of the page, there is filter' +
               'option that allows you to filter resturants based on ' +
               'selected dietary options. \n')

    question3 = 'How do I get more information on a resturant? \n'
    answer3 = ('Simply select the restaurant you would like to view ' +
               'and another screen will show you all the collected ' +
               'information on the restaurant.\n')

    question4 = 'What information do I have access to? \n'
    answer4 = ("You are able to view a restaurant's name, address, " +
               "address, hours, reviews, dietary restrictions, and " +
               "menu. \n")

    question5 = 'Can I leave a review of the resturant? \n'
    answer5 = ('Yes. Select the restaurant you would like to review' +
               ' and at the bottum of the page, there will be a' +
               'option to write a review')

    # puts all Q and A into one
    question_answer = (question1 + space + answer1 + space +
                       question2 + space + answer2 + space +
                       question3 + space + answer3 + space +
                       question4 + space + answer4 + space +
                       question5 + space + answer5)

    tkinter.messagebox.showinfo("Guest FAQs", question_answer)


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
    root.mainloop()
