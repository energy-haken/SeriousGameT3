from tkinter import *
from tkinter.messagebox import showerror

from PIL import ImageTk, Image

class TestWindow():

    photo = None    # needed otherwise Python fucking garbage collector snatch the picture

    def __init__(self,window):

        input_frame = LabelFrame(window, text="You are an idiot", padx=20, pady=20)
        input_frame.pack(fill="both", expand=1)

        self.photo = Image.open("resources/images/angry.png")
        self.photo = self.photo.resize((500,500))
        self.photo = ImageTk.PhotoImage(self.photo)

        image_label = Label(input_frame, image=self.photo)
        image_label.pack()


