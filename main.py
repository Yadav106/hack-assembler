from assembler import Assembler

def main():
    with open("code.asm", "r") as f:
        code = f.read()

    assembler = Assembler(input=code)
    assembler.assemble()

main()
