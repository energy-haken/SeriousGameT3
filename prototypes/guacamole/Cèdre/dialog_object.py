from tkinter import *

from numpy.matlib import empty
from sympy.core.random import random, randint


def build_descendant(descendants_list, index_x, canvas):
    """
    Static function building all descendants of a dialog object on the tkinter canvas
    """

    index_x+=1
    if descendants_list:
        for descendant in descendants_list:
            # Adding the GUI canvas part (Shapes)
            build_ui_part(descendant,index_x, canvas)
            build_descendant(descendant.get_descendants(), index_x, canvas)

def build_ui_part(descendant,index_x, canvas):
    """
    Static function building a single dialog object on the tkinter canvas, and storing each drawn elements in the object
    """

    offset_x = 80
    offset_y = 0
    index_y = 0 # not yet implemented
    tempt_obj = canvas.create_oval(10, 10, 80, 80, outline="black", fill="white", width=2)
    canvas.move(tempt_obj, 0 + offset_x * index_x, 0 + offset_y * index_y)
    descendant.set_tkinter_object(tempt_obj)
    coords_current_obj = canvas.coords(tempt_obj)
    line = canvas.create_line(coords_current_obj[2] + 20,  # end point x
                              int(coords_current_obj[3] / 2) + 5,  # end point y
                              coords_current_obj[2],  # start point x
                              int(coords_current_obj[3] / 2) + 5)  # start point y
    descendant.set_tkinter_line(line)
    label = canvas.create_text(40 + offset_x * index_x, 40 + offset_y * index_y,
                               text=descendant.get_character(),
                               fill="black", font=('Helvetica 15 bold'))
    descendant.set_tkinter_label(label)

    # Adding the buttons
    btn = Button(canvas, text='KILL', width=5,
                 height=1, bd='1', command=lambda: descendant.destroy_downhill(canvas))
    btn.place(x=40 + offset_x * index_x, y=50 + offset_y * index_y)
    descendant.set_tkinter_kill_button(btn)

    btn_add = Button(canvas, text='Add', width=5,
                     height=1, bd='1', command=lambda: descendant.add_descendant_gui(canvas))
    btn_add.place(x=0 + offset_x * index_x, y=50 + offset_y * index_y)
    descendant.set_tkinter_add_button(btn_add)

    # for index, descendant in enumerate(self.descendants): # can be useful for y position later
    #     self.build_descendant(descendant, index,canvas)


class DialogObject():
    """
    A graphical object containing infos about a dialog scene or part of a dialog scene.
    Still WIP

    Attributes :
        Lots of shit still being developed, thus To Be Done
    """

    character = None
    text = None
    img = None
    parent = None
    descendants = None
    tkinter_label = None
    tkinter_object = None
    tkinter_line = None
    tkinter_kill_button = None
    tkinter_add_button = None

    def __init__(self):
        self.character = "placeholder character"
        self.text = "placeholder text"
        self.img = "placeholder"
        self.descendants = []

    def set_character(self,character):
        self.character = character
    def set_text(self,text):
        self.text = text
        if self.tkinter_label is not None:
            self.tkinter_label.config(text=self.text)
    def set_img(self,img):
        self.img = img
    def set_parent(self,parent):
        self.parent = parent
        parent.add_descendant(self)
        print("My dad is : " + parent.get_character())
    def add_descendant(self,descendant):
        print("added : " + descendant.get_character()+" to : "+self.character)
        self.descendants.append(descendant)
    def set_tkinter_label(self,obj):
        self.tkinter_label = obj
    def set_tkinter_object(self,obj):
        self.tkinter_object = obj
    def set_tkinter_line(self,obj):
        self.tkinter_line = obj
    def set_tkinter_kill_button(self, obj):
        self.tkinter_kill_button = obj
    def set_tkinter_add_button(self,obj):
        self.tkinter_add_button = obj
    def get_character(self):
        return self.character
    def get_text(self):
        return self.text
    def get_img(self):
        return self.img
    def get_parent(self):
        return self.parent
    def get_descendants(self):
        print("Nb descendants for "+self.character+ " : "+str(len(self.descendants)))
        return self.descendants
    def get_tkinter_label(self):
        return self.tkinter_label
    def get_tkinter_object(self):
        return self.tkinter_object
    def get_tkinter_line(self):
        return self.tkinter_line
    def get_tkinter_kill_button(self):
        return self.tkinter_kill_button
    def get_tkinter_add_button(self):
        return self.tkinter_add_button

    def destroy_downhill(self,canvas):
        """
        Destroy all descendants, and their descendants etc... from the called object
        without destroying the object itself.
        """

        for descendant in self.descendants:
            print("Currently killing : "  + descendant.get_character())
            descendant.destroy_downhill(canvas)
            # Destroy canvas shapes
            canvas.delete(descendant.get_tkinter_object())
            canvas.delete(descendant.get_tkinter_label())
            canvas.delete(descendant.get_tkinter_line())
            # Destroy buttons
            descendant.get_tkinter_kill_button().destroy()
            descendant.get_tkinter_add_button().destroy()
            # Destroy Object
            del descendant
        # Cleanup just in case
        self.descendants = []

    def destroy(self,canvas):
        """
        Destroy the object from which the function is called and all its descendants
        """
        self.destroy_downhill(canvas)
        del self

    def add_descendant_gui(self,canvas):
        """
        Create a new descendant on the called object before adding it to the canvas
        """

        obj = DialogObject()
        obj.set_character(str(randint(0,10)))
        obj.set_img("Beans")
        obj.set_text("I hate " + "shitray[i % 5]")
        obj.set_parent(self)
        build_ui_part(obj,obj.get_index_level(),canvas)

    def get_index_level(self):
        """
        Get the index starting from the object from which the function is called to the first object.
        It is used only for drawing on the tkinter canvas.
        """

        obj = self.get_parent()
        index = 1
        while obj.get_parent() is not None:
            index+=1
            obj = obj.get_parent()
        return index

    def __del__(self):
        print(self.character + " has died :(\n")


    def build_tree(self,canvas):
        """
        build the dialog tree, starting from the object from which the function is called.
        """

        self.tkinter_object =  canvas.create_oval(10, 10, 80, 80, outline="black", fill="white", width=2)
        canvas.move(self.tkinter_object, 0, 0)
        index = 0
        build_descendant(self.get_descendants(),index, canvas)


