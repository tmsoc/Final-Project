from tkinter import *


def callback(sv):
    print(sv.get())
    print(len(sv.get()))


root = Tk()
sv = StringVar()
sv.trace_add("write", lambda name, index, mode, sv=sv: callback(sv))
e = Entry(root, textvariable=sv)
e.pack()
root.mainloop()
