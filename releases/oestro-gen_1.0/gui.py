import os
from pathlib import Path
import pathlib
import re
from tkinter import *
from tkinter.messagebox import showerror, showinfo
from PIL import ImageTk
from tkinter import ttk
import torch
from sympy.strategies.core import switch

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
    # output_label_global = None
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
        # self.output_label_global = None
        self.prompt_label_global = None
        self.user_input_global = None
        self.parameters = {}
        self.model_controller = model_controller
        self.model_controller.add_observer(self)
        self.button_generate = None
        self.context = None
        self.window = window
        # width = window.winfo_screenwidth()
        # height = window.winfo_screenheight()
        # self.resize_ratio = (width*height)/(1920*1080) # Get the user screen ratio compared to Nathan's screen ratio
        #
        # self.resize_ratio += (1 - self.resize_ratio*1.5) * 0.1  # Make a little bit bigger so it looks better
        #
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

        
        ## Frame to select the Ren'py project to use
        frameProject = Frame(frameParametersZone, width=366, height=54, bg="#383535")
        frameProject.place(x=25, y=150)

        

        pathFolder = pathlib.Path(__file__).parent ## to get the path of the current file
        pathFolder = pathlib.Path.joinpath( pathFolder , "resources/renpy_project") ## add the renpy_project folder to the path

        files = os.listdir(pathFolder) ## to get all the files/folder in the directory
       



        valueProject = StringVar()
        valueProject.set(pathFolder)

        firstProjectBase = "Project : " 
        firstProjectBase += str(pathFolder) ## add the path of the project to the label

        style = ttk.Style()

        style.theme_create('combostyle', parent='alt',
                        settings = {'TCombobox':
                                    {'configure':
                                    {'selectbackground': 'blue',
                                    'fieldbackground': '#383535',
                                    'background': 'white'
                                    }}} ## change the style of the combobox
                        )
        style.theme_use('combostyle') ## use the style for ALL the combobox
        
        ## Combobox to select the project
        comboProject = ttk.Combobox(frameProject , background="#383535" , font=("Khmer" , 23) , foreground="white" , values=files , state="readonly")
        comboProject.bind("<<ComboboxSelected>>", self.update_project_name)
        comboProject.place(x=0 , y=0)
        # comboProject.bind('<>', self.update_project_name())
        self.combobox_project = comboProject # store the combobox to update the project name

       

        ## Frame for the button to change the processing mode (between CPU and GPU)
        frameProcessingMode = Frame(frameParametersZone, width=366, height=54, bg="#383535")
        frameProcessingMode.place(x=25, y=250)

        ## Button to change the processing mode
        button_processing_type = Button(frameProcessingMode, background="#383535" , fg="white" ,text="Processing-Mode : CPU",  font=("Khmer", 24) , command=lambda: self.change_processing_type())
        button_processing_type.pack()
        self.processing_type_button = button_processing_type

        

        ## Frame for the button to change the generation mode (between text and image)
        frameGenerationMode = Frame(frameParametersZone, width=366, height=54, bg="#383535")
        frameGenerationMode.place(x=25, y=350)

        button_generationMode = Button(frameGenerationMode, background="#383535" , fg="white" ,text="Generation-Mode : Text",  font=("Khmer", 22) , command=lambda: self.update_gen_type())
        button_generationMode.pack(fill=BOTH)
        self.gen_type_label = button_generationMode

        ## Frame for the combobox to select the model
        frameListModel = Frame(frameParametersZone , background="#383535" , width=366 , height=53)
        frameListModel.place(x=25, y=450)

        ## Combobox to select the model (yes it's a combobox, not a listbox)
        listModel = ttk.Combobox(frameListModel , background="#383535" , font=("Khmer" , 23) , foreground="white"  , state="readonly")
        listModel.place(x=0, y=0)


        ## All the parameters of the model

        ## Frame for the parameters
        frameParameterModel = Frame(frameParametersZone , width=311 , height=400 , background="#383535")
        frameParameterModel.place(x=50 , y=550) 

        ## Labels for the parameters
        labelParameters = Label(frameParameterModel , text="PARAMETERS" , background="#383535" , foreground="white" , font=("Khmer" , 25))
        labelParameters.place(x=40 , y=5)

        ## Parameters : max_length

        labelMaxLength = Label(frameParameterModel , text="Max length" , background="#383535" , foreground="white" , font=("Khmer" , 20))
        labelMaxLength.place(x=5 , y=55)
        tipMaxLentg = Hovertip(labelMaxLength,'taille de la réponse en caractère')

        value1 = StringVar()
        value1.set(self.get_specific_param("max_length"))
        textMaxLenth = Entry(frameParameterModel, textvariable=value1 ,width=10)
        textMaxLenth.place(x=240 , y=70)

        ## Parameters : num_return_sequences

        labelReturnedSequence = Label(frameParameterModel , text="Number of returned \n sequences" ,justify="left", background="#383535" , foreground="white" , font=("Khmer" , 20))
        labelReturnedSequence.place(x=5 , y=110)
        tipReturnedSequence = Hovertip(labelReturnedSequence,' self explicit')

        value2 = StringVar()
        value2.set(self.get_specific_param("num_return_sequences"))
        textReturnedSequence = Entry(frameParameterModel,textvariable=value2 , width=10)
        textReturnedSequence.place(x=240 , y=150)

        ## Parameters : repetition_penalty

        labelRepetionPenalty = Label(frameParameterModel , text="Repetition penalty" ,justify="left", background="#383535" , foreground="white" , font=("Khmer" , 20))
        labelRepetionPenalty.place(x=5 , y=190)
        tipRepetionPenalty = Hovertip(labelRepetionPenalty,'pénalité lorsque le model se répète \n (favorise un vocabulaire plus diversifié )')

        value3 = StringVar()
        value3.set(self.get_specific_param("repetition_penalty"))
        textRepetionPenalty = Entry(frameParameterModel,textvariable=value3 , width=10)
        textRepetionPenalty.place(x=240 , y=200)

        ## Parameters : temperature

        labelTemperature = Label(frameParameterModel , text="Temperature" ,justify="left", background="#383535" , foreground="white" , font=("Khmer" , 20))
        labelTemperature.place(x=5 , y=240)
        tipTemperature = Hovertip(labelTemperature,' affecte le caractère aléatoire du model \n (plus c\'est petit, plus c\'est prévisible, plus c\'est grand, plus c\'est imprévisible)')
        
        ## Parameters : temperature

        value4 = StringVar()
        value4.set(self.get_specific_param("temperature"))
        textTemperature = Entry(frameParameterModel,textvariable=value4 , width=10)
        textTemperature.place(x=240 , y=250)

        ## Parameters : top_k

        labelTopK = Label(frameParameterModel , text="Top K" ,justify="left", background="#383535" , foreground="white" , font=("Khmer" , 20))
        labelTopK.place(x=5 , y=285)
        tipTopK = Hovertip(labelTopK,'nombre de mots à considérer pour la génération')
        
        value5 = StringVar()
        value5.set(self.get_specific_param("top_k"))
        textTopK = Entry(frameParameterModel,textvariable=value5,  width=10)
        textTopK.place(x=240 , y=295)

        ## Parameters : num_beams

        labelNumberOfBeam = Label(frameParameterModel , text="Number of Beam" ,justify="left", background="#383535" , foreground="white" , font=("Khmer" , 20))
        labelNumberOfBeam.place(x=5 , y=330)
        tipNumberOfBeam = Hovertip(labelNumberOfBeam,'nombre de beam pour la génération')

        value6 = StringVar()
        value6.set(self.get_specific_param("num_beams"))
        textNumberOfBeam = Entry(frameParameterModel, textvariable=value6 ,  width=10)
        textNumberOfBeam.place(x=240 , y=340)
        
        ## Button to apply the parameters
        button_apply_parameters = Button(frameParametersZone, background="#383535" , foreground="white" ,text="Apply Parameters & model" , font=("Khmer", 15), command=lambda : self.update_parameters())
        button_apply_parameters.place(x=75, y=960)
        
        ## Dictionary with the initial parameters
        self.parameters_entry_list = {"selected_model":listModel,
                                    "temperature":textTemperature,
                                    "num_beams":textNumberOfBeam,
                                    "repetition_penalty":textRepetionPenalty,
                                    "num_return_sequences":textReturnedSequence,
                                    "top_k":textTopK,
                                    "max_length":textMaxLenth}            

        ## Frame at the right of the screen with the history of the conversation and the images generated (NOT IMPLEMENTED YET)

        frameHistory = Frame(self.window ,  width=410, height=1000, bg="#1D1B1B")
        frameHistory.pack(side=RIGHT)

      
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

        ## Combobox Contexte (yes it's a combobox, not a listbox AGAIN)
        listContexte = ttk.Combobox(frameContexte , width=25 , font=("Khmer" , 20) , foreground="white")
        listContexte.place(x=5 , y=100)

        listContexte["values"] = ["Context Perso" , "Medieval , with knights and royalty" , "School , with students and teachers" , "Sci-fi , with aliens and spaceships" , "Fantasy , with elves and dragons" , "Modern , with cars and buildings"]
        listContexte.configure(state="readonly")    

        ## Button to apply the context
        buttonValidateContext = Button(frameContexte , text="Validate" , background="#383535" , foreground="white" , font=("Khmer" , 15) , command=lambda: validateContext())
        buttonValidateContext.place(x=150 , y=150)

        def validateContext():
            if(listContexte.get() == "Context Perso" or listContexte.get() == ""):
                self.context = textContexte.get()
                change_validate(self.window , "Context " + textContexte.get() + " validated")
            else:
                self.context = listContexte.get()
                change_validate(self.window , "Context " + listContexte.get() + " validated")

        ## frame Prompt

        frameInput = Frame(frameConIn, width=400 , height=200 , background="#383535")
        frameInput.pack(side=RIGHT)

        value = StringVar()
        value.set("Write your prompt here")

        labelInput = Label(frameInput , text="Prompt" , background="#383535" , foreground="white" , font=("Khmer" , 25))
        labelInput.place(x=150 , y=5)

        textInput = Entry(frameInput ,textvariable=value ,  width=25 , font=("Khmer" , 20))
        textInput.place(x=5 , y=50)

    
        self.user_input_global = textInput # store the user input to use it later
        

        
        ## Canva at the middle of the screen with the output of the generation

        canvaOutput = Canvas(self.window , width=900 , height=700 , background="#383535")
        canvaOutput.pack()
        self.canvas = canvaOutput
        labelPrompt = Label(canvaOutput , text="The prompt :" , background="#383535" , foreground="white" , font=("Khmer" , 25))
       

        self.prompt_label_global = labelPrompt

        labelOutput = Label(canvaOutput , text="Output" , background="#383535" , foreground="white" , font=("Khmer" , 25 ) , justify="left")

        self.output_label_global = labelOutput ## store the output label (it's not displayed on the screen but used to create the tree)

        ## Error_handler in case Torch.Cuda (Nvidia GPU) is not available
        if not torch.cuda.is_available():
            error_handler(self.window , "CUDA not available, expect unhandled bugs")

        ## SCROLLBARS ZONE (for the canvas to navigate through the tree)
        hbar = Scrollbar(self.window, orient=HORIZONTAL)
        hbar.pack(side=BOTTOM, fill=X)
        hbar.config(command=canvaOutput.xview)
        vbar = Scrollbar(self.window, orient=VERTICAL)
        vbar.pack(side=RIGHT, fill=Y)
        vbar.config(command=canvaOutput.yview)
        canvaOutput.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)

        ## Create the first object of the tree
        first_obj = DialogObject()
        first_obj.set_character("Willy Wonka")
        first_obj.set_img("Willy Beans")
        first_obj.set_text("I hate cappuccino")
        first_obj.set_model_controller(self.model_controller)

        first_obj.build_tree(self.canvas)
        self.first_obj = first_obj
        self.model_controller.set_current_window(window) # set the current window to the model controller

        ## Button to generate with the model (and create the tree)
        buttonGenerate = Button(self.window , text="Generate" , background="#383535" , foreground="white" , font=("Khmer" , 15) , command=lambda: self.generate())
        buttonGenerate.pack(side=BOTTOM)
    
        self.button_generate = buttonGenerate

        nb_obj = 10
        self.canvas.configure(scrollregion=(0, 0, 120*nb_obj, 2000))
        
        ## Button to generate the tree as a script file for renpy
        button_generate_script = Button(self.window,  background="#383535" , foreground="white" , font=("Khmer" , 12) ,text="Generate as file", command=lambda : self.generate_text())
        button_generate_script.pack()
        
        ## Button to generate the tree with the generated output
        button_gen_ai = Button(self.window,  background="#383535" , foreground="white"  ,  text="Generate the tree with ai", font=("Khmer" , 12) , command=lambda : self.generate_tree_with_ai())
        button_gen_ai.pack()
        
        # close the window properly
        self.window.protocol("WM_DELETE_WINDOW", lambda: self.quit_window())

        self.model_controller.update_reload()

        # Characters handlers (So the user doesn't input forbidden characters)
        # See doc : https://docs.python.org/3.8/library/stdtypes.html#str.isalpha
        # Local listeners to check the user's inputs
        def test_is_num(e):
            test_char = e.char
            if not is_num(test_char):
                # error_handler("NO >:( ")
                delete_last_character(e.widget,is_num)

        def test_is_float(e):
            test_char = e.char
            if not test_char == "\r":
                if not is_float(test_char):
                    if not test_char == '.': # for float
                        # error_handler("NO >:( ")
                        delete_last_character(e.widget,is_float)
                float_delete_dots(e.widget)

        def test_is_alpha(e):
            test_char = e.char
            if not is_alpha(test_char):
                # error_handler("NO >:( ")
                delete_last_character(e.widget,is_alpha)

        def is_num(char):
            if not char.isnumeric() and not char == '\b':
                return False
            else:
                return True

        def is_float(char):
            try:
                float(char)
                return True
            except ValueError:
                return False

        def is_alpha(char):
            if (not char.isalnum() and not char.isspace() and not char == '\b'
                    and not char == '.' and not char == ',' and not char == '!' and not char == '?'):  # \b is backspace
                return False
            else:
                return True

        def float_delete_dots(widget):
            i = 0
            nb_dots = 0
            new_text = widget.get()
            for char in widget.get():
                if char == '.':
                    nb_dots += 1
                if nb_dots>1:
                    temp_list = list(new_text) # need to convert to list, because string are immutable in python
                    temp_list[i] = " " # can't delete since it's a foreach, so we replace
                    new_text = ''.join(temp_list) # convert back to string
                i += 1
            new_text = new_text.replace(" ", "") # get rid of the white space previously generated
            widget.delete(0, END)
            widget.insert(0, new_text)

        def delete_last_character(widget,test):
            current_widget = widget
            new_text = current_widget.get()
            for char in current_widget.get():
                if not test(char):
                    new_text = new_text.replace(char,'')
            current_widget.delete(0,END)
            current_widget.insert(0,new_text)

        # bindings
        textContexte.bind("<KeyRelease>", test_is_alpha)
        self.user_input_global.bind("<KeyRelease>", test_is_alpha)
        textTemperature.bind("<KeyRelease>", test_is_float)
        textTopK.bind("<KeyRelease>", test_is_num)
        textMaxLenth.bind("<KeyRelease>", test_is_num)
        textNumberOfBeam.bind("<KeyRelease>", test_is_num)
        textRepetionPenalty.bind("<KeyRelease>", test_is_float)
        textReturnedSequence.bind("<KeyRelease>", test_is_num)
        # self.switch()  # disable generation initially, since no scene_edit_window is open yet

    def update_project_name(self,event):
        if self.combobox_project:
            if self.combobox_project.get():
                self.combobox_project.update()
                self.project_name = self.combobox_project.get()
                self.model_controller.set_current_project(self.project_name)
                # print("Project name : " + self.project_name)
            else:
                error_handler(self.window,"No project name")

    def quit_window(self):
        self.model_controller.flush_observers() # just in case
        quit()
        # self.model_controller.remove_observer(self)
        # self.window.destroy()


    def generate_tree_with_ai(self):
        self.canvas.delete("all") # clean up the canvas before generating anything with ai
        count = self.output.count('\n')
        dialogue = self.output.split('\n')
        # print(dialogue)
        self.first_obj.destroy_self(self.canvas)
        obj_p = self.first_obj
        obj_p.set_character("Character0")
        if(dialogue[0] != '' or dialogue[0] != "." or dialogue[0] != '."'):
            obj_p.set_text(dialogue[0])
        else:
            obj_p.set_text(dialogue[1])    
        
        for i in range(count):
            if( i > 0):
                if(dialogue[i] != '' or dialogue[i] != "." or dialogue[i] != ".\"" and dialogue[i] != obj_p.get_text()) : # if the line is not empty
                    obj = DialogObject()
                    obj.set_character("Character" + str(i))
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
        self.prompt = str(self.context) + " \n " + str(self.prompt)
        print(self.prompt)
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
            # self.output_label_global.place_forget()
            # self.output_label_global.place(x=75, y=100)
            self.output = message[0]['generated_text']
           
            self.generate_tree_with_ai()
           
            # self.output_label_global.config(text=message[0]['generated_text'])

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
                if selected_model == "":
                    error_handler(self.window, "No model selected")
                    return
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
    def switch(self):
        if self.button_generate["state"] == "normal":
            self.button_generate["state"] = "disabled"
        else:
            self.button_generate["state"] = "normal"

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
            case "can_generate":
                x = 0
                # self.switch()
            case "broadcast":
                if data["type"]=="error":
                    error_handler(self.window,data["message"])
                else:
                    change_validate(self.window,data["message"])
            case _:
                print("ERROR : COULDN'T READ SUBJECT DATA")
        pass


