from tkinter import *
from tkinter.messagebox import *

def placeHolder():
    showinfo("placeHolder", "Test")

def init(window):
    menubar = Menu(window)

    menu1 = Menu(menubar, tearoff=0)
    menu1.add_command(label="New Project", command=placeHolder)
    menu1.add_command(label="Open Project", command=placeHolder)
    menu1.add_separator()
    menu1.add_command(label="Quit", command=window.quit)
    menubar.add_cascade(label="Files", menu=menu1)

    menu2 = Menu(menubar, tearoff=0)
    menu2.add_command(label="Cut", command=placeHolder)
    menu2.add_command(label="Copy", command=placeHolder)
    menu2.add_command(label="Paste", command=placeHolder)
    menubar.add_cascade(label="Edit", menu=menu2)

    menu3 = Menu(menubar, tearoff=0)
    menu3.add_command(label="About", command=placeHolder)
    menubar.add_cascade(label="Help", menu=menu3)

    menu4 = Menu(menubar, tearoff=0)
    menu4.add_command(label="Stable Diffusion", command=placeHolder)
    menu4.add_command(label="XXstrem-Omega-ZimZoom", command=placeHolder)
    menubar.add_cascade(label="Model", menu=menu4)

    window.config(menu=menubar)

