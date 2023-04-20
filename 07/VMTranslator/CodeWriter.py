from os import path

from Instructions import Instruction


class CodeWriter:
    def __init__(self, filename):
        self.file = open(filename.replace(".vm", ".asm"), "w")

    def __del__(self):
        self.file.close()

    def write(self, instruction: Instruction):
        self.file.write(f"// {instruction} \n")
        for line in instruction.asm():
            line = line.replace("PROGRAM_NAME", path.basename(
                self.file.name).replace(".asm", ""))

            self.file.write(line + "\n")
