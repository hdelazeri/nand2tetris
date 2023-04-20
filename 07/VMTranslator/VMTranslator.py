import argparse

from Parser import Parser
from CodeWriter import CodeWriter


def main():
    arguments = argparse.ArgumentParser()
    arguments.add_argument("file", help="The file to translate")
    args = arguments.parse_args()

    parser = Parser(args.file)
    writer = CodeWriter(args.file)

    for instruction in parser.instructions():
        writer.write(instruction)


if __name__ == "__main__":
    main()
