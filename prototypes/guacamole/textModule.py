from tkinter import *


from modelHandler import ModelHandler

#from tkinter.messagebox import *


class TextModule:

    prompt = None
    output = None
    output_label_global = None
    prompt_label_global = None
    user_input_global = None
    model_handler = None
    model_label = None

    def __init__(self,window):
        self.prompt = "I like trains"
        self.output = "I hate trains"
        self.output_label_global = None
        self.prompt_label_global = None
        self.user_input_global = None
        self.model_handler = ModelHandler()

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




        value = StringVar()
        value.set("Enter a dialog")
        user_input = Entry(input_frame, textvariable=value, width=30)
        user_input.pack(side=LEFT)

        # init labels
        self.output_label_global = output_label
        self.prompt_label_global = prompt_label
        self.user_input_global = user_input

        button_model = Button(input_frame, text="Generate", command=lambda : self.generate_dialog())
        button_model.pack(side=LEFT)

        button_stop = Button(input_frame, text="Stop", command=lambda : self.unload_model())
        button_stop.pack(side=LEFT)

        frame_models = Frame(input_frame, borderwidth=2, relief=GROOVE)
        frame_models.pack(side=RIGHT, padx=10, pady=10)
        Label(frame_models, text="Select Model").pack(padx=10, pady=10)

        list_models = Listbox(frame_models)
        for model in self.model_handler.get_models_name():
            list_models.insert(1, model)

        list_models.pack()

        button_select_model = Button(frame_models, text="Apply", command=lambda : self.select_model(list_models))
        button_select_model.pack()
        self.model_label = Label(frame_models, text="Model name will be here")
        self.model_label.pack()

    def select_model(self,list_models):
        selected_model = "nothing"
        for i in list_models.curselection():
            selected_model = list_models.get(i)
        self.model_handler.select_model(selected_model)
        self.model_label.config(text=self.model_handler.get_current_model())

    def generate_dialog(self):
        self.update_prompt()
        self.output =  self.model_handler.generate_dialog(self.prompt)
        self.update_output()

    def unload_model(self):
        self.model_handler.turn_off_model()

    def update_output(self):
        self.output_label_global.config(text=self.output[0]['generated_text'])
    def update_prompt(self):
        self.prompt = self.user_input_global.get()
        self.prompt_label_global.config(text=self.prompt)









