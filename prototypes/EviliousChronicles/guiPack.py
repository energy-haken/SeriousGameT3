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
            frameParametersZone.pack(side=LEFT)
            
            #self.image = Image.open("Images/LogoApp.png")
            #self.image = self.photo.resize((500,500))
            #self.image = ImageTk.PhotoImage(self.image)
            #canvas.create_image(10, 10, image=self.image,anchor=NW)

            
            ## Frame pour la case [Project : nomProjet]
            frameProject = Frame(frameParametersZone, width=366, height=54, bg="#383535")
            frameProject.pack()

            labelProject = Label(frameProject , text="Project : " ,background="#383535" , foreground="white" , font=("Khmer", 25))
            labelProject.pack()

            ## Frame pour le bouton pour changer de mode d'utilisation (entre le CPU et le GPU)
            frameProcessingMode = Frame(frameParametersZone, width=366, height=54, bg="#383535")
            frameProcessingMode.pack()

            button_processing_type = Button(frameProcessingMode, background="#383535" , fg="white" ,text="Processing-Mode : CPU",  font=("Khmer", 24) , command=lambda: self.change_processing_type())
            button_processing_type.pack()

           

             ## Frame pour le bouton pour changer de mode d'utilisation (entre image et le text)
            frameGenerationMode = Frame(frameParametersZone, width=366, height=54, bg="#383535")
            frameGenerationMode.pack()

            button_generationMode = Button(frameGenerationMode, background="#383535" , fg="white" ,text="Generation-Mode : Text",  font=("Khmer", 25) , command=lambda: self.change_processing_type())
            button_generationMode.pack()

            

            ## Liste des models
            frameListModel = Frame(frameParametersZone , background="#383535" , width=366 , height=53)
            frameListModel.pack()

            listModel = ttk.Combobox(frameListModel , background="#383535" , font=("Khmer" , 23) , foreground="black" )
            listModel.pack()
            

            ## Paremtres du model

            frameParameterModel = Frame(frameParametersZone , width=311 , height=400 , background="#383535")
            frameParameterModel.pack()

            labelParameters = Label(frameParameterModel , text="PARAMETERS" , background="#383535" , foreground="white" , font=("Khmer" , 25))
            labelParameters.pack()

            labelMaxLength = Label(frameParameterModel , text="Max length" , background="#383535" , foreground="white" , font=("Khmer" , 20))
            labelMaxLength.pack()

            textMaxLenth = Entry(frameParameterModel, width=10)
            textMaxLenth.pack()



            labelReturnedSequence = Label(frameParameterModel , text="Number of returned \n sequences" ,justify="left", background="#383535" , foreground="white" , font=("Khmer" , 20))
            labelReturnedSequence.pack()

            textReturnedSequence = Entry(frameParameterModel, width=10)
            textReturnedSequence.pack()



            labelRepetionPenalty = Label(frameParameterModel , text="Repetition penalty" ,justify="left", background="#383535" , foreground="white" , font=("Khmer" , 20))
            labelRepetionPenalty.pack()

            textRepetionPenalty = Entry(frameParameterModel, width=10)
            textRepetionPenalty.pack()



            labelTemperature = Label(frameParameterModel , text="Temperature" ,justify="left", background="#383535" , foreground="white" , font=("Khmer" , 20))
            labelTemperature.pack()

            textTemperature = Entry(frameParameterModel, width=10)
            textTemperature.pack()



            labelTopK = Label(frameParameterModel , text="Top K" ,justify="left", background="#383535" , foreground="white" , font=("Khmer" , 20))
            labelTopK.pack()

            textTopK = Entry(frameParameterModel, width=10)
            textTopK.pack()


            labelNumberOfBeam = Label(frameParameterModel , text="Number of Beam" ,justify="left", background="#383535" , foreground="white" , font=("Khmer" , 20))
            labelNumberOfBeam.pack()

            textNumberOfBeam = Entry(frameParameterModel, width=10)
            textNumberOfBeam.pack()
            

            ## Frame Contexto

            frameContexte = Frame(canvas, width=400 , height=200 , background="#383535")
            frameContexte.pack()

            frameInput = Frame(canvas, width=400 , height=200 , background="#383535")
            frameInput.pack()


            ## Frame Milieu pour le output

            frameOutput = Frame(canvas , width=900 , height=700 , background="#383535")
            frameOutput.pack()

            ## Frame Droite pour l'historique

            frameHistory = Frame(canvas ,  width=410, height=1000, bg="#1D1B1B")
            frameHistory.pack()


           
            