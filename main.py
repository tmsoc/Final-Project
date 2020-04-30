from tkinter import *

from restDataAccess import Model
from controller import Controller
from view import View


def main():
    model = Model()
    root = Tk()
    controller = Controller(model, root)
    controller.begin()
    root.mainloop()
    model.close_connection()


if __name__ == "__main__":
    main()
