


class LabelObject:

    name = None
    background = None
    dialogs_dict = None
    label_type = None
    menu = None

    def __init__(self):
        self.name = ""
        self.background = ""
        self.dialogs_dict = {}
        self.label_type = "label"

    def set_name(self,name):
        self.name = name
    def set_background(self,background):
        self.background = background
    def set_dialogs_dict(self, dialogs_dict):
        self.dialogs_dict = dialogs_dict
    def add_to_dialogs_dict(self,new_dict):
        self.dialogs_dict.update(new_dict)
    def set_menu(self,menu):
        self.menu = menu
    def set_type(self,label_type):
        self.label_type = label_type
    def get_type(self):
        return self.label_type
    def get_name(self):
        return self.name
    def get_background(self):
        return self.background
    def get_dialogs_dict(self):
        return self.dialogs_dict
    def get_menu(self):
        return self.menu




