from tkinter import *
from tkinter.messagebox import *
import menu_ui
from gui1 import TextModule
import torch

#if not torch.cuda.is_available():


    #print(torch.__version__)


# https://python.doctor/page-tkinter-interface-graphique-python-tutoriel

def placeHolder():
    showinfo("placeHolder", "Test")
def error_handler(message):
    showerror("Error", message)

window = Tk()
window.iconbitmap("resources/images/icon.ico")
window.title("Œstro-gen")

# if hasattr(torch._C, "_cuda_getDeviceCount"): # test if torch is compiled with cuda to avoid further errors

if not torch.cuda.is_available():
    error_handler("CUDA not available, expect unhandled bugs")

menu_ui.init(window)
text_module = TextModule(window)

#test = TestWindow(window)
#textFrame = LabelFrame(window, text="Text Frame", padx=20, pady=20)
#textFrame.grid(row=1,  column=2,  padx=10,  pady=5)

window.mainloop()