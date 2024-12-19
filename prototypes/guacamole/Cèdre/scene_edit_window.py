import os
from tkinter import *
from tkinter.messagebox import showerror, showinfo

from PIL import ImageTk, Image

from model_observer import ModelObserver
from text_module_ui import TextModule


def error_handler(message):
    showerror("Error", message)

class SceneEditWindow(ModelObserver):

    image = None    # needed otherwise Python fucking garbage collector snatch the picture
    image_object = None
    user_input_character_global = None
    user_input_dialog_global = None
    descendant = None
    model_controller = None
    canvas = None
    base_path = "resources/renpy_project/Les Zamours/game/images/"
    image_is_ai = False
    window = None
    text_module_window = None
    menu_entry = None
    choice_entries = None

    def __init__(self,window,descendant):

        self.descendant = descendant
        self.window = window
        self.model_controller = descendant.get_model_controller()
        self.model_controller.add_observer(self)
        self.choice_entries = []

        # input_frame = LabelFrame(window,width=300,height=300,text="You are an idiot", padx=20, pady=20)
        # input_frame.pack(fill=BOTH, expand=True)
        input_frame = LabelFrame(self.window, text="Text Zone", padx=20, pady=20)
        input_frame.pack(fill="both", expand=0, side=TOP)

        character_str = StringVar()
        character_str.set(self.descendant.get_character())

        dialog_str = StringVar()
        dialog_str.set(self.descendant.get_text())

        character_input = Entry(input_frame, textvariable=character_str, width=30)
        character_input.pack()
        self.user_input_character_global = character_input


        dialog_input = Entry(input_frame, textvariable=dialog_str, width=30)
        dialog_input.pack()
        self.user_input_dialog_global = dialog_input

        # Menu
        if len(descendant.get_descendants())>1:
            menu_frame = LabelFrame(self.window, text="Menu", padx=20, pady=20)
            menu_frame.pack(fill="both", expand=0, side=TOP)
            # Menu Name
            menu_str_name = StringVar()
            menu_str_name.set("Menu name here")
            menu_name_input = Entry(menu_frame, textvariable=menu_str_name, width=30)
            menu_name_input.pack()
            self.menu_entry = menu_name_input
            choices_frame = LabelFrame(menu_frame, text="Choices", padx=20, pady=20)
            choices_frame.pack(fill="both", expand=0, side=TOP)

            for choice in descendant.get_choices():
                menu_str = StringVar()
                menu_str.set(choice)
                menu_input = Entry(choices_frame, textvariable=menu_str, width=30)
                menu_input.pack()
                self.choice_entries.append(menu_input)

        # Buttons
        button_send = Button(input_frame, text="Validate", command=lambda : self.update_fields())
        button_send.pack()

        button_ia = Button(input_frame, text="Generate with ai", command=lambda : self.launch_ia())
        button_ia.pack()

        button_save_image = Button(input_frame, text="Discard Generated Image", command=lambda : self.discard_image())
        button_save_image.pack()

        self.reload_image_path()

        self.canvas = Canvas(self.window, width=500, height=500, highlightthickness=0)
        self.image_object = self.canvas.create_image(10, 10, image=self.image, anchor=NW, tags="image")
        self.canvas.pack(fill=BOTH, expand=True)
        self.reload_image()

        # close the window properly
        self.window.protocol("WM_DELETE_WINDOW", lambda: self.quit_window())

    # close the window properly
    def quit_window(self):
        print("KILLING DAD")
        if self.text_module_window is not None: # close its child window properly
            self.text_module_window.quit_window()
        self.text_module_window = None
        self.model_controller.remove_observer(self)
        self.window.destroy()
    def clear_text_module_window(self):
        self.text_module_window = None

    def update_fields(self):
        self.descendant.set_character(str(self.user_input_character_global.get()))
        self.descendant.set_text(str(self.user_input_dialog_global.get()))
        if self.menu_entry: # if there's a menu
            self.descendant.set_menu_name(str(self.menu_entry.get()))
            choices_list = []
            for choice in self.choice_entries:
                choices_list.append(str(choice.get()))
            self.descendant.set_choice(choices_list)
        self.save_image()
        self.reload_image_path()
        self.reload_image()

    def launch_ia(self):
        if not self.text_module_window:
            self.text_module_window = TextModule(Toplevel(self.window), self.model_controller,self)
            if self.descendant.get_parent():
                character_parent = self.descendant.get_parent()
                self.text_module_window.set_context(character_parent.get_character()+":"+character_parent.get_text())

    def update_output(self,data):
        # self.descendant.set_text(data[0]['generated_text'])
        self.user_input_dialog_global.delete(0, END) #deletes the current value
        self.user_input_dialog_global.insert(0, data[0]['generated_text'])

    def reload_image_path(self):
        my_path = self.base_path+self.user_input_character_global.get()+".png"
        if os.path.isfile(my_path):
            self.image = Image.open(my_path)
        else:
            self.image = Image.open("resources/images/angry.png")
        self.image = self.image.resize((500, 500))
        self.image = ImageTk.PhotoImage(self.image)
    def reload_image(self):
        self.canvas.itemconfig(self.image_object, image=self.image)

    def update_image(self,img):
        if img[0]=="error":
            error_handler("Select a model first, then presse apply")
        else:
            self.image = ImageTk.PhotoImage(img[0])
            self.image_is_ai = True
    def save_image(self):
        if self.image_is_ai:
            file_name = self.user_input_character_global.get()
            if not self.image is None:
                img = ImageTk.getimage(self.image)
                img.save(self.base_path + file_name + ".png", "PNG")
                showinfo("Saved", "Image saved at : " + self.base_path)
                self.image_is_ai = False
            else:
                error_handler("No image to save")

    def discard_image(self):
        if self.image_is_ai:
            self.reload_image_path()
            self.reload_image()
            self.image_is_ai = False

    def update(self,subject,data_type,data) -> None:
        """
        Receive update from subject.
        """
        # Determine the type of update given
        match data_type:
            case "output":
                self.update_output(data)
            case "image":
                self.update_image(data)
                self.reload_image()
            case _: # We don't care about most updates, only about receiving the output data
                print("ERROR : DISCARDED SUBJECT DATA")
        pass
