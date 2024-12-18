from tkinter import *

from dialog_object import DialogObject
from file_writer import HomeMadeFileWriter
from renpy_converter.object_to_script_converter import ObjToScriptConverter


# https://www.askpython.com/python-modules/tkinter/tkinter-create-oval
# https://tkinterpython.top/drawing/

def generate_text(origin):
    # Init fileWriter
    file_writer = HomeMadeFileWriter()
    file_writer.set_mode("w")
    file_writer.set_file("script_test.rpy")

    # Gather information on tree
    tree_information = origin.get_tree_information()

    # Init ObjConverter
    obj_converter = ObjToScriptConverter()
    obj_converter.set_dialogs_list(tree_information["dialogs"])
    obj_converter.set_characters_list(tree_information["characters"])

    # Convert and write to file
    file_writer.write(obj_converter.convert())


class TestWindow:

    photo = None    # needed otherwise Python fucking garbage collector snatch the picture

    def __init__(self,window):

        canvas = Canvas(window,width=500, height=500,highlightthickness=0)

        # SCROLLBARS ZONE
        hbar = Scrollbar(window, orient=HORIZONTAL)
        hbar.pack(side=BOTTOM, fill=X)
        hbar.config(command=canvas.xview)
        vbar = Scrollbar(window, orient=VERTICAL)
        vbar.pack(side=RIGHT, fill=Y)
        vbar.config(command=canvas.yview)
        canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)

        first_obj = DialogObject()
        first_obj.set_character("Willy Wonka")
        first_obj.set_img("Willy Beans")
        first_obj.set_text("I hate cappuccino")

        shitray = ["Woma","Wikon","Wiky","Wololo","Wubur"]

        obj_p = first_obj

        for i in range(10):
            obj = DialogObject()
            obj.set_character(shitray[i%5])
            obj.set_img("Beans"+shitray[i%5])
            obj.set_text("I hate "+shitray[i%5])
            obj.set_parent(obj_p)
            obj_p = obj

        first_obj.build_tree(canvas)

        nb_obj = 10
        canvas.configure(scrollregion=(0, 0, 120*nb_obj, 2000))
        canvas.pack(fill=BOTH, expand=True)

        button_send = Button(window, text="Generate as file", command=lambda : generate_text(first_obj))
        button_send.pack()

