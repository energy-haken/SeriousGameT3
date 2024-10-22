from tkinter import *
from tkinter.messagebox import showerror

from PIL import ImageTk, Image
from torch.fx.experimental.unification.unification_tools import update_in


class SceneEditWindow:

    photo = None    # needed otherwise Python fucking garbage collector snatch the picture
    user_input_character_global = None
    user_input_dialog_global = None
    descendant = None


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

        button_send = Button(input_frame, text="Validate", command=lambda : self.update())
        button_send.pack()

        self.photo = Image.open("resources/images/angry.png")
        self.photo = self.photo.resize((500,500))
        self.photo = ImageTk.PhotoImage(self.photo)

        lab = Label(window, text=descendant.get_character())
        lab.pack()

        canvas = Canvas(window, width=500, height=500, highlightthickness=0)
        canvas.create_image(10, 10, image=self.photo,anchor=NW)
        canvas.pack(fill=BOTH, expand=True)
        window.mainloop()

    def update(self):
        self.descendant.set_character(str(self.user_input_character_global.get()))
        self.descendant.set_text(str(self.user_input_dialog_global.get()))
