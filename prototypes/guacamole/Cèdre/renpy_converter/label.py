


class Label:

    name = None
    background = None
    dialogs_dict = None
    label_type = None

    def __init__(self):
        self.name = ""
        self.background = ""
        self.get_dialogs_dict = {}
        self.label_type = "label"

    def set_name(self,name):
        self.name = name
    def get_name(self):
        return self.name
    def get_background(self):
        return self.background
    def get_dialogs_object(self):
        return self.dialogs_dict





