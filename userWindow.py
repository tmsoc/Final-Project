from tkinter import *
from tkinter import ttk


class View:

    is_hello_world_shown = False

    def __init__(self, root, controller):
        self.root = root
        self.controller = controller

    def _build_window(self):
        self.root.title("MVC")
        self.root.geometry("300x150")
        self.root.resizable(0, 0)

    def _build_widgets(self):
        self.hw_label = ttk.Label(
            self.root, text="", font=("Times", 32, "bold"), anchor="center"
        )
        self.btn = ttk.Button(
            self.root, text="Press", command=self.controller.print_message
        )

    def _place_widgets(self):
        self.hw_label.grid(column=0, row=0, columnspan=3, sticky=(N, S, E, W))
        self.btn.grid(column=1, row=1)

    def initialize_window(self):
        self._build_window()
        self._build_widgets()
        self._place_widgets()

        self.root.columnconfigure(1, weight=20)
        self.root.rowconfigure(0, weight=5)
        self.root.rowconfigure(1, weight=5)

    def hello_world(self):
        if not self.is_hello_world_shown:
            self.hw_label["text"] = "Hello World!!"
            self.is_hello_world_shown = True
        else:
            self.hw_label["text"] = ""
            self.is_hello_world_shown = False
