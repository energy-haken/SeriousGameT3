from functools import partial
from idlelib.editor import keynames
from tkinter import *
from tkinter.messagebox import *
import menu_ui
import text_module_ui
from text_module_ui import TextModule


# https://python.doctor/page-tkinter-interface-graphique-python-tutoriel

def placeHolder():
    showinfo("placeHolder", "Test")



window = Tk()
window.iconbitmap("resources/images/icon.ico")
window.title("Œstro-gen")

menu_ui.init(window)

#textFrame = LabelFrame(window, text="Text Frame", padx=20, pady=20)
#textFrame.grid(row=1,  column=2,  padx=10,  pady=5)

text_module = TextModule(window)
window.mainloop()