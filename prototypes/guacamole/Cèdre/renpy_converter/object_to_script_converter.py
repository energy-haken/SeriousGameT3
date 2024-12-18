

class ObjToScriptConverter:


    list_characters = None
    dialogs_dict = None
    label_list = None

    def __init__(self):
        self.list_characters = []

    def set_characters_list(self, characters_list):
        self.list_characters = self.remove_duplicates(characters_list)
    def set_label_list(self,label_list):
        self.label_list = label_list
    def remove_duplicates(self,dup_list):
        return list(dict.fromkeys(dup_list)) # remove duplicated elements

    def instantiate_character(self,character):
        return_string = "define " + (character.replace(" ", "_")).lower() + " = Character(\""+character+"\")\n"
        return return_string

    def instantiate_characters(self):
        character_instantiation = ""
        for character in self.list_characters:
            character_instantiation += self.instantiate_character(character)
        return character_instantiation

    #TODO : class menu and choice
    def generate_menu(self,menu):
        menu_text = "    menu:\n"
        menu_text += "        " +"\""+ menu.get_title()+"\"\n"

        for choice in menu.get_choice_list():
            menu_text += self.generate_choice(choice)

        return menu_text
    # uses : "    " instead of "\t" because RenPy doesn't accept tab! What a chicanery!
    def generate_choice(self,choice):
        choice_text = "        \"" + choice.get_title() + "\":\n"
        choice_text += "            \"" + choice.get_text() + "\"\n"
        choice_text += "            \"" + choice.get_jump() + "\"\n"
        return choice_text

    # character.split("*", 1)[0] allow to get rid of the dialog identifier ie : my_character*12
    def generate_dialogs(self,dialogs_dict):
        dialog_string = ""
        last_character = ""
        for character,dialog in dialogs_dict.items():
            if (not last_character.__eq__(character.split("*", 1)[0])
                    and not last_character.__eq__("")):
                dialog_string += "    " + "hide " + str(last_character.split("*", 1)[0]) + "\n"
                dialog_string += "    " + "show " + str(character.split("*", 1)[0]) + "\n"
                dialog_string += "    " + str(character.split("*", 1)[0]).replace(" ", "_").lower() + " \" " + dialog + " \" \n"
                last_character = str(character.split("*", 1)[0])
            elif last_character == "":
                dialog_string += "    " + "show " + str(character.split("*", 1)[0]) + "\n"
                dialog_string += "    " + str(character.split("*", 1)[0]).replace(" ", "_").lower() + " \" " + dialog + " \" \n"
                last_character = str(character.split("*", 1)[0])
            else:
                dialog_string += "    " + str(character.split("*", 1)[0]).replace(" ", "_").lower() + " \" " + dialog + " \" \n"
        return dialog_string

    def convert(self):
        converted_string = self.instantiate_characters()
        for label in self.label_list:
            if label.get_type() == "label": # A mere label
                converted_string += "label "+label.get_name()+":\n    scene "+label.get_background()+"\n"
                converted_string += self.generate_dialogs(label.get_dialogs_dict())
                converted_string += "    " + "return\n"
            else: # A menu with choices
                converted_string += self.generate_menu(label.get_menu())
        return converted_string
