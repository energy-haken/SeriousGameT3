from importlib.metadata import Deprecated

import sdk
from sdk import ModelsManagement



class ModelHandler:

    model_management = None
    models = []
    selected_model = None
    is_active = False


    def __init__(self):
        self.model_management = ModelsManagement()
        self.selected_model = sdk.OpenaiCommunityOpenaiGpt()
        self.models = [sdk.OpenaiCommunityOpenaiGpt(),sdk.MicrosoftPhi2()]
        self.selected_model.create_pipeline()
        ModelsManagement.add_model(self.model_management, new_model=self.selected_model)
        self.is_active = False

    def generate_dialog(self,prompt):
        output = None
        if self.is_active:
            output = self.model_management.generate_prompt(
                prompt, model_name=self.selected_model.model_name, max_length=76,
                num_return_sequences=1, do_sample=True,
                repetition_penalty=1.2, temperature=0.7, top_k=4,
                early_stopping=True, num_beams=20,
                truncation=True)
        else:
            self.model_management.load_model(self.selected_model.model_name)
            self.is_active = True
            output =  self.generate_dialog(prompt)
        return output

    def select_model(self,model_name):
        model1 = sdk.OpenaiCommunityOpenaiGpt() # temporaire car il voulait pas le faire dans les cases
        model2 = sdk.MicrosoftPhi2()
        match model_name:
            case(model1.model_name):
                print("GPT")
                self.selected_model = sdk.OpenaiCommunityOpenaiGpt()
            case (model2.model_name):
                print("MICRO")
                self.selected_model = sdk.MicrosoftPhi2()
            case _:
                print("Unknown model")

    def turn_off_model(self):
        self.model_management.unload_model(self.selected_model.model_name)
        self.is_active = False

    # Deprecated
    def turn_model(self):
        if self.is_active:
            self.model_management.unload_model(self.selected_model.model_name)
            self.is_active = False
        else:
            self.model_management.load_model(self.selected_model.model_name)
            self.is_active = True

    def get_models_name(self):
        name_liste = []
        for model in self.models:
            name_liste.append(model.model_name)
        return name_liste
    def get_current_model(self):
        return self.selected_model.model_name