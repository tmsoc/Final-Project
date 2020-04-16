from tkinter import *
from tkinter import ttk

from userWindow import View


class Conteroller:
    def __init__(self, view):
        self.view = View(view, self)

    def initialize_window(self):
        self.view.initialize_window()

    def print_message(self):
        self.view.hello_world()


def main():
    root = Tk()
    c = Conteroller(root)
    c.initialize_window()
    root.mainloop()


if __name__ == "__main__":
    main()
