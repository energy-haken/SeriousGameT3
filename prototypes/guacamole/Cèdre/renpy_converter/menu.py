class Menu:

    title = None
    choice_list = None

    def __init__(self):
        self.title = ""
        self.choice_list = []

    def set_tile(self,title):
        self.title = title
    def add_choice(self,choice):
        self.choice_list.append(choice)

    def get_title(self):
        return self.title
    def get_choice_list(self):
        return self.choice_list