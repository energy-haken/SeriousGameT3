import importlib
import inspect
import sdk
from generation_type import GenerationType
from observer import Observer
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
    """
    A model handler allowing to manipulate transformer and diffuser models thanks to the ModelsManagement from the EMF sdk.

    Attributes :
    model_management : ModelManagement
    available_models : Dict
    generation_type : GenerationType (Enum)
    is_active : Bool
    parameters : Dict
    processing : String
    __observers : ArrayList
    """

    model_management = None
    available_models = {}
    generation_type = GenerationType.TEXT
    is_active = False
    parameters = None
    processing = "CPU"
    __observers = []

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
    def add_observer(self,observer: Observer):
        self.__observers.append(observer)
        self.update_observers("parameters",self.parameters)
        #self.update_reload()

    def remove_observer(self,observer: Observer):
        if observer in self.__observers:
            self.__observers.remove(observer)
    def flush_observers(self):
        self.__observers.clear()

    def update_observers(self,data_type,data):
        for obs in self.__observers:
            if obs is not None:
                obs.update(self,data_type,data)
            else:
                print("ERROR in MODEL_HANDLER: null observer")

    def __get_loaded_model(self):
        """
        Get currently added models directly from the ModelsManagement cache
        """
        return self.model_management.loaded_models_cache

    def __gather_downloaded_models(self):
        """
        Gather configured models from the EMF installation.
        If a model is not showing up, ensure it was correctly configured by following the instruction on the
        EMF documentation.

        It also sorts models according to the generation type (Diffusers/Transformers).
        """
        # Add models to the manager according to the chosen generation type
        if self.generation_type == GenerationType.TEXT:
            transformers = self.__gather_model_of_type(sdk.ModelTransformers)
            for model in transformers:
                model_m = model()
                model_m.device = self.return_processing_method()
                ModelsManagement.add_model(self.model_management, new_model=model_m)
        else:
            diffusers = self.__gather_model_of_type(sdk.ModelDiffusers)
            for model in diffusers:
                model_m = model()
                model_m.device = self.return_processing_method()
                ModelsManagement.add_model(self.model_management, new_model=model_m)

    def __gather_model_of_type(self,model_type : sdk):
        """
        Gather configured models from the EMF installation from its class (sdk.Model).

        model_type : sdk.Model
        """
        array = []
        for model in model_type.__subclasses__():
            if model not in CONST_BASE_MODELS: # Get rid of unwanted model from the original sdk
                array.append(model)
        return array

    def change_processing_method(self):
        """
        Change which processor to use, either CPU or GPU.
        CPU can always be used, while GPU can only be used with NVIDIA GPUs
        with CUDA and Torch CUDA properly configured.
        Thus, the CPU version is always a safe bet,
        though it will take much longer to load the model and generate prompts.
        """
        if self.processing == "CPU":
            self.processing = "GPU"
        else:
            self.processing = "CPU"
        self.__reload()

    def get_processing_method(self):
        """
        Get which processing method the model handler is using (CPU or GPU)
        """
        return self.processing

    def return_processing_method(self):
        if self.processing=="CPU":
            return sdk.Devices.CPU
        else:
            return sdk.Devices.GPU

    def generate(self,user_prompt):
        if self.generation_type == GenerationType.TEXT:
            self.generate_dialog(user_prompt)
        else:
            self.generate_image(user_prompt)

    def generate_image(self,user_prompt):
        """
        Generate an image with the user prompt, if the model allows it (The model must be a diffuser type).
        """

        img = []
        if self.is_active:
            # img = self.model.generate_prompt(prompt=self.textbox.get(), height=512, width=512)[0]
            img = self.model_management.generate_prompt(model_name=self.parameters["selected_model"].model_name,
                                                        prompt = user_prompt,
                                                        height=512,width=512)[0]
        else:
            img.append("error")
        self.update_observers("image",img)
        # return img

    def generate_dialog(self,prompt):
        """
        Generate a dialog with the user prompt, if the model allows it (The model must be a transformer type.)
        """

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
            output.append({"error":"Select a model first, then presse apply"})
        self.update_observers("output",output)
        #return output

    def select_model(self,model_name):
        """
        Select a model amidst the configured and selected generation type models.
        """

        for name in self.available_models.keys():
            if name == model_name:
                self.parameters["selected_model"] = self.available_models.get(model_name)
                self.load_model()
                break

    def load_model(self):
        """
        Load the model by creating a pipeline first, then loading it in the model management for future uses.
        """

        if not self.is_active:
            self.parameters["selected_model"].create_pipeline()
            self.model_management.load_model(self.parameters["selected_model"].model_name)
            self.update_observers("current_model",self.get_current_model())
            self.is_active = True

    def turn_off_model(self):
        """
        Unload the currently loaded model without removing it from the cache.
        """

        if self.is_active:
            self.model_management.unload_model(self.parameters["selected_model"].model_name)
            self.parameters["selected_model"] = None
            self.update_observers("current_model",self.get_current_model())
            self.is_active = False

    def get_models_name(self):
        name_liste = []
        for name in self.available_models.keys():
            name_liste.append(name)
        return name_liste
    def get_current_model(self):
        """
        Get currently loaded model name
        """
        if self.parameters["selected_model"] is None:
            return "None"
        else:
            return self.parameters["selected_model"].model_name

    def update_parameters(self,new_parameters):
        """
        Update all parameters sent by the Controller and/or View.
        Not all parameters are supported yet, while some need to be cast to avoid errors.
        """

        # self.parameters = new_parameters
        self.select_model(new_parameters["selected_model"]) # update properly the model
        # put back manually some parameters not yet handled by the text module (boolean)
        self.parameters["do_sample"] = True
        self.parameters["early_stopping"] = True
        self.parameters["truncation"] = True
        # Mass cast because I hate Tkinter (integer)
        self.parameters["max_length"] = int(new_parameters["max_length"])
        self.parameters["num_return_sequences"] = int(new_parameters["num_return_sequences"])
        self.parameters["top_k"] = int(new_parameters["top_k"])
        self.parameters["num_beams"] = int(new_parameters["num_beams"])

        # update model
        self.update_observers("current_model",self.get_current_model())

    def get_generation_type(self):
        return self.generation_type
    def set_generation_type(self,new_type):
        self.generation_type = new_type
        self.__reload()

    def __reload(self):
        """
        Reload the models completely, meaning it will first unload the currently loaded model, clear all added model
        before gathering them all again in the cache.
        """

        self.turn_off_model()  # in case it is already loaded
        self.model_management.loaded_models_cache.clear() # clean up the cache to reload properly the models
        self.__gather_downloaded_models()
        # Once a model is loaded, it can't be loaded twice or removed
        self.available_models = self.__get_loaded_model()
        self.sort_model_by_type()
        self.update_reload()

    def update_reload(self):
        data = {"processing_type":self.get_processing_method(),
                "current_model":self.get_current_model(),
                "model_list":self.get_models_name(),
                "parameters":self.parameters}
        self.update_observers("reload",data)

    # Get rid of unused model according to the current generation type
    def sort_model_by_type(self):
        """
        Sorts models according to the generation type (Only for the UI).
        """

        for name in self.available_models.copy().keys(): # So you can pop the unused models without an error
            if not issubclass(self.available_models.get(name).__class__,CONST_VALID_MODELS_TYPE[self.generation_type.value]):
                self.available_models.pop(name)
        # self.update_observers()

    def get_parameters(self):
        return self.parameters