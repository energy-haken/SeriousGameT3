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

    def write_character_and_output(self, character1, character2, output):
        if self.mode and self.current_file:
            with open(self.current_file, self.mode) as f:
                f.write(f"define {character1} = Character(\"{character1}\")\n")
                f.write(f"define {character2} = Character(\"{character2}\")\n")
                f.write("label start:\n")
                output = output.replace('"', ' ')
                lines = output.split('\n')
                characters = [character1, character2]
                
                for i, line in enumerate(lines):
                    current_character = characters[i % 2]
                    other_character = characters[(i + 1) % 2]
                    f.write(f"    show {current_character}\n")
                    f.write(f"    {current_character} \"{line}\"\n")
                    f.write(f"    hide {current_character}\n")
                    ##f.write(f"    hide {other_character}\n")