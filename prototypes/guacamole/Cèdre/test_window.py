from tkinter import *
from tkinter.messagebox import showerror

from PIL import ImageTk, Image

from Cèdre.dialog_object import DialogObject
from Cèdre.dialog_tree_object import DialogTreeObject
from Cèdre.file_writer import HomeMadeFileWriter
from Cèdre.resizable_canvas import ResizingCanvas


# https://www.askpython.com/python-modules/tkinter/tkinter-create-oval
# https://tkinterpython.top/drawing/

def generate_text(origin):
    file_writer = HomeMadeFileWriter()
    file_writer.set_mode("w")
    file_writer.set_file("script_test.rpy")
    file_writer.write(origin.convert_to_script())


class TestWindow:

    photo = None    # needed otherwise Python fucking garbage collector snatch the picture

    def __init__(self,window):

        # input_frame = LabelFrame(window,width=300,height=300,text="You are an idiot", padx=20, pady=20)
        # input_frame.pack(fill=BOTH, expand=True)


        # self.photo = Image.open("resources/images/angry.png")
        # self.photo = self.photo.resize((50,50))
        # self.photo = ImageTk.PhotoImage(self.photo)

        # canvas = Canvas(window)
        canvas = Canvas(window,width=500, height=500,highlightthickness=0)
        # canvas.config(width=1000, height=1000)

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

