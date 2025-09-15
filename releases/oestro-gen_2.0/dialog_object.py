import typing
from random import choices
from tkinter import *
from uuid import uuid4

from dialog_object_ui import build_ui_part, build_descendant
from model_object.background_object import BackgroundObject
from dialog_object_observer import DialogObjectObserver
from renpy_converter.choice import Choice
from renpy_converter.dialogmenu import DialogMenu
from renpy_converter.labelobject import LabelObject
from model_object.character_object import Character


class DialogObject:
    """
    A graphical object containing infos about a dialog scene or part of a dialog scene.
    Still WIP

    Attributes :
        Lots of shit still being developed, thus To Be Done
    """

    character : Character = None
    text : str = None
    img : str = None
    parent = None
    descendants = None
    tkinter_object = None
    canvas : Canvas = None
    choices : typing.List[str]= None
    menu_name = None
    model_controller = None
    background : BackgroundObject = None
    dialog_id_y : int = None
    observer : DialogObjectObserver = None
    character_current_expression : str = ""
    clicked_on : bool = False

    def __init__(self):
        self.character = Character("Bob")
        self.text = "placeholder text"
        self.img = "placeholder"
        # Forcing type
        self.descendants : typing.List[DialogObject] = []
        self.choices = []
        self.parent : DialogObject = None
        # for testing purposes
        self.background : BackgroundObject = BackgroundObject("forest")

    def click_on(self):
        self.clicked_on = not self.clicked_on
        self.update_observer("click_on_dialog_object",id(self))
        self.update_observer("display_dialog", [self.character.get_name(), self.text, self.background.get_name()])
        # if self.clicked_on:
        #     self.update_observer("display_dialog", [self.character.get_name(),self.text,self.background.get_name()])
    def is_clicked_on(self):
        return self.clicked_on
    def update_observer(self,data_type,data):
        self.observer.update_doo(self,data_type,data)
    def set_observer(self, obs):
        self.observer = obs
    def set_canvas(self,canvas : Canvas):
        self.canvas = canvas
    def set_dialog_y(self, dialog_id : int):
        self.dialog_id_y = dialog_id
    def set_background(self,background):
        self.background = background
    def set_character(self,character : Character):
        self.character = character
        self.update_tkinter_character_label()
    def set_character_current_expression(self,expression):
        self.character_current_expression = expression
    def set_text(self,text):
        self.text = text.replace("\"", "")
    def update_tkinter_character_label(self):
        self.update_observer("update_dialog_object_character_name",[id(self),self.character.get_name()])
        #self.canvas.itemconfig(self.tkinter_label, text=self.character.get_name())
    def set_img(self,img):
        self.img = img
    def set_parent(self,parent):
        self.parent = parent
        parent.add_descendant(self)
        self.set_model_controller_from_parent() # add the model controller from the parent
        if self.parent:
            if self.parent.get_observer():
                self.set_observer(self.parent.get_observer())

    def set_model_controller(self, controller):
        self.model_controller = controller

    # add the model controller from the parent
    def set_model_controller_from_parent(self):
        if self.parent is not None:
            self.set_model_controller(self.parent.get_model_controller())
    def get_model_controller(self):
        return self.model_controller

    def add_descendant(self,descendant):
        # print("added : " + descendant.get_character()+" to : "+self.character)
        self.descendants.append(descendant)
        if len(self.descendants)>1:
            for i in range(len(self.descendants)-len(self.choices)):
                self.add_choice("Eat cheese")

    def set_tkinter_object(self,obj):
        self.tkinter_object = obj
    def set_menu_name(self,name):
        self.menu_name = name
    def get_menu_name(self):
        return self.menu_name
    def add_choice(self, choice):
        self.choices.append(choice)
    def set_choice(self,choices):
        self.choices = choices
    def get_choices(self):
        return self.choices
    def get_character_object(self):
        return self.character
    def get_character(self):
        return self.character.get_name()
    def get_character_current_expression(self):
        return self.character_current_expression
    def get_text(self):
        return self.text
    def get_img(self):
        return self.img
    def get_parent(self):
        return self.parent
    def get_descendants(self):
        return self.descendants
    def get_tkinter_object(self):
        return self.tkinter_object
    def get_background(self):
        return self.background
    def get_dialog_id_y(self):
        return self.dialog_id_y
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
        while obj is not None:
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

    def get_observer(self):
        return self.observer

    def add_descendant_gui(self,canvas : Canvas):
        """
        Create a new descendant on the called object before adding it to the canvas
        """

        obj = DialogObject()
        # obj.set_character(str(randint(0,10)))
        obj.set_img("Beans")
        obj.set_text("Hi, I'm "+obj.get_character())
        obj.set_parent(self)
        origin = obj.get_origin_object()
        self.build_tree(canvas)
        #build_ui_part(obj, obj.get_index_x_level(),obj.get_index_y_level(), canvas)
    def destroy_descendant(self,index):
        self.descendants.pop(index)
        if len(self.choices)>1:
            self.choices.pop(index)
        else:
            self.choices.clear()

    def __del__(self):
        print(self.character.get_name() + " has died :(\n")

    def destroy_downhill(self,canvas : Canvas):
        """
        Destroy all descendants, and their descendants etc... from the called object
        without destroying the object itself.
        """
        for descendant in self.descendants:
            # print("Currently killing : "  + descendant.get_character())
            descendant.destroy_downhill(canvas)
            # Destroy canvas shapes
            descendant.destroy_all_gui_objects(canvas)
            del descendant
        # Cleanup just in case
        self.descendants = []
        self.update_observer("delete_choices",id(self))


    def destroy_self(self,canvas : Canvas):
        """
        Destroy the object from which the function is called and all its descendants
        """
        self.destroy_downhill(canvas)
        self.destroy_tree(canvas)
        if self.get_parent():
            index = self.get_parent().get_descendants().index(self)
            self.parent.destroy_descendant(index) # kill itself by garbage collector
        self.update_observer("kill_dialog_object", id(self))
        self.build_tree(canvas) # rebuild once everything is cleared


    def destroy_all_gui_objects(self, canvas : Canvas):
        """
        Destroy all GUI objects from the object, without deleting it
        """
        self.update_observer("kill_dialog_object", id(self))

    def destroy_tree(self,canvas : Canvas):
        """
        Destroy the whole GUI tree, without deleting the objects themselves
        """
        origin = self.get_origin_object()
        origin.destroy_tree_branch(canvas)

    def destroy_tree_branch(self, canvas : Canvas):
        """
        Destroy part of the GUI tree, without deleting the objects themselves
        """
        #origin = self.get_origin_object()
        self.destroy_all_gui_objects(canvas)
        for descendant in self.descendants:
            descendant.destroy_tree_branch(canvas)
            descendant.destroy_all_gui_objects(canvas)


    def build_tree(self,canvas : Canvas):
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
        # print("### Mainline : " + str(self.get_mainline_length()))
        canvas.configure(scrollregion=(0, 0, 120 * self.get_mainline_length(), 2000))

    def gather_object_information(self,parent_label):
        character_list = [self.get_character_object()]
        labels_list = []
        current_label = LabelObject()

        dialog_dict = {self.get_character_object(): (self.get_text(),self.character_current_expression)} # create a unique id for the dialog
        if not parent_label:
            current_label.set_name("start")
            current_label.set_background(self.background.get_name())
            current_label.set_dialogs_dict(dialog_dict)
            labels_list.append(current_label)
        else:
            current_label = parent_label
            current_label.add_to_dialogs_dict(dialog_dict)

        menu = None
        if self.get_choices() or len(self.get_choices()) != 0:  # there's a menu
            menu = DialogMenu()
            menu.set_tile(self.menu_name)
            # menu.set_choices()
            for choice in self.choices:
                new_choice = Choice()
                new_choice.set_title(choice)
                new_choice.set_text("You chose : "+choice)
                new_choice.set_jump("jump_to_"+str(uuid4().int>>64))
                menu.add_choice(new_choice)
            new_menu_label = LabelObject()
            new_menu_label.set_menu(menu)
            new_menu_label.set_type("menu")
            labels_list.append(new_menu_label)
        dialog_tree_info = {"characters": character_list, "labels": labels_list}
        i = 0 # for the choices
        for descendant in self.descendants:
            if not menu:
                temp_dict_info = descendant.gather_object_information(current_label) # get information from downstream
                # append the information to the characters list
                dialog_tree_info["characters"].extend(temp_dict_info["characters"])
                temp_list = dialog_tree_info["labels"]
                for label in temp_dict_info["labels"]:
                    temp_list.append(label)
                temp_list = list(dict.fromkeys(temp_list)) # remove duplicates
                dialog_tree_info["labels"] = temp_list
            else:
                new_choice_label = LabelObject()
                current_choice = menu.get_choice_list()[i]
                new_choice_label.set_name(current_choice.get_jump())
                new_choice_label.set_type("label")
                new_choice_label.set_background(descendant.get_background().get_name())
                dialog_tree_info["labels"].append(new_choice_label)
                temp_dict_info = descendant.gather_object_information(new_choice_label)  # get information from downstream
                dialog_tree_info["characters"].extend(temp_dict_info["characters"])
                temp_list = dialog_tree_info["labels"]
                for label in temp_dict_info["labels"]:
                    temp_list.append(label)
                temp_list = list(dict.fromkeys(temp_list)) # remove duplicates
                dialog_tree_info["labels"] = temp_list
                i += 1 # for the choices

        if len(self.descendants)==0:
            current_label.set_type("label-end")

        return dialog_tree_info

    def get_tree_information(self):
        return self.get_origin_object().gather_object_information(None)
