label_counter = 0


def generate_label(prefix=""):
    global label_counter
    label_counter += 1

    return f"{prefix}${label_counter}"


class Instruction:
    def asm(self) -> list[str]:
        raise NotImplementedError()


class Push(Instruction):
    def __init__(self, segment, index):
        self.segment = segment
        self.index = index

    def _getValue(self):
        match self.segment:
            case "argument":
                return ["@ARG", "D=M", f"@{self.index}", "A=D+A", "D=M"]
            case "local":
                return ["@LCL", "D=M", f"@{self.index}", "A=D+A", "D=M"]
            case "static":
                return [f"@PROGRAM_NAME.{self.index}", "D=M"]
            case "constant":
                return [f"@{self.index}", "D=A"]
            case "this":
                return ["@THIS", "D=M", f"@{self.index}", "A=D+A", "D=M"]
            case "that":
                return ["@THAT", "D=M", f"@{self.index}", "A=D+A", "D=M"]
            case "pointer":
                if self.index == "0":
                    return ["@THIS", "D=M"]
                elif self.index == "1":
                    return ["@THAT", "D=M"]
                else:
                    raise Exception("Invalid pointer index", self.index)
            case "temp":
                return [f"@{5 + int(self.index)}", "D=M"]
            case _:
                raise Exception("Invalid segment", self.segment)

    def asm(self):
        return [*self._getValue(), "@SP", "A=M", "M=D", "@SP", "M=M+1"]

    def __str__(self):
        return f"push {self.segment} {self.index}"


class Pop(Instruction):
    def __init__(self, segment, index):
        self.segment = segment
        self.index = index

    def _getAddress(self):
        match self.segment:
            case "argument":
                return ["@ARG", "D=M", f"@{self.index}", "D=D+A"]
            case "local":
                return ["@LCL", "D=M", f"@{self.index}", "D=D+A"]
            case "static":
                return [f"@PROGRAM_NAME.{self.index}", "D=A"]
            case "this":
                return ["@THIS", "D=M", f"@{self.index}", "D=D+A"]
            case "that":
                return ["@THAT", "D=M", f"@{self.index}", "D=D+A"]
            case "pointer":
                if self.index == "0":
                    return ["@THIS", "D=A"]
                elif self.index == "1":
                    return ["@THAT", "D=A"]
                else:
                    raise Exception("Invalid pointer index", self.index)
            case "temp":
                return [f"@{5 + int(self.index)}", "D=A"]
            case _:
                raise Exception("Invalid segment", self.segment)

    def asm(self):
        return [*self._getAddress(), "@R13", "M=D", "@SP", "AM=M-1", "D=M", "@R13", "A=M", "M=D"]

    def __str__(self):
        return f"pop {self.segment} {self.index}"


# ======================== Binary Ops ========================

class BinaryOperation(Instruction):
    def __init__(self, operation):
        self.operation = operation

    def asm(self):
        return ["@SP", "AM=M-1", "D=M", "@SP", "AM=M-1", f"M=M{self.operation}D", "@SP", "M=M+1"]


class Add(BinaryOperation):
    def __init__(self):
        super().__init__("+")

    def __str__(self):
        return "add"


class Sub(BinaryOperation):
    def __init__(self):
        super().__init__("-")

    def __str__(self):
        return "sub"


class And(BinaryOperation):
    def __init__(self):
        super().__init__("&")

    def __str__(self):
        return "and"


class Or(BinaryOperation):
    def __init__(self):
        super().__init__("|")

    def __str__(self):
        return "or"


# ======================== Unary Ops ========================

class UnaryOperation(Instruction):
    def __init__(self, operation):
        self.operation = operation

    def asm(self):
        return ["@SP", "A=M-1", f"M={self.operation}M"]


class Neg(UnaryOperation):
    def __init__(self):
        super().__init__("-")

    def __str__(self):
        return "neg"


class Not(UnaryOperation):
    def __init__(self):
        super().__init__("!")

    def __str__(self):
        return "not"


# ======================== Comparison Ops ========================

class Comparison(Instruction):
    def __init__(self, operation):
        self.operation = operation

    def asm(self):
        true_label = generate_label("TRUE")
        end_label = generate_label("END")

        return ["@SP", "AM=M-1", "D=M", "@SP", "AM=M-1", "D=M-D", f"@{true_label}", f"D;J{self.operation}", "D=0", f"@{end_label}", "0;JMP", f"({true_label})", "D=-1", f"({end_label})", "@SP", "A=M", "M=D", "@SP", "M=M+1"]


class Eq(Comparison):
    def __init__(self):
        super().__init__("EQ")

    def __str__(self):
        return "eq"


class Lt(Comparison):
    def __init__(self):
        super().__init__("LT")

    def __str__(self):
        return "lt"


class Gt(Comparison):
    def __init__(self):
        super().__init__("GT")

    def __str__(self):
        return "gt"
