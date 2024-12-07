from pathlib import Path
from tkinter import *
from tkinter.messagebox import showerror, showinfo

from PIL import ImageTk
from sympy.core.random import random

from generation_type import GenerationType
from model_handler import ModelHandler
from observer import Observer


def error_handler(message):
    showerror("Error", message)

class TextModule(Observer):

    prompt = None
    output = None
    output_label_global = None
    prompt_label_global = None
    user_input_global = None
    model_controller = None
    model_label = None
    parameters = None
    parameters_entry_list = None
    image_label = None
    generation_type = GenerationType.TEXT
    gen_type_label = None
    processing_type_button = None
    image_cache = None # stored image if the user want to save it
    window = None

    def __init__(self, window, model_controller):
        self.prompt = "I like trains"
        self.output = "I hate trains"
        self.output_label_global = None
        self.prompt_label_global = None
        self.user_input_global = None
        self.parameters = {}
        self.model_controller = model_controller
        self.model_controller.add_observer(self)
        self.window = window

        ### Draw the frame for the user input & output
        input_frame = LabelFrame(self.window, text="Text Zone", padx=20, pady=20)
        input_frame.pack(fill="both", expand=0, side=TOP)

        prompt_frame = LabelFrame(self.window, text="Prompt", padx=20, pady=20)
        prompt_frame.pack(fill="both", expand=1, side=LEFT)

        prompt_label = Label(prompt_frame, text="The prompt will be here")
        prompt_label.pack()

        output_frame = LabelFrame(self.window, text="Results", padx=20, pady=20)
        output_frame.pack(fill="both", expand=1, side=RIGHT)

        output_label = Label(output_frame, text="The dialog will be here")
        output_label.pack()

        # Prompt input
        value = StringVar()
        value.set("Write your prompt here")
        user_input = Entry(input_frame, textvariable=value, width=30)
        user_input.pack()

        # init labels
        self.output_label_global = output_label
        self.prompt_label_global = prompt_label
        self.user_input_global = user_input

        image_label = Label(input_frame)
        image_label.pack()
        self.image_label = image_label

        button_model = Button(input_frame, text="Generate", command=lambda : self.generate())
        button_model.pack()

        button_stop = Button(input_frame, text="Stop", command=lambda : self.stop())
        button_stop.pack()

        button_processing_type = Button(input_frame, text="CURRENTLY : CPU MODE", command=lambda: self.change_processing_type())
        button_processing_type.pack()
        self.processing_type_button = button_processing_type

        save = Button(input_frame, text="Save image", command=lambda: self.save_image())
        save.pack()

        frame_models = LabelFrame(input_frame, text = "Models selection", borderwidth=2, relief=GROOVE)
        frame_models.pack(side=RIGHT, padx=10, pady=10)
        Label(frame_models, text="Select Model").pack(padx=10, pady=10)

        # Parameters UI
        frame_parameters = LabelFrame(input_frame, text = "Parameters Selection", borderwidth=2, relief=GROOVE)
        frame_parameters.pack(side=LEFT, padx=10, pady=10)

        # Parameter_input = p_i
        Label(frame_parameters, text="Max length").pack(padx=10, pady=10)
        value1 = StringVar()
        value1.set(self.get_specific_param("max_length"))
        p_i_max_length = Entry(frame_parameters, textvariable=value1, width=30)
        p_i_max_length.pack()

        Label(frame_parameters, text="Number of returned sequences").pack(padx=10, pady=10)
        value2 = StringVar()
        value2.set(self.get_specific_param("num_return_sequences"))
        p_i_num_return_sequences = Entry(frame_parameters, textvariable=value2,width=30)
        p_i_num_return_sequences.pack()

        Label(frame_parameters, text="Repetition penalty").pack(padx=10, pady=10)
        value3 = StringVar()
        value3.set(self.get_specific_param("repetition_penalty"))
        p_i_repetition_penalty = Entry(frame_parameters, textvariable=value3,width=30)
        p_i_repetition_penalty.pack()

        Label(frame_parameters, text="Temperature").pack(padx=10, pady=10)
        value4 = StringVar()
        value4.set(self.get_specific_param("temperature"))
        p_i_temperature = Entry(frame_parameters, textvariable=value4, width=30)
        p_i_temperature.pack()

        Label(frame_parameters, text="Top K").pack(padx=10, pady=10)
        value5 = StringVar()
        value5.set(self.get_specific_param("top_k"))
        p_i_top_k = Entry(frame_parameters, textvariable=value5, width=30)
        p_i_top_k.pack()

        Label(frame_parameters, text="Number of beams").pack(padx=10, pady=10)
        value6 = StringVar()
        value6.set(self.get_specific_param("num_beams"))
        p_i_num_beams = Entry(frame_parameters, textvariable=value6, width=30)
        p_i_num_beams.pack()

        button_apply_parameters = Button(frame_parameters, text="Apply Parameters & model", command=lambda : self.update_parameters())
        button_apply_parameters.pack()


        # Add all user input entries to the global list


        # Model UI
        self.model_label = Label(frame_models, text="Model name will be here")
        self.model_label.pack()

        list_models = Listbox(frame_models)



        self.parameters_entry_list = {"selected_model":list_models,
                                      "temperature":p_i_temperature,
                                      "num_beams":p_i_num_beams,
                                      "repetition_penalty":p_i_repetition_penalty,
                                      "num_return_sequences":p_i_num_return_sequences,
                                      "top_k":p_i_top_k,
                                      "max_length":p_i_max_length}
        self.gen_type_label = Label(frame_models, text="TEXT")
        #self.update_models_list()
        list_models.pack()
        self.gen_type_label.pack()

        button_update_gen_type = Button(frame_models,
                                        text="Change generation type", command=lambda : self.update_gen_type())
        button_update_gen_type.pack()
        self.model_controller.update_reload() # force update

        # close the window properly
        self.window.protocol("WM_DELETE_WINDOW", lambda: self.quit_window())

    # close the window properly
    def quit_window(self):
        print("KILLING CHILD")
        self.model_controller.remove_observer(self)
        self.window.destroy()

    def change_processing_type(self):
        self.model_controller.change_processing_method()
    def obs_update_processing_type(self,processing_type):
        if self.processing_type_button is not None:
            self.processing_type_button.config(text="CURRENTLY : " +processing_type+" MODE")
    def stop(self):
        self.unload_model()
        self.image_label.config(image="") # clear the image
        self.image_cache = None

    def update_gen_type(self):
        if self.generation_type == GenerationType.TEXT:
            self.model_controller.set_generation_type(GenerationType.IMAGE)
            self.generation_type = GenerationType.IMAGE
        else:
            self.model_controller.set_generation_type(GenerationType.TEXT)
            self.generation_type = GenerationType.TEXT
        self.gen_type_label.config(text=self.generation_type.name)
        #self.update_models_list()

    def obs_update_models_list(self, model_list):
        if self.parameters_entry_list is not None:
            self.parameters_entry_list["selected_model"].delete(0,END)
            for model in model_list:
                self.parameters_entry_list["selected_model"].insert(1, model)

    def generate(self):
        self.update_prompt()
        self.model_controller.generate(self.prompt)

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
            error_handler("No image to save")

    def update_image(self,img):
        if img[0]=="error":
            error_handler("Select a model first, then presse apply")
        else:
            tkimg = ImageTk.PhotoImage(img[0])
            self.image_label.config(image=tkimg)
            self.image_label.image = tkimg
            self.image_cache = tkimg

    def unload_model(self):
        self.model_controller.turn_off_model()


    def update_output(self,message):
        if 'error' in message[0]:
            error_handler(message[0]['error'])
        else:
            self.output_label_global.config(text=message[0]['generated_text'])

    def update_prompt(self):
        self.prompt = self.user_input_global.get()
        self.prompt_label_global.config(text=self.prompt)

    def update_parameters(self):
        for index in self.parameters_entry_list.keys():
            if index == "selected_model":
                selected_model = "nothing"
                for i in self.parameters_entry_list.get(index).curselection():  # search the selected model
                    selected_model = self.parameters_entry_list.get(index).get(i)
                if selected_model != "nothing":
                    self.parameters.update({"selected_model": selected_model})
                else:  # in case there's no selected model
                    self.parameters.update({"selected_model": self.get_specific_param("selected_model")})
            else:
                self.parameters.update({index:float(self.parameters_entry_list.get(index).get())}) # float so the sdk don't break

        # Update the parameters of the model_handler with the updated parameters
        self.model_controller.update_parameters(self.parameters)
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



