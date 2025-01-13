import re
import pprint

class Assembler:
    def __init__(self, input: str):
        self.input = input
        self.line_number = 0
        self.var_num = 16
        self.symbols = {
            # Predefined symbols
            "R0": 0,
            "R1": 1,
            "R2": 2,
            "R3": 3,
            "R4": 4,
            "R5": 5,
            "R6": 6,
            "R7": 7,
            "R8": 8,
            "R9": 9,
            "R10": 10,
            "R11": 11,
            "R12": 12,
            "R13": 13,
            "R14": 14,
            "R15": 15,
            "KBD": 24576,
            "SCREEN": 16384,
            "SP": 0,
            "LCL": 1,
            "ARG": 2,
            "THIS": 3,
            "THAT": 4,
        }

        self.compbits = {
            "0": "0101010",
            "1": "0111111",
            "-1": "0111010",
            "D": "0001100",
            "A": "0110000",
            "M": "1110000",
            "!D": "0001101",
            "!A": "0110001",
            "!M": "1110001",
            "-D": "0001111",
            "-A": "0110011",
            "-M": "1110011",
            "D+1": "0011111",
            "A+1": "0110111",
            "M+1": "1110111",
            "D-1": "0001110",
            "A-1": "0110010",
            "M-1": "1110010",
            "D+A": "0000010",
            "D+M": "1000010",
            "D-A": "0010011",
            "D-M": "1010011",
            "A-D": "0000111",
            "M-D": "1000111",
            "D&A": "0000000",
            "D&M": "1000000",
            "D|A": "0010101",
            "D|M": "1010101"
        }
        self.destbits = {
            "-1": "000",
            "M": "001",
            "D": "010",
            "MD": "011",
            "A": "100",
            "AM": "101",
            "AD": "110",
            "AMD": "111"
        }
        self.jumpbits = {
            "-1": "000",
            "JGT": "001",
            "JEQ": "010",
            "JGE": "011",
            "JLT": "100",
            "JNE": "101",
            "JLE": "110",
            "JMP": "111"
        }

        self.machine_code = []

    def assemble(self):
        self.fill_symbol_table()
        self.parse()

        output = "\n".join(self.machine_code)
        return output

    def parse(self):
        ipLines = self.input.splitlines()

        for ip in ipLines:
            ip = "".join(ip.split())
            comment_match = re.split("//", ip, 1)
            ip = comment_match[0]
            if len(ip) == 0:
                continue

            if ip[0] == '/':
                continue

            if ip[0] == "(":
                continue

            if ip[0] == "@":
                # parse A instruction
                self.parse_A_instr(ip)
                pass
            else:
                # parse C instruction
                self.parse_C_instr(ip)
                pass

            

    def parse_A_instr(self, ip):
        # regex = "@(\\w+)"
        # match = re.search(regex, ip)
        # if match is None:
        #     print(f"Error : no match found at {self.line_number} for instruction {ip}")
        #     return
        #
        # sym = match.group(1)
        sym = ip[1:]
        sym = sym.strip()
        if not sym.isnumeric():
            sym = self.symbols.get(sym)

        if sym is None:
            print(f"Error : Found none for symbol in {ip}")
            return

        symbin = "{0:b}".format(int(sym))

        a_instr = "0" + ((15 - len(str(symbin))) * "0") + str(symbin)
        # self.machine_code.append(ip + " " + a_instr)
        self.machine_code.append(a_instr)

    def parse_C_instr(self, ip):
        tip = ip
        jump = "-1"
        dest = "-1"

        jump_re = re.split(";", ip)
        if len(jump_re) == 2:
            jump = jump_re[1]
            ip = jump_re[0]

        dest_re = re.split("=", ip)
        if len(dest_re) == 2:
            dest = dest_re[0]
            ip = dest_re[1]

        comp = ip

        # c_instr = tip + " " +"111" + str(self.compbits.get(comp)) + str(self.destbits.get(dest)) + str(self.jumpbits.get(jump))
        c_instr = "111" + str(self.compbits.get(comp)) + str(self.destbits.get(dest)) + str(self.jumpbits.get(jump))
        self.machine_code.append((c_instr))


    def fill_symbol_table(self):
        ipLines = self.input.splitlines()

        # label symbols
        for ip in ipLines:
            ip = "".join(ip.split())
            if len(ip) == 0:
                continue

            if ip[0] == '/':
                continue

            if ip[0] == "(":
                # handle label symbol
                # regex = "\\((\\w+)\\)"
                # match = re.search(regex, ip)
                # if match is None:
                #     continue
                # sym = match.group(1)
                sym = ip[1:-1]
                self.symbols[sym] = self.line_number
                continue

            self.line_number += 1

        self.line_number = 0

        # variable symbols
        for ip in ipLines:
            ip = "".join(ip.split())
            if len(ip) == 0:
                continue

            if ip[0] == '/':
                continue

            if ip[0] == "(":
                continue

            if ip[0] == "@":
                # handle variable symbol if the next characters are symbols
                num_regex = "@(\\d+)"
                num_match = re.search(num_regex, ip)
                if num_match is not None:
                    self.line_number += 1
                    continue

                sym_regex = "@(\\w+\\.?\\w+)"
                sym_match = re.search(sym_regex, ip)
                if sym_match is None:
                    continue

                sym = sym_match.group(1)
                if sym not in self.symbols:
                    self.symbols[sym] = self.var_num
                    self.var_num += 1

            self.line_number += 1

        self.line_number = 0
        pprint.pprint(self.symbols)


