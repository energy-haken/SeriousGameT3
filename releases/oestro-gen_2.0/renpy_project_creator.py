import os
import platform
import subprocess
import glob

def launch_renpy():
    os_name = platform.system()

    if os_name == "Linux":
        renpy_path = subprocess.run("find ~ -name renpy.sh", shell=True, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
        renpy_path = renpy_path.stdout.decode("utf-8")
        assert renpy_path != ""
        os.chdir(os.path.dirname(renpy_path))
        subprocess.run("./renpy.sh")
    if os_name == "Windows":
        renpy_path = glob.glob("C:/**/renpy.exe",recursive=True)
        if not renpy_path:
            glob.glob("D:/**/renpy.exe",recursive=True)
        print(renpy_path)
        assert renpy_path != ""
        #print("Path : "+renpy_path)
        #os.chdir(os.path.dirname(renpy_path))
        #subprocess.run("start renpy.exe")


class RenpyProjectCreator:
    __name = "Renpy Project Creator"
    __resolutiion = "1280x720"
    __color = "pink"

    def __init__(self, name : str, resolution : str, color : str):
        self.__name = name
        self.__resolution = resolution
        self.__color = color

    def create_project(self):
        base_path = "resources/renpy_project/"
        # Create the directory of the project
        if not os.path.exists(base_path+self.__name):
            os.mkdir(base_path+self.__name)

        # Create the directory game of the project
        game_path = base_path+self.__name
        if not os.path.exists(base_path+self.__name+"/game"):
            os.mkdir(base_path+self.__name+"/game")
            game_path = base_path+self.__name+"/game"

            # Créer script.rpy
            with open(os.path.join(game_path, "script.rpy"), "w", encoding="utf-8") as f:
                f.write('label start:\n    "Bonjour, monde!"\n    return\n')

            # Créer options.rpy
            with open(os.path.join(game_path, "options.rpy"), "w", encoding="utf-8") as f:
                f.write(f'''define config.window_title = "{self.__name}"\ndefine gui.init_resolution = ({self.__resolution.split("x")[0]}, {self.__resolution.split("x")[1]})''')

            # Créer gui.rpy avec couleurs simples
            couleur_text = {
                "light": "define gui.text_color = '#000000'\n",
                "dark": "define gui.text_color = '#FFFFFF'\n"
            }
            with open(os.path.join(game_path, "gui.rpy"), "w", encoding="utf-8") as f:
                f.write(couleur_text.get(self.__color, couleur_text["light"]))

            print(f"Projet '{self.__name}' créé avec succès à : {base_path}")

