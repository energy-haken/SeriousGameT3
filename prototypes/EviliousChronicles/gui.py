
import os
from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
import pathlib
import re
from tkinter import *
from tkinter.messagebox import showerror, showinfo
from PIL import ImageTk
from tkinter import ttk
import torch
from generation_type import GenerationType
from model_handler import ModelHandler
from observer import Observer

def error_handler(root , message):
    #showerror("Error", message)
    ## frame error

    frameError = Frame(root , width=400 , height=60 , bg="red")
                
    frameError.place(x=0 , y=0)
    frameError.lift()

    labelError = Label(frameError , text=message , background="red" , foreground="white" , font=("Khmer" , 15))
                
    labelError.place(x=10 , y=5)

    root.after(5000, frameError.place_forget)

def change_validate(root , message):
    frameValidate = Frame(root , width=400 , height=60 , bg="green")
    frameValidate.place(x=0 , y=0)
    frameValidate.lift()

    labelValidate = Label(frameValidate , text=message , background="green" , foreground="white" , font=("Khmer" , 15))
    labelValidate.place(x=10 , y=5)

    root.after(5000, frameValidate.place_forget)


class Gui(Observer):
    image = None
    prompt = None
    output = None
    output_label_global = None
    prompt_label_global = None
    button_generate = None
    user_input_global = None
    model_handler = None
    model_label = None
    parameters = None
    parameters_entry_list = None
    image_label = None
    generation_type = GenerationType.TEXT
    gen_type_label = None
    processing_type_button = None
    image_cache = None # stored image if the user want to save it
    fond = None

    def __init__(self,window):
            
           

            self.prompt = "I like trains"
            self.output = "I hate trains"
            self.output_label_global = None
            self.prompt_label_global = None
            self.user_input_global = None
            self.parameters = {}
            self.model_handler = ModelHandler()
            self.model_handler.add_observer(self)
            self.button_generate = None
           

            canvas = Canvas(window,width=1920, height=1080,highlightthickness=0)
            ##window.configure(background="#0D0B0B")
            ## window.geometry("1920x1080")

            canvas.configure(background="#0D0B0B")
            
            

            canvas.pack(fill=BOTH, expand=True)

            self.fond = canvas
                

            ## Frame a gauche de l'ecran avec les differents parametres du model
            frameParametersZone = Frame(canvas, width=410, height=1000, bg="#1D1B1B")
            frameParametersZone.place(x=30, y=24)
            
            self.image = ImageTk.PhotoImage(file="images\LogoApp.png")
            image_label = Label(frameParametersZone, image=self.image , background="#1D1B1B" , height=199 , width=432)
            image_label.place(x=-30, y=-30)

            
            ## Frame pour la case [Project : nomProjet]
            frameProject = Frame(frameParametersZone, width=366, height=54, bg="#383535")
            frameProject.place(x=25, y=150)

            

            pathFolder = pathlib.Path(__file__).parent ## Recuperation du chemin du fichier
            pathFolder = os.path.basename(pathFolder).split('/')[-1] ## Recuperation du nom du dossier
            valueProject = StringVar()
            valueProject.set(pathFolder)

            firstProjectBase = "Project : " 
            firstProjectBase += str(pathFolder) ## Ajout du nom du dossier


            labelProject = Label(frameProject , text=firstProjectBase ,background="#383535" , foreground="white" , font=("Khmer", 25))
            labelProject.place(x=1 , y=5)
    

            ## Frame pour le bouton pour changer de mode d'utilisation (entre le CPU et le GPU)
            frameProcessingMode = Frame(frameParametersZone, width=366, height=54, bg="#383535")
            frameProcessingMode.place(x=25, y=250)

            button_processing_type = Button(frameProcessingMode, background="#383535" , fg="white" ,text="Processing-Mode : CPU",  font=("Khmer", 24) , command=lambda: self.change_processing_type())
            button_processing_type.pack()
            self.processing_type_button = button_processing_type

           

             ## Frame pour le bouton pour changer de mode d'utilisation (entre image et le text)
            frameGenerationMode = Frame(frameParametersZone, width=366, height=54, bg="#383535")
            frameGenerationMode.place(x=25, y=350)

            button_generationMode = Button(frameGenerationMode, background="#383535" , fg="white" ,text="Generation-Mode : Text",  font=("Khmer", 22) , command=lambda: self.update_gen_type())
            button_generationMode.pack(fill=BOTH)
            self.gen_type_label = button_generationMode

            #button_generationMode.place(x=0 , y=0)

            ## Liste des models
            frameListModel = Frame(frameParametersZone , background="#383535" , width=366 , height=53)
            frameListModel.place(x=25, y=450)

            initial_data = ["Plan A", "Plan B"]

            listModel = ttk.Combobox(frameListModel , background="#383535" , font=("Khmer" , 23) , foreground="black" , values=initial_data )
            listModel.place(x=0, y=0)

            button_apply_parameters = Button(frameParametersZone, text="Apply Parameters & model", command=lambda : self.update_parameters())
            button_apply_parameters.place(x=25, y=500)
            

            ## Paremtres du model

            frameParameterModel = Frame(frameParametersZone , width=311 , height=400 , background="#383535")
            frameParameterModel.place(x=50 , y=550) 

            labelParameters = Label(frameParameterModel , text="PARAMETERS" , background="#383535" , foreground="white" , font=("Khmer" , 25))
            labelParameters.place(x=40 , y=5)

            labelMaxLength = Label(frameParameterModel , text="Max length" , background="#383535" , foreground="white" , font=("Khmer" , 20))
            labelMaxLength.place(x=5 , y=55)

            value1 = StringVar()
            value1.set(self.get_specific_param("max_length"))
            textMaxLenth = Entry(frameParameterModel, textvariable=value1 ,width=10)
            textMaxLenth.place(x=240 , y=70)



            labelReturnedSequence = Label(frameParameterModel , text="Number of returned \n sequences" ,justify="left", background="#383535" , foreground="white" , font=("Khmer" , 20))
            labelReturnedSequence.place(x=5 , y=110)

            value2 = StringVar()
            value2.set(self.get_specific_param("num_return_sequences"))
            textReturnedSequence = Entry(frameParameterModel,textvariable=value2 , width=10)
            textReturnedSequence.place(x=240 , y=150)



            labelRepetionPenalty = Label(frameParameterModel , text="Repetition penalty" ,justify="left", background="#383535" , foreground="white" , font=("Khmer" , 20))
            labelRepetionPenalty.place(x=5 , y=190)

            value3 = StringVar()
            value3.set(self.get_specific_param("repetition_penalty"))
            textRepetionPenalty = Entry(frameParameterModel,textvariable=value3 , width=10)
            textRepetionPenalty.place(x=240 , y=200)



            labelTemperature = Label(frameParameterModel , text="Temperature" ,justify="left", background="#383535" , foreground="white" , font=("Khmer" , 20))
            labelTemperature.place(x=5 , y=240)

            value4 = StringVar()
            value4.set(self.get_specific_param("temperature"))
            textTemperature = Entry(frameParameterModel,textvariable=value4 , width=10)
            textTemperature.place(x=240 , y=250)



            labelTopK = Label(frameParameterModel , text="Top K" ,justify="left", background="#383535" , foreground="white" , font=("Khmer" , 20))
            labelTopK.place(x=5 , y=285)
            
            value5 = StringVar()
            value5.set(self.get_specific_param("top_k"))
            textTopK = Entry(frameParameterModel,textvariable=value5,  width=10)
            textTopK.place(x=240 , y=295)


            labelNumberOfBeam = Label(frameParameterModel , text="Number of Beam" ,justify="left", background="#383535" , foreground="white" , font=("Khmer" , 20))
            labelNumberOfBeam.place(x=5 , y=330)

            value6 = StringVar()
            value6.set(self.get_specific_param("num_beams"))
            textNumberOfBeam = Entry(frameParameterModel, textvariable=value6 ,  width=10)
            textNumberOfBeam.place(x=240 , y=340)
            

            self.parameters_entry_list = {"selected_model":listModel,
                                      "temperature":textTemperature,
                                      "num_beams":textNumberOfBeam,
                                      "repetition_penalty":textRepetionPenalty,
                                      "num_return_sequences":textReturnedSequence,
                                      "top_k":textTopK,
                                      "max_length":textMaxLenth}            

            ## Frame Contexto

            frameContexte = Frame(canvas, width=400 , height=200 , background="#383535")
            frameContexte.place(x=500 , y=24)

            

            labelContexte = Label(frameContexte , text="Context" , background="#383535" , foreground="white" , font=("Khmer" , 25))
            labelContexte.place(x=150 , y=5)

            textContexte = Entry(frameContexte , width=25 , font=("Khmer" , 20))
            textContexte.place(x=5 , y=50)

            listContexte = ttk.Combobox(frameContexte , width=25 , font=("Khmer" , 20))
            listContexte.place(x=5 , y=100)

            listContexte["values"] = ["Context 1" , "Context 2" , "Context 3"]

            ## frame Prompt

            frameInput = Frame(canvas, width=400 , height=200 , background="#383535")
            frameInput.place(x=1000 , y=24)

            value = StringVar()
            value.set("Write your prompt here")

            labelInput = Label(frameInput , text="Prompt" , background="#383535" , foreground="white" , font=("Khmer" , 25))
            labelInput.place(x=150 , y=5)

            textInput = Entry(frameInput ,textvariable=value ,  width=25 , font=("Khmer" , 20))
            textInput.place(x=5 , y=50)

            self.user_input_global = textInput
            


            ## Frame Milieu pour le output

            frameOutput = Frame(canvas , width=900 , height=700 , background="#383535")
            frameOutput.place(x=500, y=300)

            labelPrompt = Label(frameOutput , text="The prompt :" , background="#383535" , foreground="white" , font=("Khmer" , 25))
            labelPrompt.place(x=5 , y=5)

            self.prompt_label_global = labelPrompt

            labelOutput = Label(frameOutput , text="Output" , background="#383535" , foreground="white" , font=("Khmer" , 25))
            labelOutput.place(x=5 , y=5)

            self.output_label_global = labelOutput

            ## Frame Droite pour l'historique

            frameHistory = Frame(canvas ,  width=410, height=1000, bg="#1D1B1B")
            frameHistory.place(x=1470 , y=24)

            buttonGenerate = Button(canvas , text="Generate" , background="#383535" , foreground="white" , font=("Khmer" , 15) , command=lambda: self.generate())
            buttonGenerate.place(x=1000 , y=1010)
        
            self.button_generate = buttonGenerate
            

            if(textInput.focus()):
                buttonGenerate.configure(text="test")

            if not torch.cuda.is_available():
                errorValue = error_handler(canvas , "CUDA not available, expect unhandled bugs")

                

            self.model_handler.update_reload() 
           
    def change_processing_type(self):
        self.model_handler.change_processing_method()
    def obs_update_processing_type(self,processing_type):
        if self.processing_type_button is not None:
            self.processing_type_button.config(text="Processing-Mode  :" +processing_type+"")
    def stop(self):
        self.unload_model()
        self.image_label.config(image="") # clear the image
        self.image_cache = None

    def update_gen_type(self):
        if self.generation_type == GenerationType.TEXT:
            self.model_handler.set_generation_type(GenerationType.IMAGE)
            self.generation_type = GenerationType.IMAGE
        else:
            self.model_handler.set_generation_type(GenerationType.TEXT)
            self.generation_type = GenerationType.TEXT
        self.gen_type_label.config(text="Generation-Mode : " + self.generation_type.name)
        #self.update_models_list()

    def obs_update_models_list(self, model_list):
       
        self.parameters_entry_list["selected_model"].configure(values=model_list)
        ##for model in model_list:
          ##      print(model)

                
    def generate(self):
        self.update_prompt()
        self.model_handler.generate(self.prompt)
        self.button_generate.configure(text="Regenerate") # change the button text to regenerate
        

    def save_image(self):
        base_path = "resources/images/"
        file_name = "generated_img"
        if not self.image_cache is None:
            img = ImageTk.getimage(self.image_cache) # get the actual image
            nb = 1
            if Path(base_path).is_dir():    # if the directory exist, do
                while Path(base_path + file_name + str(nb) + ".png").is_file():
                    nb+=1
                img.save(base_path + file_name + str(nb) + ".png", "PNG")
                showinfo("Saved", "Image saved at : "+base_path)
        else:
            error_handler(self.fond ,"No image to save")

    def update_image(self,img):
        if img[0]=="error":
            error_handler(self.fond , "Select a model first, then presse apply")
        else:
            tkimg = ImageTk.PhotoImage(img[0])
            self.image_label.config(image=tkimg)
            self.image_label.image = tkimg
            self.image_cache = tkimg

    def unload_model(self):
        self.model_handler.turn_off_model()


    def update_output(self,message):
        if 'error' in message[0]:
            error_handler(self.fond , message[0]['error'])
        else:
            self.output_label_global.config(text=message[0]['generated_text'])

    def update_prompt(self):
        self.prompt = self.user_input_global.get()
        self.prompt_label_global.config(text=self.prompt)

    def update_parameters(self):
        for index in self.parameters_entry_list.keys():
            if index == "selected_model":
                selected_model = self.parameters_entry_list.get(index).get()
                if selected_model:
                    self.parameters.update({"selected_model": selected_model})
                    change_validate(self.fond, "Model " + selected_model + " selected")
                else:
                    self.parameters.update({"selected_model": self.get_specific_param("selected_model")})
            else:
                try:
                    value = float(self.parameters_entry_list.get(index).get())
                    self.parameters.update({index: value})
                except ValueError:
                    error_handler(self.fond, f"Parameter {index} is not a valid number")
                    return

        self.model_handler.update_parameters(self.parameters)
    def obs_update_parameters(self,data):
        self.parameters = data

    def obs_update_current_model(self, current_model):
        if self.model_label is not None:
            self.model_label.config(text=current_model)

    def get_specific_param(self,param):
        # return self.model_handler.get_parameters()[param]
        return self.parameters[param]

    def update(self,subject,data_type,data) -> None:
        """
        Receive update from subject.
        """

        # Determine the type of update given
        match data_type:
            case "output":
                self.update_output(data)
            case "model_list":
                self.obs_update_models_list(data)
            # case "gen_type": # Since it's a button exclusive command, shouldn't be used with observer-type update
            #     self.update_gen_type()
            case "current_model":
                self.obs_update_current_model(data)
            case "image":
                self.update_image(data)
            case "parameters":
                self.obs_update_parameters(data)
            case "reload":
                self.obs_update_models_list(data["model_list"])
                # self.update_gen_type() # same as above
                self.obs_update_current_model(data["current_model"])
                self.obs_update_processing_type(data["processing_type"])
                self.obs_update_parameters(data["parameters"])
            case _:
                print("ERROR : COULDN'T READ SUBJECT DATA")
        pass


