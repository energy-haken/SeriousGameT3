from tkinter import *
from tkinter.messagebox import showerror

from PIL import ImageTk, Image

class DialogTreeObject():

    name = "Betrayal Scene"
    descendants = []
    text = "Amogus"
    img = None
    object = None
    canvas = None
    parent = None

    # FULLY DEPRECATED
    def __init__(self, in_canvas,parent,offset):
        self.canvas = in_canvas
        self.parent = parent
        coords_parent = self.canvas.coords(self.parent)
        print(coords_parent)
        # coords_parent[3]/ 2
        self.object = self.canvas.create_oval(10, 10, 80, 80, outline="black", fill="white", width=2)
        self.canvas.move(self.object,coords_parent[2]+40,0+offset)
        coords_current_obj = self.canvas.coords(self.object) # starting coords
        self.canvas.create_line(coords_current_obj[2]+40, # ending point x
                           (coords_current_obj[3] / 2 )+offset, # ending point y
                           coords_current_obj[2],       # starting point x
                           (coords_current_obj[3] / 2 )+offset)     # starting point y

    def addDescendant(self,descendant):
        self.descendants.append(descendant)
        for index, descendant in enumerate(self.getDescendants()):
            self.buildDescendant(descendant,index)



    def buildDescendant(self,descendant,index_x):
        index = index_x+1
        coords_current_obj = self.canvas.coords(self.object) # starting coords
        self.canvas.create_line(coords_current_obj[2]+40, # ending point x
                           coords_current_obj[3] / 2 + index*40, # ending point y
                           coords_current_obj[2],       # starting point x
                           coords_current_obj[3] / 2)     # starting point y
        DialogTreeObject(self.canvas,self.object,index*40)


    def getObject(self):
        return self.object
    def getDescendants(self):
        return self.descendants