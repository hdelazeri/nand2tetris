from enum import Enum


class Segments(Enum):
    ARG = 'ARG'
    LOCAL = 'LCL'
    STATIC = 'static'
    THIS = 'THIS'
    THAT = 'THAT'
    POINTER = 'pointer'
    TEMP = 'temp'
    CONSTANT = 'constant'

    def parse(string):
        if string == 'argument':
            return Segments.ARG
        elif string == 'local':
            return Segments.LOCAL
        elif string == 'static':
            return Segments.STATIC
        elif string == 'this':
            return Segments.THIS
        elif string == 'that':
            return Segments.THAT
        elif string == 'pointer':
            return Segments.POINTER
        elif string == 'temp':
            return Segments.TEMP
        elif string == 'constant':
            return Segments.CONSTANT
        else:
            raise Exception('Invalid segment')

    def __str__(self):
        return self.value

class Command(Enum):
    C_ARITHMETIC = 0
    C_PUSH = 1
    C_POP = 2
    C_LABEL = 3
    C_GOTO = 4
    C_IF = 5
    C_FUNCTION = 6
    C_RETURN = 7
    C_CALL = 8

    @staticmethod
    def parse(string):
        parts = string.split(' ')

        if len(parts) == 1:
            if parts[0] in ['add', 'sub', 'neg', 'and', 'or', 'not', 'eq', 'gt', 'lt']:
                return (Command.C_ARITHMETIC, parts[0], None)
        
        if len(parts) == 3:
            if parts[0] in ['push']:
                return (Command.C_PUSH, Segments.parse(parts[1]), parts[2])
            elif parts[0] in ['pop']:
                return (Command.C_POP, Segments.parse(parts[1]), parts[2])

        raise Exception('Invalid command')  