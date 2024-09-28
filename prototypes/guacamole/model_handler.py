import importlib
import inspect
import sdk
from generation_type import GenerationType
from sdk import ModelsManagement

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
# Models type that we can use either for text or image generation
CONST_VALID_MODELS_TYPE = [sdk.ModelTransformers,
                          sdk.ModelDiffusers]

class ModelHandler:
    model_management = None
    available_models = {}
    generation_type = GenerationType.TEXT
    is_active = False
    parameters = None

    def __init__(self):
        self.model_management = ModelsManagement()
        # Gather all downloaded model and select the ones available for tex-generation
        self.__gather_downloaded_models()
        # reset the available models with the currently loaded ones
        self.available_models = self.__get_loaded_model()
        self.parameters = {"selected_model": None,
                           "max_length": 76,
                           "num_return_sequences":1,
                           "do_sample":True,
                           "repetition_penalty":1.2,
                           "temperature":0.7,
                           "top_k":4,
                           "early_stopping":True,
                           "num_beams":20,
                           "truncation":True,
                           "height":512,
                           "width":512}
        self.is_active = False

    def __get_loaded_model(self):
        return self.model_management.loaded_models_cache

    def __gather_downloaded_models(self):
        ### check for downloaded models
        diffusers = []
        transformers = []
        # Gather diffusers (for image gen)
        for model in sdk.ModelDiffusers.__subclasses__():
            if model not in CONST_BASE_MODELS:
                diffusers.append(model)
        # Gather transformers (for text gen)
        for model in sdk.ModelTransformers.__subclasses__():
            if model not in CONST_BASE_MODELS: # Get rid of unwanted model from the original sdk
                transformers.append(model)

        # Add models to the manager according to the chosen generation type
        if self.generation_type == GenerationType.TEXT:
            for model in transformers:
                ModelsManagement.add_model(self.model_management, new_model=model())
        else:
            for model in diffusers:
                ModelsManagement.add_model(self.model_management, new_model=model())
        # Original way to get all models
        # for name, downloaded_model in inspect.getmembers(sdk):
        #     if inspect.isclass(downloaded_model) and downloaded_model not in CONST_BASE_MODELS:
        #         new_model = downloaded_model()
        #         if self.generation_type == GenerationType.TEXT and issubclass(downloaded_model, sdk.ModelTransformers):
        #             ModelsManagement.add_model(self.model_management, new_model= new_model)
        #             print(new_model.model_name)

    def generate_image(self,user_prompt):
        img = []
        if self.is_active:
            # img = self.model.generate_prompt(prompt=self.textbox.get(), height=512, width=512)[0]
            img = self.model_management.generate_prompt(model_name=self.parameters["selected_model"].model_name,
                                                        prompt = user_prompt,
                                                        height=512,width=512)[0]
        else:
            img.append({"error": "Select a model first"})
        return img

    def generate_dialog(self,prompt):
        output = []
        if self.is_active:
            output = self.model_management.generate_prompt(prompt = prompt,
                model_name=self.parameters["selected_model"].model_name,
                max_length=self.parameters["max_length"],
                num_return_sequences=self.parameters["num_return_sequences"], do_sample=self.parameters["do_sample"],
                repetition_penalty=self.parameters["repetition_penalty"], temperature=self.parameters["temperature"],
                top_k=self.parameters["top_k"], early_stopping=self.parameters["early_stopping"],
                num_beams=self.parameters["num_beams"],truncation=self.parameters["truncation"])
        else:
            output.append({"error":"Select a model first"})
        return output

    def select_model(self,model_name):
        for name in self.available_models.keys():
            if name == model_name:
                self.parameters["selected_model"] = self.available_models.get(model_name)
                self.load_model()
                break

    def load_model(self):
        if not self.is_active:
            self.parameters["selected_model"].create_pipeline()
            self.model_management.load_model(self.parameters["selected_model"].model_name)
            self.is_active = True

    def turn_off_model(self):
        if self.is_active:
            self.model_management.unload_model(self.parameters["selected_model"].model_name)
            self.is_active = False

    def get_models_name(self):
        name_liste = []
        for name in self.available_models.keys():
            name_liste.append(name)
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
    def get_generation_type(self):
        return self.generation_type
    def set_generation_type(self,new_type):
        self.generation_type = new_type
        self.turn_off_model() # in case it is already loaded
        self.__gather_downloaded_models()
        # Once a model is loaded, it can't be loaded twice or removed
        self.available_models = self.__get_loaded_model()
        self.sort_model_by_type()

    # Get rid of unused model according to the current generation type
    def sort_model_by_type(self):
        for name in self.available_models.copy().keys(): # So you can pop the unused models without an error
            if not issubclass(self.available_models.get(name).__class__,CONST_VALID_MODELS_TYPE[self.generation_type.value]):
                self.available_models.pop(name)

    def get_parameters(self):
        return self.parameters