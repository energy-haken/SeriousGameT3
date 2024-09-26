import inspect
from importlib.metadata import Deprecated

import sdk
from sdk import ModelsManagement

global CONST_BASE_MODELS
# Basic models we don't want in our model list
CONST_BASE_MODELS = [sdk.AutoTokenizer,
                     sdk.DemoTextGen,
                     sdk.DemoTextConv,
                     sdk.DemoTextToVideo,
                     sdk.DemoTextToImg,
                     sdk.ModelTransformers,
                     sdk.ModelDiffusers,
                     sdk.ModelsManagement,
                     sdk.ModelsTextConversation,
                     sdk.StableDiffusionPipeline,
                     sdk.Tokenizer,
                     sdk.Devices,
                     sdk.Model,
                     sdk.OpenAIGPTLMHeadModel,
                     sdk.PhiForCausalLM
                     ]

class ModelHandler:

    model_management = None
    available_models = []
    #selected_model = None
    is_active = False
    parameters = None

    def __init__(self):
        self.model_management = ModelsManagement()
        #self.models = [sdk.OpenaiCommunityOpenaiGpt(), sdk.MicrosoftPhi2()]
        self.gather_downloaded_models()
        self.add_models_with_type("text-generation")
        self.parameters = {"selected_model": self.available_models[0],
                           "max_length": 76,
                           "num_return_sequences":1,
                           "do_sample":True,
                           "repetition_penalty":1.2,
                           "temperature":0.7,
                           "top_k":4,
                           "early_stopping":True,
                           "num_beams":20,
                           "truncation":True}
        #self.parameters["selected_model"]
        self.is_active = False

    def gather_downloaded_models(self):
        ### check for downloaded models
        print("Downloaded models")
        for name, downloaded_model in inspect.getmembers(sdk):
            if inspect.isclass(downloaded_model) and downloaded_model not in CONST_BASE_MODELS:

                ### Temp fix because I can't gather the model list from the model_management
                ### and it will break the whole application if someone select an unavailable
                ### model in model_management
                try:
                    if downloaded_model().task == "text-generation":
                        self.available_models.append(downloaded_model())
                        print(name)
                except:
                    print("No task defined")

    def add_models_with_type(self,type):
        for model in self.available_models:
            try:
                if model.task == type:
                    ModelsManagement.add_model(self.model_management, new_model=model)
            except:
                print("No task defined")

    def generate_dialog(self,prompt):
        output = None
        self.parameters["selected_model"].create_pipeline()
        if self.is_active:
            output = self.model_management.generate_prompt(
                prompt, model_name=self.parameters["selected_model"].model_name, max_length=self.parameters["max_length"],
                num_return_sequences=self.parameters["num_return_sequences"], do_sample=self.parameters["do_sample"],
                repetition_penalty=self.parameters["repetition_penalty"], temperature=self.parameters["temperature"],
                top_k=self.parameters["top_k"], early_stopping=self.parameters["early_stopping"],
                num_beams=self.parameters["num_beams"],truncation=self.parameters["truncation"])
        else:
            self.model_management.load_model(self.parameters["selected_model"].model_name)
            self.is_active = True
            output =  self.generate_dialog(prompt)
        return output

    def select_model(self,model_name):
        model1 = self.available_models[0] # temporaire, car il ne voulait pas le faire dans les cases
        model2 = self.available_models[1]
        match model_name:
            case(model1.model_name):
                print("GPT")
                self.parameters["selected_model"] = self.available_models[0]
            case (model2.model_name):
                print("MICRO")
                self.parameters["selected_model"] = self.available_models[1]
            case _:
                print("Unknown model")

    def turn_off_model(self):
        self.model_management.unload_model(self.parameters["selected_model"].model_name)
        self.is_active = False

    # Deprecated
    def turn_model(self):
        if self.is_active:
            self.model_management.unload_model(self.parameters["selected_model"].model_name)
            self.is_active = False
        else:
            self.model_management.load_model(self.parameters["selected_model"].model_name)
            self.is_active = True

    def get_models_name(self):
        name_liste = []
        for model in self.available_models:
            name_liste.append(model.model_name)
        return name_liste
    def get_current_model(self):
        return self.parameters["selected_model"].model_name
    def update_parameters(self,new_parameters):
        self.parameters = new_parameters
        self.select_model(self.parameters["selected_model"]) # update properly the model
        # put back manually some parameters not yet handled by the text module (boolean)
        self.parameters["do_sample"] = True
        self.parameters["early_stopping"] = True
        self.parameters["truncation"] = True
        # Mass cast because I hate Tkinter (integer)
        self.parameters["max_length"] = int(self.parameters["max_length"])
        self.parameters["num_return_sequences"] = int(self.parameters["num_return_sequences"])
        self.parameters["top_k"] = int(self.parameters["top_k"])
        self.parameters["num_beams"] = int(self.parameters["num_beams"])

    def get_parameters(self):
        return self.parameters