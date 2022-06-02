import argparse

from writer import Writer
from parser import Parser
from vm import Command        

def get_args():
    parser = argparse.ArgumentParser(description='Translate a Hack vm file into a Hack assembly file')
    parser.add_argument('input', help='the input file to be translated')
    return parser.parse_args()

def main():
    args = get_args()

    input_file = args.input
    output_file = input_file.replace('.vm', '.asm')
    
    parser = Parser(input_file)
    writer = Writer(output_file)

    while parser.has_more_commands():
        command = parser.get_command()
        command = Command.parse(command)

        writer.write_command(command)

if __name__ == "__main__":
    main()