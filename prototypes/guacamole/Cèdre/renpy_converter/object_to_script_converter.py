

class ObjToScriptConverter:


    list_characters = None
    dialogs_dict = None

    def __init__(self):
        self.list_characters = []
        self.dialogs_dict = {}

    def set_characters_list(self,list):
        self.list_characters = self.remove_duplicates(list)
    def set_dialogs_dict(self, dialogs):
        self.dialogs_dict = dialogs
    def remove_duplicates(self,dup_list):
        return list(dict.fromkeys(dup_list)) # remove duplicated elements

    def instantiate_character(self,character):
        return_string = "define " + character.replace(" ", "_") + " = Character(\""+character+"\")\n"
        return return_string

    def instantiate_characters(self):
        character_instantiation = ""
        for character in self.list_characters:
            character_instantiation += self.instantiate_character(character)
        return character_instantiation
    # def remove_spaces(self):
    #     for i in range(len(self.list_characters)):
    #         character = self.list_characters[i]
    #         self.list_characters.remove(character)
    #         character = character.replace(" ", "_")
    #         self.list_characters.append(character)


    #TODO : class menu and choice
    def generate_menu(self,menu):
        menu_text = "    menu:\n"
        menu_text += "    " + menu.get_first_dialog()

        for choice in menu.get_choices():
            menu_text += self.generate_choice(choice)

        return menu_text
    # uses : "    " instead of "\t" because RenPy doesn't accept tab! What a chicanery!
    def generate_choice(self,choice):
        choice_text = "    " + choice.get_choice_text()
        choice_text += "    " + choice.get_choice_dialog()
        choice_text += "    " + choice.get_choice_jump()

        return choice_text

    # character.split("*", 1)[0] allow to get rid of the dialog identifier ie : my_character*12
    def generate_dialogs(self):
        dialog_string = ""
        last_character = ""
        for character,dialog in self.dialogs_dict.items():
            if not last_character.__eq__(character) and last_character != "":
                dialog_string += "    " + "hide " + last_character.split("*", 1)[0] + "\n"
                dialog_string += "    " + "show " + str(character.split("*", 1)[0]) + "\n"
                dialog_string += "    " + str(character.split("*", 1)[0]) + " \" " + dialog + " \" \n"
            elif last_character == "":
                dialog_string += "    " + "show " + str(character.split("*", 1)[0]) + "\n"
                dialog_string += "    " + str(character.split("*", 1)[0]) + " \" " + dialog + " \" \n"
            else:
                dialog_string += "    " + str(character.split("*", 1)[0]) + " \" " + dialog + " \" \n"
        return dialog_string

    def convert(self):
        converted_string = self.instantiate_characters()
        converted_string += "label start:\n    scene bg room\n"
        converted_string += self.generate_dialogs()
        converted_string += "    " + "return\n"
        return converted_string
