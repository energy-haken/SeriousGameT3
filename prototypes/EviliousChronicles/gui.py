from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import *
from PIL import ImageTk
from tkinter import ttk

class Gui:
    image = None

    def __init__(self,window):
            
           

            canvas = Canvas(window,width=1920, height=1080,highlightthickness=0)
            ##window.configure(background="#0D0B0B")
            ## window.geometry("1920x1080")

            canvas.configure(background="#0D0B0B")
            
            

            canvas.pack(fill=BOTH, expand=True)

            
            ## Frame a gauche de l'ecran avec les differents parametres du model
            frameParametersZone = Frame(canvas, width=410, height=1000, bg="#1D1B1B")
            frameParametersZone.place(x=30, y=24)
            
            #self.image = Image.open("Images/LogoApp.png")
            #self.image = self.photo.resize((500,500))
            #self.image = ImageTk.PhotoImage(self.image)
            #canvas.create_image(10, 10, image=self.image,anchor=NW)

            
            ## Frame pour la case [Project : nomProjet]
            frameProject = Frame(frameParametersZone, width=366, height=54, bg="#383535")
            frameProject.place(x=25, y=150)

            labelProject = Label(frameProject , text="Project : " ,background="#383535" , foreground="white" , font=("Khmer", 25))
            labelProject.place(x=1 , y=5)

            ## Frame pour le bouton pour changer de mode d'utilisation (entre le CPU et le GPU)
            frameProcessingMode = Frame(frameParametersZone, width=366, height=54, bg="#383535")
            frameProcessingMode.place(x=25, y=250)

            button_processing_type = Button(frameProcessingMode, background="#383535" , fg="white" ,text="Processing-Mode : CPU",  font=("Khmer", 24) , command=lambda: self.change_processing_type())
            button_processing_type.pack()

            button_processing_type.place(x=0 , y=0)

             ## Frame pour le bouton pour changer de mode d'utilisation (entre image et le text)
            frameGenerationMode = Frame(frameParametersZone, width=366, height=54, bg="#383535")
            frameGenerationMode.place(x=25, y=350)

            button_generationMode = Button(frameGenerationMode, background="#383535" , fg="white" ,text="Generation-Mode : Text",  font=("Khmer", 25) , command=lambda: self.change_processing_type())
            button_generationMode.pack()

            button_generationMode.place(x=0 , y=0)

            ## Liste des models
            frameListModel = Frame(frameParametersZone , background="#383535" , width=366 , height=53)
            frameListModel.place(x=25, y=450)

            listModel = ttk.Combobox(frameListModel , background="#383535" , font=("Khmer" , 23) , foreground="black" )
            listModel.place(x=0, y=0)
            

            ## Paremtres du model

            frameParameterModel = Frame(frameParametersZone , width=311 , height=400 , background="#383535")
            frameParameterModel.place(x=50 , y=550) 

            labelParameters = Label(frameParameterModel , text="PARAMETERS" , background="#383535" , foreground="white" , font=("Khmer" , 25))
            labelParameters.place(x=40 , y=5)

            labelMaxLength = Label(frameParameterModel , text="Max length" , background="#383535" , foreground="white" , font=("Khmer" , 20))
            labelMaxLength.place(x=5 , y=55)

            textMaxLenth = Entry(frameParameterModel, width=10)
            textMaxLenth.place(x=240 , y=70)



            labelReturnedSequence = Label(frameParameterModel , text="Number of returned \n sequences" ,justify="left", background="#383535" , foreground="white" , font=("Khmer" , 20))
            labelReturnedSequence.place(x=5 , y=110)

            textReturnedSequence = Entry(frameParameterModel, width=10)
            textReturnedSequence.place(x=240 , y=150)



            labelRepetionPenalty = Label(frameParameterModel , text="Repetition penalty" ,justify="left", background="#383535" , foreground="white" , font=("Khmer" , 20))
            labelRepetionPenalty.place(x=5 , y=190)

            textRepetionPenalty = Entry(frameParameterModel, width=10)
            textRepetionPenalty.place(x=240 , y=200)



            labelTemperature = Label(frameParameterModel , text="Temperature" ,justify="left", background="#383535" , foreground="white" , font=("Khmer" , 20))
            labelTemperature.place(x=5 , y=240)

            textTemperature = Entry(frameParameterModel, width=10)
            textTemperature.place(x=240 , y=250)



            labelTopK = Label(frameParameterModel , text="Top K" ,justify="left", background="#383535" , foreground="white" , font=("Khmer" , 20))
            labelTopK.place(x=5 , y=285)

            textTopK = Entry(frameParameterModel, width=10)
            textTopK.place(x=240 , y=295)


            labelNumberOfBeam = Label(frameParameterModel , text="Number of Beam" ,justify="left", background="#383535" , foreground="white" , font=("Khmer" , 20))
            labelNumberOfBeam.place(x=5 , y=330)

            textNumberOfBeam = Entry(frameParameterModel, width=10)
            textNumberOfBeam.place(x=240 , y=340)
            

            ## Frame Contexto

            frameContexte = Frame(canvas, width=400 , height=200 , background="#383535")
            frameContexte.place(x=500 , y=24)

            frameInput = Frame(canvas, width=400 , height=200 , background="#383535")
            frameInput.place(x=1000 , y=24)


            ## Frame Milieu pour le output

            frameOutput = Frame(canvas , width=900 , height=700 , background="#383535")
            frameOutput.place(x=500, y=300)

            ## Frame Droite pour l'historique

            frameHistory = Frame(canvas ,  width=410, height=1000, bg="#1D1B1B")
            frameHistory.place(x=1470 , y=24)


           
            