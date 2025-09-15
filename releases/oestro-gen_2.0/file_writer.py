import json
from typing import Dict

from model_object.background_object import BackgroundObject
from model_object.character_object import Character


class HomeMadeFileWriter:

    current_file = None
    mode = None

    def __init__(self):
        e = 0

    def set_file(self,file):
        self.current_file = file
    def set_mode(self,mode):
        match mode:
            case "w":
                self.mode = mode
            case "a":
                self.mode = mode
            case _:
                self.mode = "x"

    def write(self,text):
        if self.mode and self.current_file:
            f = open(self.current_file, self.mode)
            f.write(text)
            f.close()
    def read(self):
        f = open(self.current_file, "r")
        text = f.read()
        f.close()
        return text

    def load_json(self):
        """
        Json to Dict converter
        """
        json_file = self.read()
        return json.loads(json_file)
    def convert_dict_to_object(self,object_dict : Dict):
        """
        Dict to Object converter
        """
        new_object = None
        if object_dict.get("type").__eq__("Character"):
            new_object = Character(object_dict.get("name"))
            new_object.set_expressions(object_dict.get("expressions"))
        elif object_dict.get("type").__eq__("Background"):
            new_object = BackgroundObject(object_dict.get("name"))

        return new_object

    def dump_json(self, object_t):
        """
        Dict to Json converter
        """
        json_dict = {}
        if isinstance(object_t, Character):
            object_t: Character
            json_dict = {
                "type": "Character",
                "name": object_t.get_name(),
                "expression": list(object_t.get_expressions())  # Convert to list
            }
        elif isinstance(object_t, BackgroundObject):
            object_t: BackgroundObject
            json_dict = {
                "type": "Background",
                "name": object_t.get_name()
            }
        json_file = json.dumps(json_dict)
        return json_file
