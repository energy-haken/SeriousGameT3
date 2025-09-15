from model_object.character_object import Character


class ObjToScriptConverter:


    list_characters = None
    dialogs_dict = None
    label_list = None

    def __init__(self):
        self.list_characters = []

    def set_characters_list(self, characters_list):
        self.remove_duplicates(characters_list)
    def set_label_list(self,label_list):
        self.label_list = label_list
    def remove_duplicates(self,dup_list):
        new_list = []
        known_characters = []
        for character in dup_list:
            if not character.get_name() in known_characters:
                known_characters.append(character.get_name())
                new_list.append(character)
        self.list_characters = new_list

    def instantiate_character(self,character : Character):
        return_string = "define " + (character.get_name().replace(" ", "_")).lower() + " = Character(\""+character.get_name()+"\")\n"
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
        choice_text += "            jump " + choice.get_jump() + "\n"
        return choice_text

    def generate_dialogs(self,dialogs_dict):
        dialog_string = ""
        last_character = Character("")
        last_expression = ""
        for character,dialog_list in dialogs_dict.items():
            dialog = dialog_list[0]
            expression = dialog_list[1]
            if (not last_character.get_name().__eq__(character.get_name())
                    and not last_character.get_name().__eq__("")):
                dialog_string += "    " + "hide " + str(last_character.get_character_image(last_expression)).lower() + "\n"
                dialog_string += "    " + "show " + str(character.get_character_image(expression)).lower() + "\n"
                dialog_string += "    " + str(character.get_name()).replace(" ", "_").lower() + " \" " + dialog + " \" \n"
                last_character = character
                last_expression = expression
            elif last_character.get_name() == "":
                dialog_string += "    " + "show " + str(character.get_character_image(expression)).lower() + "\n"
                dialog_string += "    " + str(character.get_name()).replace(" ", "_").lower() + " \" " + dialog + " \" \n"
                last_character = character
                last_expression = expression
            else:
                dialog_string += "    " + str(character.get_name()).replace(" ", "_").lower() + " \" " + dialog + " \" \n"
        return dialog_string

    def convert(self):
        converted_string = self.instantiate_characters()
        for label in self.label_list:
            if label.get_type() == "label": # A mere label
                converted_string += "label "+label.get_name()+":\n    scene "+label.get_background()+"\n"
                converted_string += self.generate_dialogs(label.get_dialogs_dict())
            elif label.get_type() == "label-end":
                converted_string += "label "+label.get_name()+":\n    scene "+label.get_background()+"\n"
                converted_string += self.generate_dialogs(label.get_dialogs_dict())
                converted_string += "    " + "return\n"
            else: # A menu with choices
                converted_string += self.generate_menu(label.get_menu())
        return converted_string
