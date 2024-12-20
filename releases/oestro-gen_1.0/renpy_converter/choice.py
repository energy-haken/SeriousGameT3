

class Choice:

    title = None
    jump = None

    def __init__(self):
        self.title = ""
        self.text = ""
        self.jump = ""

    def set_title(self,title):
        self.title = title
    def set_jump(self,jump):
        self.jump = jump
    def set_text(self,text):
        self.text = text

    def get_title(self):
        return self.title
    def get_jump(self):
        return self.jump
    def get_text(self):
        return self.text