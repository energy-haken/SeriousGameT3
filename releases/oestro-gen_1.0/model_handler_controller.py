
class ModelController:
    """
    A controller allowing to manipulate a model handler from Guacamole.

    Attributes :
    model_handler : ModelHandler
    """
    model_handler = None
    current_window = None
    current_project = None

    def __init__(self,model_handler):
        self.model_handler = model_handler
    def set_current_project(self,current_project):
        self.current_project = current_project
    def get_current_project(self):
        return self.current_project
    def set_current_window(self,window):
        self.current_window = window
    def get_current_window(self):
        return self.current_window
    def update_reload(self):
        self.model_handler.update_reload()
    def change_processing_method(self):
        self.model_handler.change_processing_method()
    def set_generation_type(self,generation_type):
        self.model_handler.set_generation_type(generation_type)
    def generate(self,prompt):
        self.model_handler.generate(prompt)
    def turn_off_model(self):
        self.model_handler.turn_off_model()
    def update_parameters(self,parameters):
        self.model_handler.update_parameters(parameters)
    def add_observer(self,observer):
        self.model_handler.add_observer(observer)
    def remove_observer(self,observer):
        self.model_handler.remove_observer(observer)
    def flush_observers(self):
        self.model_handler.flush_observers()
    def switch_can_generate(self):
        self.model_handler.switch_can_generate()
    def ask_can_generate(self):
        self.model_handler.ask_can_generate()