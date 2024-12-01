from tkinter import *
from tkinter.messagebox import *

from Cèdre.dialog_object import DialogObject
from Cèdre.test_window import TestWindow
import torch


def placeHolder():
    showinfo("placeHolder", "Test")
def error_handler(message):
    showerror("Error", message)

window = Tk()
window.iconbitmap("resources/images/icon.ico")
window.title("Œstro-gen")
window.geometry("700x350")

test = TestWindow(window)

window.mainloop()

# first_obj = DialogObject()
# first_obj.set_character("Willy Wonka")
# first_obj.set_img("Willy Beans")
# first_obj.set_text("I hate cappuccino")
#
# shitray = ["Woma","Wikon","Wiky","Wololo","Wubur"]
#
# obj_p = first_obj
#
# for i in range(10):
#     obj = DialogObject()
#     obj.set_character(shitray[i%5])
#     obj.set_img("Beans"+shitray[i%5])
#     obj.set_text("I hate "+shitray[i%5])
#     obj.set_parent(obj_p)
#     obj_p = obj
#
# while(obj_p is not None):
#     print(obj_p.get_character() + "\n" + obj_p.get_img() + "\n" + obj_p.get_text() + "\n")
#     obj_p = obj_p.get_parent()

