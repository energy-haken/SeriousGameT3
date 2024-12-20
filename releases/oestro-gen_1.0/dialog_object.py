from tkinter import *
from uuid import uuid4

from renpy_converter.choice import Choice
from renpy_converter.dialogmenu import DialogMenu
from renpy_converter.labelobject import LabelObject
from guiSceneEditWindow import SceneEditWindow


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
    descendant.set_canvas(canvas)

    offset_x = 80
    offset_y = 100
    parent_object = None
    coords_parent_obj = [0,0,0,0]
    parent_index_y = 0
    if descendant.get_parent():
        parent_object = descendant.get_parent().get_tkinter_object()
        coords_parent_obj = canvas.coords(parent_object)
        parent_index_y = descendant.get_y_level_parent_scope()

    descendant_object = canvas.create_oval(10, 10, 80, 80, outline="black", fill="white", width=2)
    canvas.move(descendant_object, 0 + offset_x * index_x, 0 + offset_y * index_y)
    descendant.set_tkinter_object(descendant_object)

    line = canvas.create_line(coords_parent_obj[2]+10,  # end point x
                              int((coords_parent_obj[3]) -35 + offset_y * parent_index_y),  # end point y
                              coords_parent_obj[2],  # start point x
                              int((coords_parent_obj[3]) -35))  # start point y
    descendant.set_tkinter_line(line)
    label = canvas.create_text(40 + offset_x * index_x, 40 + offset_y * index_y,
                               text=descendant.get_character(),
                               fill="black", font=('Helvetica 15 bold'))
    descendant.set_tkinter_label(label)

    btn_kill = canvas.create_rectangle(5, 0, 20, 15, outline="black", fill="red", width=2)
    canvas.move(btn_kill, 10 + offset_x * index_x, 50 + offset_y * index_y)
    btn_window = canvas.create_rectangle(5, 0, 20, 15, outline="black", fill="grey", width=2)
    canvas.move(btn_window, 30 + offset_x * index_x, 50 + offset_y * index_y)
    btn_add = canvas.create_rectangle(5, 0, 20, 15, outline="black", fill="green", width=2)
    canvas.move(btn_add, 50 + offset_x * index_x, 50 + offset_y * index_y)

    i = 0
    if not len(descendant.get_descendants())<=1:
        for child in descendant.get_descendants():
            btn_choice = canvas.create_rectangle(0, 0, 10, 10, outline="black", fill="orange", width=2)
            canvas.move(btn_choice, 70 + offset_x * index_x, 30 +10*i + offset_y * index_y)
            descendant.add_tkinter_choice(btn_choice)
            descendant.add_choice("test_banana"+str(uuid4().int>>64))
            i+=1

    descendant.set_tkinter_kill_button(btn_kill)
    descendant.set_tkinter_add_button(btn_add)
    descendant.set_tkinter_window_button(btn_window)
    # super source :
    # https://stackoverflow.com/questions/2786877/how-to-bind-events-to-canvas-items

    # Events for the canvas

    def click_remove(event):
        # print('Got object click', event.x, event.y)
        # print(event.widget.find_closest(event.x, event.y))
        descendant.destroy_self(canvas)
    def click_add(event):
        # print('Got object click', event.x, event.y)
        # print(event.widget.find_closest(event.x, event.y))
        descendant.add_descendant_gui(canvas)
    def click_window(event):
        # print('Got object click', event.x, event.y)
        # print(event.widget.find_closest(event.x, event.y))
        if descendant.get_model_controller().get_current_project():
            try:
                scene_window = SceneEditWindow(Toplevel(),descendant)
                #descendant.get_model_controller().get_current_window()
            except ValueError:
                print("ERROR : Multiple scene_edit_window opened at the same time !")
        else:
            descendant.get_model_controller().broadcast_message("No project selected","error")

    canvas.tag_bind(btn_kill, '<ButtonPress-1>', click_remove)
    canvas.tag_bind(btn_add, '<ButtonPress-1>', click_add)
    canvas.tag_bind(btn_window, '<ButtonPress-1>', click_window)

    # for index, descendant in enumerate(self.descendants): # can be useful for y position later
    #     self.build_descendant(descendant, index,canvas)


class DialogObject:
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
    tkinter_window_button = None
    canvas = None
    tkinter_choices = None
    choices = None
    menu_name = None
    model_controller = None

    def __init__(self):
        self.character = "Bob"
        self.text = "placeholder text"
        self.img = "placeholder"
        self.descendants = []
        self.tkinter_choices = []
        self.choices = []
    def set_canvas(self,canvas):
        self.canvas = canvas

    def set_character(self,character):
        self.character = character
        if self.tkinter_label:
            self.update_tkinter_character_label()
    def set_text(self,text):
        self.text = text
    def update_tkinter_character_label(self):
        self.canvas.itemconfig(self.tkinter_label, text=self.character)
    def set_img(self,img):
        self.img = img
    def set_parent(self,parent):
        self.parent = parent
        parent.add_descendant(self)
        self.set_model_controller_from_parent() # add the model controller from the parent
        # print("My dad is : " + parent.get_character())

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
    def set_tkinter_window_button(self,obj):
        self.tkinter_window_button = obj
    def set_menu_name(self,name):
        self.menu_name = name
    def get_menu_name(self):
        return self.menu_name
    def add_tkinter_choice(self,choice):
        self.tkinter_choices.append(choice)
    def add_choice(self, choice):
        self.choices.append(choice)
    def set_choice(self,choices):
        self.choices = choices
    def get_choices(self):
        return self.choices
    def get_character(self):
        return self.character
    def get_text(self):
        return self.text
    def get_img(self):
        return self.img
    def get_parent(self):
        return self.parent
    def get_descendants(self):
        # print("Nb descendants for "+self.character+ " : "+str(len(self.descendants)))
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
    def get_tkinter_window_button(self):
        return self.tkinter_window_button

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

    def add_descendant_gui(self,canvas):
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



    def __del__(self):
        print(self.character + " has died :(\n")


    def destroy_downhill(self,canvas):
        """
        Destroy all descendants, and their descendants etc... from the called object
        without destroying the object itself.
        """

        for descendant in self.descendants:
            # print("Currently killing : "  + descendant.get_character())
            descendant.destroy_downhill(canvas)
            # Destroy canvas shapes
            descendant.destroy_all_gui_objects(canvas)
            # Destroy Object
            del descendant
        # Cleanup just in case
        self.descendants = []
    def destroy_ui_choices(self,canvas):
        for choice in self.tkinter_choices:
            canvas.delete(choice)
        self.choices.clear()

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
        if canvas:
            if self.get_tkinter_object():
                canvas.delete(self.get_tkinter_object())
            if self.get_tkinter_label():
                canvas.delete(self.get_tkinter_label())
            if self.get_tkinter_line():
                canvas.delete(self.get_tkinter_line())
            if self.get_tkinter_kill_button():
                canvas.delete(self.get_tkinter_kill_button())
            if self.get_tkinter_add_button():
                canvas.delete(self.get_tkinter_add_button())
            if self.get_tkinter_window_button():
                canvas.delete(self.get_tkinter_window_button())
            self.destroy_ui_choices(canvas)

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
        # print("### Mainline : " + str(self.get_mainline_length()))
        canvas.configure(scrollregion=(0, 0, 120 * self.get_mainline_length(), 2000))

    def gather_object_information(self,parent_label):
        character_list = [self.get_character()]
        # dialog_dict = {((self.get_character())
        #                +"*"+ str(uuid4())).lower(): self.get_text()} # create a unique id for the dialog
        labels_list = []
        current_label = LabelObject()
        dialog_dict = {((self.get_character())
                       +"*"+ str(uuid4())).lower(): self.get_text()} # create a unique id for the dialog
        if not parent_label:
            current_label.set_name("start")
            current_label.set_background("room")
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
                new_choice_label.set_background("room")
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
