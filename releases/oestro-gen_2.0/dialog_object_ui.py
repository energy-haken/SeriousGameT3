from abc import ABC, abstractmethod
from tkinter import Toplevel, Canvas
from uuid import uuid4


from guiSceneEditWindow import SceneEditWindow
from dialog_object_observer import DialogObjectObserver


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

def build_ui_part(descendant,index_x,index_y, canvas : Canvas):
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
        descendant.set_dialog_y(parent_index_y)
    else: # origin of the tree
        descendant.set_dialog_y(0)

    descendant_object = canvas.create_oval(10, 10, 80, 80, outline="black", fill="white"
                                           , width=2,tags=("oval"+'|'+str(id(descendant))))
    canvas.move(descendant_object, 0 + offset_x * index_x, 0 + offset_y * index_y)
    descendant.set_tkinter_object(descendant_object)
    # Create the line connecting to the parent
    line = canvas.create_line(coords_parent_obj[2]+10,  # end point x
                              int((coords_parent_obj[3]) -35 + offset_y * parent_index_y),  # end point y
                              coords_parent_obj[2],  # start point x
                              int((coords_parent_obj[3]) -35),  # start point y
                              tags=("line"+'|'+str(id(descendant))
                              ))
    # Create the label for the character
    label = canvas.create_text(40 + offset_x * index_x, 40 + offset_y * index_y,
                               text=descendant.get_character(),
                               fill="black", font=('Helvetica 15 bold'),
                               tags=("label"+'|'+str(id(descendant))))
    # Create buttons (delete, open, add)
    btn_kill = canvas.create_rectangle(5, 0, 20, 15, outline="black", fill="red", width=2,
                               tags=("btn_kill"+'|'+str(id(descendant))))
    canvas.move(btn_kill, 10 + offset_x * index_x, 50 + offset_y * index_y)
    btn_window = canvas.create_rectangle(5, 0, 20, 15, outline="black", fill="grey", width=2,
                             tags=("btn_window"+'|'+str(id(descendant))))
    canvas.move(btn_window, 30 + offset_x * index_x, 50 + offset_y * index_y)
    btn_add = canvas.create_rectangle(5, 0, 20, 15, outline="black", fill="green", width=2,
                              tags=("btn_add"+'|'+str(id(descendant))))
    canvas.move(btn_add, 50 + offset_x * index_x, 50 + offset_y * index_y)

    i = 0
    if not len(descendant.get_descendants())<=1:
        for child in descendant.get_descendants():
            btn_choice = canvas.create_rectangle(0, 0, 10, 10, outline="black", fill="orange", width=2,
                                                 tags=("choice"+'|'+str(id(descendant))))
            canvas.move(btn_choice, 70 + offset_x * index_x, 30 +10*i + offset_y * index_y)
            i+=1

    # super source :
    # https://stackoverflow.com/questions/2786877/how-to-bind-events-to-canvas-items

    # Events for the canvas

    def click_dialog_object(event):
        if descendant.get_model_controller():
            descendant.get_model_controller().broadcast_message(f"DialogObject clicked: {descendant.get_character()}", "info")
        if descendant.get_tkinter_object() and not descendant.is_clicked_on():
            canvas.itemconfig(canvas.find_withtag('oval'+'|'+str(id(descendant)))[0],outline="yellow")
            descendant.click_on()
        else:
            descendant.click_on()

    canvas.tag_bind(descendant_object, '<ButtonPress-1>', click_dialog_object)

    def click_remove(event):
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

    descendant.update_observer("add_dialog_object",id(descendant))


def destroy_dialog_object(canvas,dialog_id):
    canvas.delete(canvas.find_withtag('oval'+'|'+str(dialog_id))[0])
    canvas.delete(canvas.find_withtag('line'+'|'+str(dialog_id))[0])
    canvas.delete(canvas.find_withtag('btn_kill'+'|'+str(dialog_id))[0])
    canvas.delete(canvas.find_withtag('btn_window'+'|'+str(dialog_id))[0])
    canvas.delete(canvas.find_withtag('btn_add'+'|'+str(dialog_id))[0])
    canvas.delete(canvas.find_withtag('label'+'|'+str(dialog_id))[0])
    destroy_choices(canvas,dialog_id)
def destroy_choices(canvas,dialog_id):
    for choice in canvas.find_withtag('choice'+'|'+str(dialog_id)): # delete the choices buttons
        canvas.delete(choice)
def update_dialog_object_name(canvas,dialog_id,new_name):
    canvas.itemconfig(canvas.find_withtag('label' + '|' + str(dialog_id))[0], text=new_name)
def on_click_change_dialog_object(canvas,dialog_id,color):
    canvas.itemconfig(canvas.find_withtag('oval' + '|' + str(dialog_id))[0],outline=color)

class DialogObjectUi(DialogObjectObserver, ABC):

    label = None
    body = None
    line = None
    btn_kill = None
    btn_add = None
    btn_window = None
    choices = None
    canvas : Canvas = None

    def __init__(self):
        self.choices = []

    def destroy_ui_choices(self):
        for choice in self.choices:
            self.canvas.delete(choice)
        self.choices.clear()
    def update_tkinter_character_label(self,character):
        self.canvas.itemconfig(self.label, text=character)
    def set_tkinter_label(self,obj):
        self.label = obj
    def set_tkinter_object(self,obj):
        self.body = obj
    def set_tkinter_line(self,obj):
        self.line = obj
    def set_tkinter_kill_button(self, obj):
        self.btn_kill = obj
    def set_tkinter_add_button(self,obj):
        self.btn_add = obj
    def set_tkinter_window_button(self,obj):
        self.btn_window = obj
    def set_canvas(self,canvas : Canvas):
        self.canvas = canvas
    def add_tkinter_choice(self,choice):
        self.choices.append(choice)
    def destroy_all_gui_objects(self):
        """
        Destroy all GUI objects from the object, without deleting it
        """
        if self.canvas:
            if self.body:
                self.canvas.delete(self.body())
            if self.label:
                self.canvas.delete(self.label())
            if self.line:
                self.canvas.delete(self.line())
            if self.btn_kill:
                self.canvas.delete(self.btn_kill())
            if self.btn_add:
                self.canvas.delete(self.btn_add())
            if self.btn_window:
                self.canvas.delete(self.btn_window())
            self.destroy_ui_choices()


    @abstractmethod
    def update_doo(self,subject,data_type,data) -> None:
        """
        Receive update from subject.
        """
        pass




