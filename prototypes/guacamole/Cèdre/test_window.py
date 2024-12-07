from tkinter import *

from dialog_object import DialogObject
from file_writer import HomeMadeFileWriter
from model_handler import ModelHandler
from model_handler_controller import ModelController
from renpy_converter.object_to_script_converter import ObjToScriptConverter


# https://www.askpython.com/python-modules/tkinter/tkinter-create-oval
# https://tkinterpython.top/drawing/




def generate_text(origin):
    base_path = "resources/renpy_project/Les Zamours/game/"
    # Init fileWriter
    file_writer = HomeMadeFileWriter()
    file_writer.set_mode("w")
    file_writer.set_file(base_path+"script.rpy")

    # Gather information on tree
    tree_information = origin.get_tree_information()

    # Init ObjConverter



    obj_converter = ObjToScriptConverter()
    obj_converter.set_dialogs_dict(tree_information["dialogs"])
    obj_converter.set_characters_list(tree_information["characters"])

    # Convert and write to file
    file_writer.write(obj_converter.convert())


class TestWindow:

    photo = None    # needed otherwise Python fucking garbage collector snatch the picture
    model_controller = None
    canvas = None
    window = None
    def __init__(self,window):

        self.window = window
        self.canvas = Canvas(self.window,width=500, height=500,highlightthickness=0)
        self.model_controller = ModelController(ModelHandler())


        # SCROLLBARS ZONE
        hbar = Scrollbar(self.window, orient=HORIZONTAL)
        hbar.pack(side=BOTTOM, fill=X)
        hbar.config(command=self.canvas.xview)
        vbar = Scrollbar(self.window, orient=VERTICAL)
        vbar.pack(side=RIGHT, fill=Y)
        vbar.config(command=self.canvas.yview)
        self.canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)



        first_obj = DialogObject()
        first_obj.set_character("Willy Wonka")
        first_obj.set_img("Willy Beans")
        first_obj.set_text("I hate cappuccino")
        first_obj.set_model_controller(self.model_controller)


        # shitray = ["Woma","Wikon","Wiky","Wololo","Wubur"]

        # obj_p = first_obj
        #
        # for i in range(10):
        #     obj = DialogObject()
        #     obj.set_character(shitray[i%5])
        #     obj.set_img("Beans"+shitray[i%5])
        #     obj.set_text("I hate "+shitray[i%5])
        #     obj.set_parent(obj_p)
        #     obj_p = obj

        first_obj.build_tree(self.canvas)

        self.model_controller.set_current_window(window)

        nb_obj = 10
        self.canvas.configure(scrollregion=(0, 0, 120*nb_obj, 2000))
        self.canvas.pack(fill=BOTH, expand=True)

        button_send = Button(self.window, text="Generate as file", command=lambda : generate_text(first_obj))
        button_send.pack()
        button_gen_ai = Button(self.window, text="Generate the tree with ai", command=lambda : self.generate_tree_with_ai())
        button_gen_ai.pack()
        # close the window properly
        self.window.protocol("WM_DELETE_WINDOW", lambda: self.quit_window())

    # close the window properly
    def quit_window(self):
        quit()
        # self.model_controller.remove_observer(self)
        # self.window.destroy()


    def generate_tree_with_ai(self):
        self.canvas.delete("all") # clean up the canvas before generating anything with ai
        x = 0