from tkinter import *

from sympy.core.random import random, randint


def build_descendant(descendants_list, index_x,index_y, canvas):
    """
    Static function building all descendants of a dialog object on the tkinter canvas
    """

    index_x+=1

    if descendants_list:
        for descendant in descendants_list:
            # Adding the GUI canvas part (Shapes)
            #index_y = descendants_list.index(descendant)
            index_y = descendant.get_index_y_level()
            build_ui_part(descendant,index_x,index_y, canvas)
            build_descendant(descendant.get_descendants(), index_x,index_y, canvas)

def build_ui_part(descendant,index_x,index_y, canvas):
    """
    Static function building a single dialog object on the tkinter canvas, and storing each drawn elements in the object
    """

    offset_x = 80
    offset_y = 100
    descendant_object = canvas.create_oval(10, 10, 80, 80, outline="black", fill="white", width=2)
    canvas.move(descendant_object, 0 + offset_x * index_x, 0 + offset_y * index_y)
    descendant.set_tkinter_object(descendant_object)
    parent_object = None
    coords_parent_obj = [0,0,0,0]
    parent_index_y = 0
    if descendant.get_parent():
        parent_object = descendant.get_parent().get_tkinter_object()
        coords_parent_obj = canvas.coords(parent_object)
        parent_index_y = descendant.get_y_level_parent_scope()

    line = canvas.create_line(coords_parent_obj[2]+10,  # end point x
                              int((coords_parent_obj[3]) -35 + offset_y * parent_index_y),  # end point y
                              coords_parent_obj[2],  # start point x
                              int((coords_parent_obj[3]) -35))  # start point y
    descendant.set_tkinter_line(line)
    label = canvas.create_text(40 + offset_x * index_x, 40 + offset_y * index_y,
                               text=descendant.get_character(),
                               fill="black", font=('Helvetica 15 bold'))
    descendant.set_tkinter_label(label)

    # Adding the buttons
    btn = Button(canvas, text='KILL', width=5,
                 height=1, bd='1', command=lambda: descendant.destroy_self(canvas))
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

    def get_index_x_level(self):
        """
        Get the x index starting from the object from which the function is called to the first object.
        It is used only for drawing on the tkinter canvas.
        """

        obj = self.get_parent()
        index = 1
        while obj.get_parent() is not None:
            index+=1
            obj = obj.get_parent()
        return index

    def get_index_y_level(self):
        """
        Get the y index starting from the object from which the function is called to the first object.
        It is used only for drawing on the tkinter canvas.
        """

        obj = self.get_parent()
        index = 0
        child = self

        while obj.get_parent() is not None:
            index+=obj.get_descendants().index(child)
            child = obj
            obj = obj.get_parent()
        print("y index of : " + self.get_character() + "is : " + str(index))
        return index

    def get_y_level_parent_scope(self):
        """
        Get the y index from the parent scope.
        It is used only for drawing on the tkinter canvas.
        """

        obj = self.get_parent()
        index = obj.get_descendants().index(self)
        return index

    def get_origin_object(self):
        obj = self
        if self.get_parent():
            obj = self.get_parent()
            while obj.get_parent() is not None:
                obj = obj.get_parent()
        return obj

    def get_mainline_length(self):
        """
        Get the length of the main timeline
        """
        index = 0
        origin = self.get_origin_object()
        index = origin.get_line_length(index)

        return index
    def get_line_length(self,index):
        """
        Get the length of one timeline
        """
        if self.get_descendants():
            index = self.get_descendants()[0].get_line_length(index)
            index += 1
        return index

    ########## POSTPONED FOR THE RELEASE OF HALF LIFE THREE
    # def check_x_y_placement_offset(self):
    #     y_offset = 0
    #     index_x = self.get_index_x_level()
    #     index_y = self.get_index_y_level()
    #
    #     obj = self.get_parent()
    #     while obj.get_parent() is not None: # go to the mainline
    #         obj = obj.get_parent()
    #
    #     total_y_offset = obj.explore(index_x,index_y)
    #     return y_offset
    #
    # def explore(self,index_x_limit,index_y_limit):
    #     """
    #     Explore each timeline according to the limits and return the y offset of the object
    #     STILL WIP AND NON-FUNCTIONAL
    #     """
    #
    #     index_y = 0
    #     obj = self
    #
    #     for i in range(index_x_limit): # shit code, going to do something that explore the lines next time
    #         obj_x = obj
    #         for y in range(index_y_limit):  # shit code, going to do something that explore the lines next time
    #             if obj_x.get_descendants() and len(obj_x.get_descendants())>=y:
    #                 obj_y = obj_x.get_descendants()[y]
    #         obj_x = obj.get_descendants()[i]
    #     return index_y

    def add_descendant_gui(self,canvas):
        """
        Create a new descendant on the called object before adding it to the canvas
        """

        obj = DialogObject()
        obj.set_character(str(randint(0,10)))
        obj.set_img("Beans")
        obj.set_text("I hate " + "shitray[i % 5]")
        obj.set_parent(self)
        origin = obj.get_origin_object()
        self.build_tree(canvas)
        #build_ui_part(obj, obj.get_index_x_level(),obj.get_index_y_level(), canvas)



    def __del__(self):
        print(self.character + " has died :(\n")


    def destroy_downhill(self,canvas):
        """
        Destroy all descendants, and their descendants etc... from the called object
        without destroying the object itself.
        """

        for descendant in self.descendants:
            print("Currently killing : "  + descendant.get_character())
            descendant.destroy_downhill(canvas)
            # Destroy canvas shapes
            descendant.destroy_all_gui_objects(canvas)
            # Destroy Object
            del descendant
        # Cleanup just in case
        self.descendants = []

    def destroy_self(self,canvas):
        """
        Destroy the object from which the function is called and all its descendants
        """
        self.destroy_downhill(canvas)
        self.destroy_tree(canvas)
        if self.get_parent():
            index = self.get_parent().get_descendants().index(self)
            self.get_parent().get_descendants().pop(index) # kill itself by garbage collector
        self.build_tree(canvas) # rebuild once everything is cleared


    def destroy_all_gui_objects(self, canvas):
        """
        Destroy all GUI objects from the object, without deleting it
        """
        canvas.delete(self.get_tkinter_object())
        canvas.delete(self.get_tkinter_label())
        canvas.delete(self.get_tkinter_line())
        # Destroy buttons
        if self.get_tkinter_kill_button():
            self.get_tkinter_kill_button().destroy()
        if self.get_tkinter_add_button():
            self.get_tkinter_add_button().destroy()

    def destroy_tree(self,canvas):
        """
        Destroy the whole GUI tree, without deleting the objects themselves
        """
        origin = self.get_origin_object()
        origin.destroy_tree_branch(canvas)

    def destroy_tree_branch(self, canvas):
        """
        Destroy part of the GUI tree, without deleting the objects themselves
        """
        #origin = self.get_origin_object()
        self.destroy_all_gui_objects(canvas)
        for descendant in self.descendants:
            descendant.destroy_tree_branch(canvas)
            descendant.destroy_all_gui_objects(canvas)


    def build_tree(self,canvas):
        """
        build the dialog tree, starting from the origin object.
        """
        origin = self.get_origin_object()
        self.destroy_tree(canvas)

        origin.tkinter_object =  canvas.create_oval(10, 10, 80, 80, outline="black", fill="white", width=2)
        canvas.move(origin.tkinter_object, 0, 0)
        index_x = 0
        index_y = 0


        build_ui_part(origin, index_x,index_y, canvas)
        build_descendant(origin.get_descendants(),index_x,index_y, canvas)
        print("### Mainline : " + str(self.get_mainline_length()))
        canvas.configure(scrollregion=(0, 0, 120 * self.get_mainline_length(), 2000))


