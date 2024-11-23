
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