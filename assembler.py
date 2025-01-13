import re

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
        self.machine_code = []

    def assemble(self):
        self.fill_symbol_table()
        self.parse()

        output = "\n".join(self.machine_code)
        print(output)
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
        regex = "@(\\w+)"
        match = re.search(regex, ip)
        if match is None:
            print(f"Error : no match found at {self.line_number} for instruction {ip}")
            return

        sym = match.group(1)
        if not sym.isnumeric():
            sym = self.symbols.get(sym)
        print(f"Found {sym} for instruction {ip}")

        symbin = "{0:b}".format(int(sym))

        print("0" + ((15 - len(str(symbin))) * "0") + str(symbin))

    def parse_C_instr(self, ip):
        pass

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
                regex = "\\((\\w+)\\)"
                match = re.search(regex, ip)
                if match is None:
                    continue
                sym = match.group(1)
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

                sym_regex = "@(\\w+)"
                sym_match = re.search(sym_regex, ip)
                if sym_match is None:
                    continue

                sym = sym_match.group(1)
                if sym not in self.symbols:
                    self.symbols[sym] = self.var_num
                    self.var_num += 1

            self.line_number += 1

        self.line_number = 0


