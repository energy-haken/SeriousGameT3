import typing


class Character:
    __name : str = None
    # The keys are the expressions, the values are the images' name used
    __expressions : typing.Dict[str,str] = None
    # Key of the currently used expression

    def __init__(self,name : str):
        self.__name = name
        self.__expressions = {"":name} # in case there's no expression to avoid crash
    def set_expressions(self, expressions):
        self.__expressions = expressions
    def add_expression(self,expression : str):
        self.__expressions[expression] = self.__name + " "+ expression
    def get_character_image(self,expression):
        return self.__expressions[expression]
    def get_name(self):
        return self.__name
    def get_expression(self,expression):
        return self.__expressions[expression]
    def get_expressions(self):
        return self.__expressions.keys()