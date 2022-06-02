from pathlib import Path

from vm import Command, Segments

class Writer:
    def __init__(self, output_file) -> None:
        self.output_file = open(output_file, 'w')
        self.name = Path(output_file).stem
        self.label_count = 0

    def write_command(self, command):
        if command[0] == Command.C_ARITHMETIC:
            self.write_arithmetic(command[1])
        elif command[0] == Command.C_PUSH:
            self.write_push(command[1], command[2])
        elif command[0] == Command.C_POP:
            self.write_pop(command[1], command[2])

    def write_push(self, segment, index):
        print(f'// push {segment} {index}', file=self.output_file)

        if segment == Segments.CONSTANT:
            print(f'@{index}', file=self.output_file)
            print('D=A', file=self.output_file)

        if segment == Segments.STATIC:
            print(f'@{self.name}.{index}', file=self.output_file)
            print('D=M', file=self.output_file)

        if segment == Segments.TEMP:
            print(f'@{5 + int(index)}', file=self.output_file)
            print('D=M', file=self.output_file)

        if segment == Segments.POINTER:
            print(f'@{3 + int(index)}', file=self.output_file)
            print('D=M', file=self.output_file)

        if segment in [Segments.ARG, Segments.LOCAL, Segments.THIS, Segments.THAT]:
            print(f'@{index}', file=self.output_file)
            print('D=A', file=self.output_file)
            print(f'@{segment}', file=self.output_file)
            print('A=D+M', file=self.output_file)
            print('D=M', file=self.output_file)
        
        self._push_from_reg('D')

        print('', file=self.output_file)

    def write_pop(self, segment, index):
        print(f'// pop {segment} {index}', file=self.output_file)

        if segment == Segments.CONSTANT:
            raise Exception('Cannot pop to constant')

        if segment == Segments.STATIC:
            print(f'@{self.name}.{index}', file=self.output_file)
            print('D=A', file=self.output_file)

        if segment == Segments.TEMP:
            print(f'@{5 + int(index)}', file=self.output_file)
            print('D=A', file=self.output_file)

        if segment == Segments.POINTER:
            print(f'@{3 + int(index)}', file=self.output_file)
            print('D=A', file=self.output_file)

        if segment in [Segments.ARG, Segments.LOCAL, Segments.THIS, Segments.THAT]:
            print(f'@{index}', file=self.output_file)
            print('D=A', file=self.output_file)
            print(f'@{segment}', file=self.output_file)
            print('D=D+M', file=self.output_file)

        # Store temp value
        print('@R13', file=self.output_file)
        print('M=D', file=self.output_file)
        
        self._pop_to_reg('D')
        
        # write value to pop destination
        print('@R13', file=self.output_file)
        print('A=M', file=self.output_file)
        print('M=D', file=self.output_file)

        print('', file=self.output_file)
    
    def write_arithmetic(self, command):
        print(f'// {command}', file=self.output_file)

        if command == 'add': self._binary_op('M+D')
        if command == 'sub': self._binary_op('M-D')
        if command == 'and': self._binary_op('M&D')
        if command == 'or':  self._binary_op('M|D')
        if command == 'neg': self._unary_op('-M')
        if command == 'not': self._unary_op('!M')
        if command == 'eq':  self._compare('JEQ')
        if command == 'gt':  self._compare('JGT')
        if command == 'lt':  self._compare('JLT')

        print('', file=self.output_file)

    def _dec_SP(self):
        print('@SP', file=self.output_file)
        print('M=M-1', file=self.output_file)
    
    def _inc_SP(self):
        print('@SP', file=self.output_file)
        print('M=M+1', file=self.output_file)

    def _pop_to_reg(self, destination):
        self._dec_SP()

        print('@SP', file=self.output_file)
        print('A=M', file=self.output_file)

        print(f'{destination}=M', file=self.output_file)

    def _push_from_reg(self, source):
        print('@SP', file=self.output_file)
        print('A=M', file=self.output_file)

        print(f'M={source}', file=self.output_file)

        self._inc_SP()

    def _unary_op(self, operation):
        self._pop_to_reg('M')

        print(f'D={operation}', file=self.output_file)

        self._push_from_reg('D')

    def _binary_op(self, operation):
        self._pop_to_reg('D')
        self._pop_to_reg('M')

        print(f'D={operation}', file=self.output_file)

        self._push_from_reg('D')

    def _jump(self, value, operation):
        label = f'{self.name}_{self.label_count}'
        self.label_count += 1

        print(f'@{label}', file=self.output_file)
        print(f'{value};{operation}', file=self.output_file)

        return label

    def _compare(self, operation):
        self._pop_to_reg('D')
        self._pop_to_reg('M')

        print(f'D=M-D', file=self.output_file)

        true_label = self._jump('D', operation)
        self._push_from_reg('0')

        false_label = self._jump('0', 'JMP')
        
        print(f'({true_label})', file=self.output_file)
        self._push_from_reg('-1')
        
        print(f'({false_label})', file=self.output_file)

        self.label_count += 1
        