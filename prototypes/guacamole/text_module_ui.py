from tkinter import *
from tkinter.messagebox import showerror

from PIL import ImageTk

from generation_type import GenerationType
from model_handler import ModelHandler

def error_handler(message):
    showerror("Error", message)

class TextModule:

    prompt = None
    output = None
    output_label_global = None
    prompt_label_global = None
    user_input_global = None
    model_handler = None
    model_label = None
    parameters = None
    parameters_entry_list = None
    image_label = None
    generation_type = GenerationType.TEXT
    gen_type_label = None

    def __init__(self,window):
        self.prompt = "I like trains"
        self.output = "I hate trains"
        self.output_label_global = None
        self.prompt_label_global = None
        self.user_input_global = None
        self.model_handler = ModelHandler()
        self.parameters = {}

        ### Draw the frame for the user input & output
        input_frame = LabelFrame(window, text="Text Zone", padx=20, pady=20)
        input_frame.pack(fill="both", expand=0, side=TOP)

        prompt_frame = LabelFrame(window, text="Prompt", padx=20, pady=20)
        prompt_frame.pack(fill="both", expand=1, side=LEFT)

        prompt_label = Label(prompt_frame, text="The prompt will be here")
        prompt_label.pack()

        output_frame = LabelFrame(window, text="Results", padx=20, pady=20)
        output_frame.pack(fill="both", expand=1, side=RIGHT)

        output_label = Label(output_frame, text="The dialog will be here")
        output_label.pack()

        # Prompt input
        value = StringVar()
        value.set("Enter a dialog")
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

        button_stop = Button(input_frame, text="Stop", command=lambda : self.unload_model())
        button_stop.pack()

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

        button_apply_parameters = Button(frame_parameters, text="Apply", command=lambda : self.update_parameters())
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
        self.update_models_list()
        list_models.pack()
        self.gen_type_label.pack()

        button_update_gen_type = Button(frame_models, text="Change", command=lambda : self.update_gen_type())
        button_update_gen_type.pack()

    def update_gen_type(self):
        if self.generation_type == GenerationType.TEXT:
            self.model_handler.set_generation_type(GenerationType.IMAGE)
            self.generation_type = GenerationType.IMAGE
        else:
            self.model_handler.set_generation_type(GenerationType.TEXT)
            self.generation_type = GenerationType.TEXT
        self.gen_type_label.config(text=self.generation_type)
        self.update_models_list()
    def update_models_list(self):
        self.parameters_entry_list["selected_model"].delete(0,END)
        for model in self.model_handler.get_models_name():
            self.parameters_entry_list["selected_model"].insert(1, model)

    def generate(self):
        if self.generation_type == GenerationType.TEXT:
            self.generate_dialog()
        else:
            self.generate_image()

    def generate_dialog(self):
        message = "none"
        self.update_prompt()
        self.output =  self.model_handler.generate_dialog(self.prompt)
        if 'error' in self.output[0]:
            message = self.output[0]['error']
            error_handler(message)
        else:
            message = self.output[0]['generated_text']
            self.update_output(message)
    def generate_image(self):
        self.update_prompt()
        img = self.model_handler.generate_image(self.prompt)

        # img = self.model.generate_prompt(prompt=self.textbox.get(), height=512, width=512)[0]
        self.update_image(img)

    def update_image(self,img):
        tkimg = ImageTk.PhotoImage(img[0])
        self.image_label.config(image=tkimg)
        self.image_label.image = tkimg

    def unload_model(self):
        self.model_handler.turn_off_model()
        self.model_label.config(text="None")

    def update_output(self,message):
        self.output_label_global.config(text=message)

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
        self.model_handler.update_parameters(self.parameters)
        self.model_label.config(text=self.model_handler.get_current_model())

    def get_specific_param(self,param):
        return self.model_handler.get_parameters()[param]




