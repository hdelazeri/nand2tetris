from Instructions import Push, Pop, Add, Sub, Eq, Lt, Gt, Neg, And, Or, Not


class Parser:
    def __init__(self, filename):
        self.filename = filename

    def instructions(self):
        with open(self.filename) as file:
            for line in file:
                line = line.strip()
                if line.startswith("//") or line == "":
                    continue

                match line.split():
                    case ["push", segment, index]:
                        yield Push(segment, index)
                    case ["pop", segment, index]:
                        yield Pop(segment, index)
                    case ["add"]:
                        yield Add()
                    case ["sub"]:
                        yield Sub()
                    case ["and"]:
                        yield And()
                    case ["or"]:
                        yield Or()
                    case ["neg"]:
                        yield Neg()
                    case ["not"]:
                        yield Not()
                    case ["eq"]:
                        yield Eq()
                    case ["lt"]:
                        yield Lt()
                    case ["gt"]:
                        yield Gt()
                    case _:
                        raise Exception("Invalid instruction", line)
