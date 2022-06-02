class Parser:
    def __init__(self, input_file) -> None:
        self.command_type = None
        self.arg1 = None
        self.arg2 = None

        file = open(input_file, 'r')
        self.lines = file.readlines()

        self.lines = [line.strip() for line in self.lines]
        self.lines = filter(lambda line: line != '', self.lines)
        self.lines = filter(lambda line: not line.startswith('//'), self.lines)
        self.lines = list(self.lines)

        self.read_position = 0

    def has_more_commands(self) -> bool:
        return self.read_position < len(self.lines)

    def get_command(self):
        self.read_position += 1
        return self.lines[self.read_position - 1]