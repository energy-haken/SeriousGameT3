import os
from tkinter import *
from tkinter.messagebox import showerror, showinfo

from PIL import ImageTk, Image
from PIL.ImagePath import Path

from model_handler import ModelHandler
from observer import Observer
from text_module_ui import TextModule


def error_handler(message):
    showerror("Error", message)

class SceneEditWindow(Observer):

    image = None    # needed otherwise Python fucking garbage collector snatch the picture
    image_object = None
    user_input_character_global = None
    user_input_dialog_global = None
    descendant = None
    model_handler = None
    canvas = None
    base_path = "resources/renpy_project/Les Zamours/game/images/"

    def __init__(self,window,descendant):

        self.descendant = descendant
        # input_frame = LabelFrame(window,width=300,height=300,text="You are an idiot", padx=20, pady=20)
        # input_frame.pack(fill=BOTH, expand=True)
        input_frame = LabelFrame(window, text="Text Zone", padx=20, pady=20)
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

        button_send = Button(input_frame, text="Validate", command=lambda : self.update_fields())
        button_send.pack()

        button_ia = Button(input_frame, text="Generate with ai", command=lambda : self.launch_ia())
        button_ia.pack()

        button_save_image = Button(input_frame, text="Save Generated Image", command=lambda : self.save_image())
        button_save_image.pack()

        my_path = self.base_path+self.user_input_character_global.get()+".png"
        if os.path.isfile(my_path):
            self.image = Image.open(my_path)
        else:
            self.image = Image.open("resources/images/angry.png")
        self.image = self.image.resize((500, 500))
        self.image = ImageTk.PhotoImage(self.image)

        self.canvas = Canvas(window, width=500, height=500, highlightthickness=0)
        self.image_object = self.canvas.create_image(10, 10, image=self.image, anchor=NW, tags="image")
        self.canvas.pack(fill=BOTH, expand=True)
        window.mainloop()

    def update_fields(self):
        self.descendant.set_character(str(self.user_input_character_global.get()))
        self.descendant.set_text(str(self.user_input_dialog_global.get()))
        # self.save_image()

    def launch_ia(self):
        if not self.model_handler:
            self.model_handler = ModelHandler()
            self.model_handler.add_observer(self)
        TextModule(Toplevel(),self.model_handler)

    def update_output(self,data):
        self.descendant.set_text(data[0]['generated_text'])
        # self.user_input_dialog_global.config(textvariable=data[0]['generated_text'])
        self.user_input_dialog_global.delete(0, END) #deletes the current value
        self.user_input_dialog_global.insert(0, data[0]['generated_text'])


    def update_image(self,img):
        if img[0]=="error":
            error_handler("Select a model first, then presse apply")
        else:
            self.image = ImageTk.PhotoImage(img[0])
            self.canvas.itemconfig(self.image_object, image = self.image)
            # self.image_label.config(image=tkimg)
            # self.image_label.image = tkimg
            # self.image_cache = tkimg
    def save_image(self):
        file_name = self.user_input_character_global.get()
        if not self.image is None:
            img = ImageTk.getimage(self.image)  # get the actual image
            img.save(self.base_path + file_name + ".png", "PNG")
            showinfo("Saved", "Image saved at : " + self.base_path)
        else:
            error_handler("No image to save")
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
            case _: # We don't care about most updates, only about receiving the output data
                print("ERROR : DISCARDED SUBJECT DATA")
        pass
