

class ObjToScriptConverter:


    list_characters = None
    dialogs_dict = None

    def __init__(self):
        self.list_characters = []
        self.dialogs_dict = {}

    def set_characters_list(self,list):
        self.list_characters = self.remove_duplicates(list)
    def set_dialogs_list(self,dialogs):
        self.dialogs_dict = dialogs
    def remove_duplicates(self,dup_list):
        return list(dict.fromkeys(dup_list)) # remove duplicated elements

    def instantiate_character(self,character):
        return_string = "define " + character + " = Character(\""+character+"\")\n"
        return return_string

    def instantiate_characters(self):
        character_instantiation = ""
        for character in self.list_characters:
            character_instantiation += self.instantiate_character(character)
        return character_instantiation



    def generate_dialogs(self):
        dialog_string = ""
        last_character = ""
        for character,dialog in self.dialogs_dict.items():
            if not last_character.__eq__(character) and last_character is not "":
                dialog_string += "\t" + "hide " + last_character + "\n"
                dialog_string += "\t" + "show " + str(character) + "\n"
                dialog_string += "\t" + str(character) + " \" " + dialog + " \" \n"
            elif last_character is "":
                dialog_string += "\t" + "show " + str(character) + "\n"
                dialog_string += "\t" + str(character) + " \" " + dialog + " \" \n"
            else:
                dialog_string += "\t" + str(character) + " \" " + dialog + " \" \n"
        return dialog_string

    def convert(self):
        converted_string = self.instantiate_characters()
        converted_string += "label start:\nscene bg room\n"
        converted_string += self.generate_dialogs()
        converted_string += "\t" + "return\n"
        return converted_string
