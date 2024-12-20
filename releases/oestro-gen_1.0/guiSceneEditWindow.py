import os
from tkinter import *
from tkinter.messagebox import showerror, showinfo

from PIL import ImageTk, Image

from model_observer import ModelObserver
from idlelib.tooltip import Hovertip


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
    is_linked_to_model_handler = False
    menu_entry = None
    choice_entries = None

    def __init__(self,window,descendant):

        window.configure(bg="#0D0B0B")

        self.descendant = descendant
        self.window = window
        self.model_controller = descendant.get_model_controller()
        self.choice_entries = []
        self.model_controller.add_observer(self)
        self.model_controller.ask_can_generate()
        if self.model_controller.get_current_project():
            self.base_path = "resources/renpy_project/"+self.model_controller.get_current_project()+"/game/images/"
        else:
            self.quit_window()
        #input_frame = LabelFrame(self.window, text="Text Zone", padx=20, pady=20 , background="#0D0B0B")
        #input_frame.pack(fill="both", expand=0, side=TOP)

        frameNameDia = Frame(self.window, background="#1D1B1B" , pady=20, padx=80)
        frameNameDia.pack( expand=0, side=TOP)


        
        character_str = StringVar()
        character_str.set(self.descendant.get_character())

        dialog_str = StringVar()
        dialog_str.set(self.descendant.get_text())

        labelCharName = Label(frameNameDia, text="Character Name", background="#1D1B1B", fg="white" , font=("Khmer" , 15))
        labelCharName.pack()
        character_input = Entry(frameNameDia, textvariable=character_str, width=30)
        character_input.pack()
        self.user_input_character_global = character_input

        labelDialog = Label(frameNameDia, text="Dialog", background="#1D1B1B", fg="white" , font=("Khmer" , 15))
        labelDialog.pack()
        dialog_input = Entry(frameNameDia, textvariable=dialog_str, width=30)
        dialog_input.pack()
        self.user_input_dialog_global = dialog_input

        # Menu
        if len(descendant.get_choices())>1:
            #menu_frame = LabelFrame(self.window, text="Menu", padx=20, pady=20)
            #menu_frame.pack(fill="both", expand=0, side=TOP)

            frameVide = Frame(self.window, background="#0D0B0B" , height=50)
            frameVide.pack( fill="none" , expand=0, side=TOP)

            frameMenu = Frame(self.window, background="#1D1B1B" , pady=20, padx=80)
            frameMenu.pack(expand=0, side=TOP)
            # Menu Name
            menu_str_name = StringVar()
            menu_str_name.set("Menu name here")

            labelMenuName = Label(frameMenu, text="Menu Name", background="#1D1B1B", fg="white" , font=("Khmer" , 15))
            labelMenuName.pack()
            menu_name_input = Entry(frameMenu, textvariable=menu_str_name, width=30)
            menu_name_input.pack()
            self.menu_entry = menu_name_input
            #choices_frame = LabelFrame(frameMenu, text="Choices", padx=20, pady=20)
            #choices_frame.pack(fill="both", expand=0, side=TOP)

            frameChoices = Frame(frameMenu, background="#383535" , pady=20, padx=60)
            frameChoices.pack( expand=0, side=TOP)

            labelChoices = Label(frameChoices, text="Choices", background="#383535", fg="white" , font=("Khmer" , 15))
            labelChoices.pack()

            for choice in descendant.get_choices():
                menu_str = StringVar()
                menu_str.set(choice)
                menu_input = Entry(frameChoices, textvariable=menu_str, width=30)
                menu_input.pack()
                self.choice_entries.append(menu_input)

        button_send = Button(frameNameDia, background="#383535" , foreground="white" ,text="Validate", command=lambda : self.update_fields())
        button_send.pack()

        
        #button_ia = Button(frameNameDia, background="#383535" , foreground="white" , text="Generate with ai", command=lambda : self.launch_ia())
        #button_ia.pack()

        labelGenerateImage = Label(frameNameDia, text="To generate an image \n -Keep this window open and click on \"Generate\" \n -Wait", background="#1D1B1B", fg="white" , font=("Khmer" , 15))
        labelGenerateImage.pack()

        button_discard_image = Button(frameNameDia, background="#383535" , foreground="white" ,  text="Discard Generated Image", command=lambda : self.discard_image())
        button_discard_image.pack()
        tipDiscard = Hovertip(button_discard_image, "Discard the image just generated and reload the original one")

        self.reload_image_path()

        frameImage = Frame(self.window, background="#0D0B0B" , pady=20, padx=80)
        frameImage.pack( expand=0, side=TOP)
        labelImage = Label(frameImage, text="Image", background="#0D0B0B", fg="white" , font=("Khmer" , 15))
        labelImage.pack()
        self.canvas = Canvas(frameImage, width=500, height=500, highlightthickness=0 , background="#0D0B0B")
        
        self.image_object = self.canvas.create_image(10, 10, image=self.image, anchor=NW, tags="image")
        self.canvas.pack(fill=BOTH, expand=True)
        self.reload_image()

        # Add the bindings to the entries
        self.user_input_dialog_global.bind("<KeyRelease>", self.test_is_alpha)
        self.user_input_character_global.bind("<KeyRelease>", self.test_is_alpha)
        self.menu_entry.bind("<KeyRelease>", self.test_is_alpha)
        for choice in self.choice_entries:
            choice.bind("<KeyRelease>", self.test_is_alpha)

        # close the window properly
        self.window.protocol("WM_DELETE_WINDOW", lambda: self.quit_window())

    def test_is_alpha(self,e):
        test_char = e.char
        if not self.is_alpha(test_char):
            # error_handler("NO >:( ")
            self.delete_last_character(e.widget, self.is_alpha)

    def delete_last_character(self,widget,test):
        current_widget = widget
        new_text = current_widget.get()
        for char in current_widget.get():
            if not test(char):
                new_text = new_text.replace(char,'')
        current_widget.delete(0,END)
        current_widget.insert(0,new_text)

    def is_alpha(self,char):
        if (not char.isalnum() and not char.isspace() and not char == '\b'
        and not char == '.'and not char == ',' and not char=='!' and not char=='?'): # \b is backspace
            return False
        else:
            return True

    # close the window properly
    def quit_window(self):
        self.model_controller.remove_observer(self)
        self.window.destroy()

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
            case "ask_can_generate":
                if not self.is_linked_to_model_handler:
                    if not data: # Not true, can't generate
                        self.model_controller.broadcast_message("Not allowed to open more than 1 window","error")
                        # self.quit_window()
                    else:
                        self.is_linked_to_model_handler = True
            case _: # We don't care about most updates, only about receiving the output data
                print("ERROR : DISCARDED SUBJECT DATA")
        pass
