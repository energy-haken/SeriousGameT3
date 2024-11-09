

class Act:

    label = None
    content = None
    indent = None

    def __init__(self):
        self.label = ""
        self.content = []
        self.indent = 0 # for tab

    def add_content(self,content):
        self.content.append(content)




