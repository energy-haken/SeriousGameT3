import importlib
import inspect
from sdk import generated_models
import sdk

# for name, cls in inspect.getmembers(importlib.import_module("myfile"), inspect.isclass):

# for name, model in inspect.getmembers(sdk.generated_models):
#     if inspect.isclass(model):
#         print(model)
# for name, model in inspect.getmembers(generated_models,inspect.isclass):
#     print(model)

# for model in sdk.ModelTransformers.__subclasses__():
#     if model == sdk.ModelsTextConversation:
#         e = 0
#     else:
#         print(model().model_name)
for name, downloaded_model in inspect.getmembers(sdk, inspect.isclass):
    if downloaded_model not in CONST_BASE_MODELS:
        if self.generation_type == GenerationType.TEXT and issubclass(downloaded_model, sdk.ModelTransformers):
            print(downloaded_model().model_name)