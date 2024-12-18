


class Dialog_Label:

    name = None
    background = None
    dialogs_dict = None
    label_type = None

    def __init__(self):
        self.name = ""
        self.background = ""
        self.label_dialog_object = {}
        self.label_type = "label"

    def set_name(self,name):
        self.name = name
    def set_background(self,background):
        self.background = background
    def set_dialogs_object(self, d_object):
        self.label_dialog_object = d_object
    def get_name(self):
        return self.name
    def get_background(self):
        return self.background
    def get_dialogs_object(self):
        return self.label_dialog_object





