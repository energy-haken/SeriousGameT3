import os
from pathlib import Path
import pathlib
import re
from tkinter import *
from tkinter.messagebox import showerror, showinfo
from PIL import ImageTk
from tkinter import ttk
import torch
from dialog_object import DialogObject
from generation_type import GenerationType
from model_observer import ModelObserver
from idlelib.tooltip import Hovertip 
from file_writer import HomeMadeFileWriter
from renpy_converter.object_to_script_converter import ObjToScriptConverter

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


class Gui(ModelObserver):
    image = None
    prompt = None
    output = None
    output_label_global = None
    prompt_label_global = None
    button_generate = None
    user_input_global = None
    model_label = None
    parameters = None
    parameters_entry_list = None
    image_label = None
    generation_type = GenerationType.TEXT
    gen_type_label = None
    processing_type_button = None
    image_cache = None # stored image if the user want to save it
    context = None
    window = None
    canvas = None
    first_obj = None
    resize_ratio = 1.0
    project_name = None
    combobox_project = None
    model_controller = None

    def __init__(self,window ,model_controller):
            
            

        self.prompt = "I like trains"
        self.output = "I hate trains"
        self.output_label_global = None
        self.prompt_label_global = None
        self.user_input_global = None
        self.parameters = {}
        self.model_controller = model_controller
        self.model_controller.add_observer(self)
        self.button_generate = None
        self.context = None
        self.window = window
        width = window.winfo_screenwidth()
        height = window.winfo_screenheight()
        self.resize_ratio = (width*height)/(1920*1080) # Get the user screen ratio compared to Nathan's screen ratio

        self.resize_ratio += (1 - self.resize_ratio*1.5) * 0.1  # Make a little bit bigger so it looks better
    
        self.window.configure(background="#0D0B0B")
        self.window.state('zoomed') #Full screen zoomed
        # self.window.attributes("-fullscreen", True) # Full screen (it looks terrible)
        ## Frame a gauche de l'ecran avec les differents parametres du model
        frameParametersZone = Frame(self.window, width=410, height=1000, bg="#1D1B1B")
        frameParametersZone.pack(side=LEFT, fill=X)
        
        self.image = ImageTk.PhotoImage(file="images\LogoApp.png")
        image_label = Label(frameParametersZone, image=self.image , background="#1D1B1B" , height=199 , width=432)
        self.image_label = image_label
        image_label.place(x=-30, y=-30)

        
        ## Frame pour la case [Project : nomProjet]
        frameProject = Frame(frameParametersZone, width=366, height=54, bg="#383535")
        frameProject.place(x=25, y=150)

        

        pathFolder = pathlib.Path(__file__).parent ## Recuperation du chemin du fichier
        pathFolder = pathlib.Path.joinpath( pathFolder , "resources/renpy_project") ## Ajout du chemin du dossier ressources

        files = os.listdir(pathFolder) ## Recuperation de la liste des fichiers dans le dossier ressources
        # print(files)



        valueProject = StringVar()
        valueProject.set(pathFolder)

        firstProjectBase = "Project : " 
        firstProjectBase += str(pathFolder) ## Ajout du nom du dossier

        style = ttk.Style()

        style.theme_create('combostyle', parent='alt',
                        settings = {'TCombobox':
                                    {'configure':
                                    {'selectbackground': 'blue',
                                    'fieldbackground': '#383535',
                                    'background': 'white'
                                    }}}
                        )
        style.theme_use('combostyle')
        comboProject = ttk.Combobox(frameProject , background="#383535" , font=("Khmer" , 23) , foreground="white" , values=files , state="readonly")
        comboProject.bind("<<ComboboxSelected>>", self.update_project_name)
        comboProject.place(x=0 , y=0)
        # comboProject.bind('<>', self.update_project_name())
        self.combobox_project = comboProject

        ##labelProject = Label(frameProject , text=firstProjectBase ,background="#383535" , foreground="white" , font=("Khmer", 25))
        ##labelProject.place(x=1 , y=5)
        style = ttk.Style()




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

        listModel = ttk.Combobox(frameListModel , background="#383535" , font=("Khmer" , 23) , foreground="white" , values=initial_data , state="readonly")
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
        tipMaxLentg = Hovertip(labelMaxLength,'taille de la réponse en caractère')

        value1 = StringVar()
        value1.set(self.get_specific_param("max_length"))
        textMaxLenth = Entry(frameParameterModel, textvariable=value1 ,width=10)
        textMaxLenth.place(x=240 , y=70)



        labelReturnedSequence = Label(frameParameterModel , text="Number of returned \n sequences" ,justify="left", background="#383535" , foreground="white" , font=("Khmer" , 20))
        labelReturnedSequence.place(x=5 , y=110)
        tipReturnedSequence = Hovertip(labelReturnedSequence,' self explicit')


        value2 = StringVar()
        value2.set(self.get_specific_param("num_return_sequences"))
        textReturnedSequence = Entry(frameParameterModel,textvariable=value2 , width=10)
        textReturnedSequence.place(x=240 , y=150)



        labelRepetionPenalty = Label(frameParameterModel , text="Repetition penalty" ,justify="left", background="#383535" , foreground="white" , font=("Khmer" , 20))
        labelRepetionPenalty.place(x=5 , y=190)
        tipRepetionPenalty = Hovertip(labelRepetionPenalty,'pénalité lorsque le model se répète \n (favorise un vocabulaire plus diversifié )')

        value3 = StringVar()
        value3.set(self.get_specific_param("repetition_penalty"))
        textRepetionPenalty = Entry(frameParameterModel,textvariable=value3 , width=10)
        textRepetionPenalty.place(x=240 , y=200)



        labelTemperature = Label(frameParameterModel , text="Temperature" ,justify="left", background="#383535" , foreground="white" , font=("Khmer" , 20))
        labelTemperature.place(x=5 , y=240)
        tipTemperature = Hovertip(labelTemperature,' affecte le caractère aléatoire du model \n (plus c\'est petit, plus c\'est prévisible, plus c\'est grand, plus c\'est imprévisible)')
        
        

        value4 = StringVar()
        value4.set(self.get_specific_param("temperature"))
        textTemperature = Entry(frameParameterModel,textvariable=value4 , width=10)
        textTemperature.place(x=240 , y=250)



        labelTopK = Label(frameParameterModel , text="Top K" ,justify="left", background="#383535" , foreground="white" , font=("Khmer" , 20))
        labelTopK.place(x=5 , y=285)
        tipTopK = Hovertip(labelTopK,'nombre de mots à considérer pour la génération')

        
        value5 = StringVar()
        value5.set(self.get_specific_param("top_k"))
        textTopK = Entry(frameParameterModel,textvariable=value5,  width=10)
        textTopK.place(x=240 , y=295)


        labelNumberOfBeam = Label(frameParameterModel , text="Number of Beam" ,justify="left", background="#383535" , foreground="white" , font=("Khmer" , 20))
        labelNumberOfBeam.place(x=5 , y=330)
        tipNumberOfBeam = Hovertip(labelNumberOfBeam,'nombre de beam pour la génération')


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

        ## Frame Droite pour l'historique

        frameHistory = Frame(self.window ,  width=410, height=1000, bg="#1D1B1B")
        frameHistory.pack(side=RIGHT)

        frameTest = Frame(frameHistory , width=366 , height=54 , bg="#383535")
        frameTest.place(x=25 , y=150)  
        ## frame contexto + prompt

        frameConIn = Frame(self.window, width=1000 , height=200 , background="#0D0B0B")
        frameConIn.pack(side=TOP , fill=X)


        ## Frame Contexto

        
        frameContexte = Frame(frameConIn, width=400 , height=200 , background="#383535")
        frameContexte.pack(side=LEFT)

        

        labelContexte = Label(frameContexte , text="Context" , background="#383535" , foreground="white" , font=("Khmer" , 25))
        labelContexte.place(x=150 , y=5)

        textContexte = Entry(frameContexte , width=25 , font=("Khmer" , 20))
        textContexte.place(x=5 , y=50)

        listContexte = ttk.Combobox(frameContexte , width=25 , font=("Khmer" , 20) , foreground="white")
        listContexte.place(x=5 , y=100)

        listContexte["values"] = ["Context Perso" , "Context 2" , "Context 3"]
        listContexte.configure(state="readonly")    
        if(listContexte.get() == "Context Perso" or listContexte.get() == ""):
            self.context = listContexte.get()
        else:
            self.context = textContexte.get()

        ## frame Prompt

        frameInput = Frame(frameConIn, width=400 , height=200 , background="#383535")
        frameInput.pack(side=RIGHT)

        value = StringVar()
        value.set("Write your prompt here")

        labelInput = Label(frameInput , text="Prompt" , background="#383535" , foreground="white" , font=("Khmer" , 25))
        labelInput.place(x=150 , y=5)

        textInput = Entry(frameInput ,textvariable=value ,  width=25 , font=("Khmer" , 20))
        textInput.place(x=5 , y=50)

        self.user_input_global = textInput
        

        
        ## Frame Milieu pour le output

        canvaOutput = Canvas(self.window , width=900 , height=700 , background="#383535")
        canvaOutput.pack()
        self.canva = canvaOutput
        labelPrompt = Label(canvaOutput , text="The prompt :" , background="#383535" , foreground="white" , font=("Khmer" , 25))
        #labelPrompt.place(x=5 , y=5)

        self.prompt_label_global = labelPrompt

        labelOutput = Label(canvaOutput , text="Output" , background="#383535" , foreground="white" , font=("Khmer" , 25 ) , justify="left")
        labelOutput.place(x=400 , y=100)

        self.output_label_global = labelOutput

        

        
        

        if not torch.cuda.is_available():
            error_handler(self.window , "CUDA not available, expect unhandled bugs")

        hbar = Scrollbar(self.window, orient=HORIZONTAL)
        hbar.pack(side=BOTTOM, fill=X)
        hbar.config(command=canvaOutput.xview)
        vbar = Scrollbar(self.window, orient=VERTICAL)
        vbar.pack(side=RIGHT, fill=Y)
        vbar.config(command=canvaOutput.yview)
        canvaOutput.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)

        first_obj = DialogObject()
        first_obj.set_character("Willy Wonka")
        first_obj.set_img("Willy Beans")
        first_obj.set_text("I hate cappuccino")
        first_obj.set_model_controller(self.model_controller)

        first_obj.build_tree(self.canva)
        self.first_obj = first_obj
        self.model_controller.set_current_window(window)

        buttonGenerate = Button(self.window , text="Generate" , background="#383535" , foreground="white" , font=("Khmer" , 15) , command=lambda: self.generate())
        buttonGenerate.pack(side=BOTTOM)
    
        self.button_generate = buttonGenerate

        nb_obj = 10
        self.canva.configure(scrollregion=(0, 0, 120*nb_obj, 2000))
        

        button_send = Button(self.window, text="Generate as file", command=lambda : self.generate_text())
        button_send.pack()
        button_gen_ai = Button(self.window, text="Generate the tree with ai", command=lambda : self.generate_tree_with_ai())
        button_gen_ai.pack()
        # close the window properly
        self.window.protocol("WM_DELETE_WINDOW", lambda: self.quit_window())

        self.model_controller.update_reload()
    def update_project_name(self,event):
        if self.combobox_project:
            if self.combobox_project.get():
                self.combobox_project.update()
                self.project_name = self.combobox_project.get()
                self.model_controller.set_current_project(self.project_name)
                print("Project name : " + self.project_name)
            else:
                error_handler(self.window,"No project name")

    def quit_window(self):
        self.model_controller.flush_observers() # just in case
        quit()
        # self.model_controller.remove_observer(self)
        # self.window.destroy()


    def generate_tree_with_ai(self):
        count = self.output_label_global.cget("text").count('\n')
        dialogue = self.output_label_global.cget("text").split('\n')
        print(dialogue)
        obj_p = self.first_obj
        for i in range(count):
            obj = DialogObject()
            obj.set_character("Character1")
            obj.set_text(dialogue[i])
            obj.set_parent(obj_p)
            obj_p = obj
        obj_p.build_tree(self.canvas)
        
    def change_processing_type(self):
        self.model_controller.change_processing_method()
    def obs_update_processing_type(self,processing_type):
        if self.processing_type_button is not None:
            self.processing_type_button.config(text="Processing-Mode  :" +processing_type+"")
    # def stop(self):
        # self.unload_model()
        # self.image_label.config(image="") # clear the image
        # self.image_cache = None

    def update_gen_type(self):
        if self.generation_type == GenerationType.TEXT:
            self.model_controller.set_generation_type(GenerationType.IMAGE)
            self.generation_type = GenerationType.IMAGE
            self.gen_type_label.config(text="Generation-Mode : Image  ")
        else:
            self.model_controller.set_generation_type(GenerationType.TEXT)
            self.generation_type = GenerationType.TEXT
            self.gen_type_label.config(text="Generation-Mode : Text     ")
        
        #self.update_models_list()

    def obs_update_models_list(self, model_list):
        
        self.parameters_entry_list["selected_model"].configure(values=model_list)
        ##for model in model_list:
            ##      print(model)

                
    def generate(self):
        self.update_prompt()
        self.model_controller.generate(self.prompt)
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
            error_handler(self.window ,"No image to save")

    # def update_image(self,img):
    #     if img[0]=="error":
    #         error_handler(self.window , "Select a model first, then presse apply")
    #     else:
    #         tkimg = ImageTk.PhotoImage(img[0])
    #         self.image_label.config(image=tkimg)
    #         self.image_label.image = tkimg
    #         self.image_cache = tkimg

    def unload_model(self):
        self.model_controller.turn_off_model()


    def update_output(self,message):
        if 'error' in message[0]:
            error_handler(self.window , message[0]['error'])
        else:
            self.output_label_global.place_forget()
            self.output_label_global.place(x=75, y=100)
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
                    change_validate(self.window, "Model " + selected_model + " selected")
                else:
                    self.parameters.update({"selected_model": self.get_specific_param("selected_model")})
            else:
                try:
                    value = float(self.parameters_entry_list.get(index).get())
                    self.parameters.update({index: value})
                except ValueError:
                    error_handler(self.window, f"Parameter {index} is not a valid number")
                    return

        self.model_controller.update_parameters(self.parameters)
    def obs_update_parameters(self,data):
        self.parameters = data

    def obs_update_current_model(self, current_model):
        if self.model_label is not None:
            self.model_label.config(text=current_model)

    def get_specific_param(self,param):
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
                # self.update_image(data) # No longer in use
                x = 0
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


    def generate_text(self):
        base_path = "resources/renpy_project/"+self.project_name+"/game/" # TODO : With the project selection combobox
        # Init fileWriter
        file_writer = HomeMadeFileWriter()
        file_writer.set_mode("w")
        file_writer.set_file(base_path+"script.rpy")

        # Gather information on tree
        tree_information = self.first_obj.get_tree_information()

        # Init ObjConverter
        obj_converter = ObjToScriptConverter()
        obj_converter.set_label_list(tree_information["labels"])
        obj_converter.set_characters_list(tree_information["characters"])

        # Convert and write to file
        file_writer.write(obj_converter.convert())
        change_validate(self.window,"Script generated at : "+base_path)
