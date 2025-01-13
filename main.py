from assembler import Assembler

def main():
    name = input("Enter name of your file : ")
    with open(f"{name}.asm", "r") as f:
        code = f.read()

    assembler = Assembler(input=code)
    output = assembler.assemble()
    with open(f"{name}.hack", "w") as f:
        f.write(output)

main()
