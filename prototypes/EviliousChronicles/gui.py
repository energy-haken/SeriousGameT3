from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import *
from tkinter import ttk

class Gui:
    def __init__(self,window):
            
           
            canvas = Canvas(window,width=1920, height=1080,highlightthickness=0)
            ##window.configure(background="#0D0B0B")
            ## window.geometry("1920x1080")

            canvas.configure(background="#0D0B0B")
            

            canvas.create_rectangle(700, 300, 30, 80, fill="grey", width=366 ) 

            canvas.pack(fill=BOTH, expand=True)

            

            frameParametersZone = Frame(canvas, width=410, height=1000, bg="#1D1B1B")
            frameParametersZone.place(x=30, y=24)

            frameProject = Frame(frameParametersZone, width=366, height=54, bg="#383535")
            frameProject.place(x=25, y=100)