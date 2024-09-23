from tkinter import *
#from tkinter.messagebox import *

import sdk
from sdk import ModelsManagement

model_management = ModelsManagement()
selected_model = sdk.MicrosoftPhi2()
selected_model.create_pipeline()
ModelsManagement.add_model(model_management ,new_model=selected_model)
is_active = False
prompt = "I like trains"
output = "I hate trains"
output_label_global = None
prompt_label_global = None
user_input_global = None

def initTextInput(window):
    #def sendText(): # éclaté mais tkt c'est un prototype
        #results.config(text=userInput.get())
   #     prompt = user_input.get()
   #     updatePrompt()

    global output_label_global
    global prompt_label_global
    global user_input_global

    ### Draw the frame for the user input & output
    input_frame = LabelFrame(window, text="Text Zone", padx=20, pady=20)
    input_frame.pack(fill="both", expand=1)

    prompt_frame = LabelFrame(window, text="Prompt", padx=20, pady=20)
    prompt_frame.pack(fill="both", expand=1)

    output_frame = LabelFrame(window, text="Results", padx=20, pady=20)
    output_frame.pack(fill="both", expand=1)



    prompt_label = Label(prompt_frame, text="The prompt will be here")
    prompt_label.pack()

    output_label = Label(output_frame, text="The dialog will be here")
    output_label.pack()

    output_label_global = output_label
    prompt_label_global = prompt_label

    value = StringVar()
    value.set("Enter a dialog")
    user_input = Entry(input_frame, textvariable=value, width=30)
    user_input.pack()
    user_input_global = user_input

    #button = Button(input_frame, text="Send", command=sendText)
    #button.pack()

    button_model = Button(input_frame, text="Generate", command=generateDialog)
    button_model.pack()

    button_stop = Button(input_frame, text="Stop", command=unloadModel)
    button_stop.pack()

    ### END

def generateDialog():
    global output
    global prompt
    updatePrompt()
    if is_active:
        output = model_management.generate_prompt(prompt, model_name=selected_model.model_name, max_length=76,
                                                              num_return_sequences=1, do_sample=True,
                                                              repetition_penalty=1.2, temperature=0.7, top_k=4,
                                                              early_stopping=True, num_beams=20,
                                                              truncation=True)
        updateOutput()
    else:
        launchModel()
def updateOutput():
    global output_label_global
    output_label_global.config(text=output[0]['generated_text'])
def updatePrompt():
    global user_input_global
    global prompt
    prompt = user_input_global.get()
    prompt_label_global.config(text=prompt)


def selectModel(model):
    global selected_model
    selected_model = model # temp


def launchModel():
    global is_active
    model_management.load_model(selected_model.model_name)
    is_active = True

def unloadModel():
    global is_active
    model_management.unload()
    is_active = False












