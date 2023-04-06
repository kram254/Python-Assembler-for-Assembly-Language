import sys
import re

R_set = set(["ADD", "SUB", "LB", "SB", "BNE", "NOR", "XOR", "AND", "OR", "SLL", "SLR", "EQ", "LT", "RXOR"])
Ri_set = set(["ADDI"])
M_set = set(["MOVR"])
Mi_set = set(["MOVI"])
B_set = set(["BT"])

B_map = {"LOAD_MESSAGE": "0000"}

op_map = {
    "ADD": "00000",
    "SUB": "00001",
    "LB": "00011",
    "SB": "00100",
    "BEQ": "00101",
    "BT": "00101",
    "BNE": "00101",
    "NOR": "00111",
    "XOR": "01000",
    "AND": "01001",
    "OR": "01010",
    "SLL": "01011",
    "SLR": "01100",
    "EQ": "01101",
    "LT": "01110",
    "RXOR": "01111",
    "ADDI": "00010",
    "MOVR": "10",
    "MOVI": "11",
}

reg_map_R = {
    "$0": "00",
    "$1": "01",
    "$2": "10",
    "$3": "11",
    "$4": "00",
    "$5": "01",
    "$6": "10",
    "$7": "11",
    "$t0": "00",
    "$t1": "01",
    "$t2": "10",
    "$t3": "11",
    "$t4": "00",
    "$t5": "01",
    "$t6": "10",
    "$t7": "11",
    "$a0": "00",
    "$a1": "01",
    "$a2": "10",
    "$a3": "11",
}

reg_map_Ri = {
    "0": "00",
    "1": "01",
    "-2": "10",
    "-1": "11",
}
reg_map_M = {
    "0": "000",
    "1": "001",
    "2": "010",
    "3": "011",
    "4": "100",
    "5": "101",
    "6": "110",
    "7": "111",
}
reg_map_Mi = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "-8": "1000",
    "-7": "1001",
    "-6": "1010",
    "-5": "1011",
    "-4": "1100",
    "-3": "1101",
    "-2": "1110",
    "-1": "1111",
}

def parse_R(line, inst_type):
    pattern = r"\s+"
    line = re.sub(pattern, "", line)

    aluop = op_map[inst_type]
    
    if inst_type == "BNE":
        operands = line.split(",", 1)
        operand1 = reg_map_R[operands[0].strip()]
        operand2 = reg_map_R[operands[1].strip()]
        offset = bin(int(operands[2].strip()))[2:].zfill(8)  # convert offset to binary and pad with zeroes
        final_instruction = aluop + operand1 + operand2 + offset + "\n"
    elif inst_type in ["SLL", "SLR"]:
        operands = line.split(",", 1)
        operand1 = reg_map_R[operands[0].strip()]
        operand2 = reg_map_R[operands[1].strip()]
        final_instruction = aluop + operand1 + operand2 + "\n"
    else:
        operands = line.split(",", 2)
        operand1 = reg_map_R[operands[0].strip()]
        operand2 = reg_map_R[operands[1].strip()]
        operand3 = reg_map_R[operands[2].strip()]
        final_instruction = aluop + operand1 + operand2 + operand3 + "\n"
    
    return final_instruction


# def parse_R(line, inst_type):
#     pattern = r"\s+"
#     line = re.sub(pattern, "", line)

#     aluop = op_map[inst_type]
#     operands = line.split(",", 1)
#     operand1 = reg_map_R[operands[0].strip()]
#     operand2 = reg_map_R[operands[1].strip()]
#     final_instruction = aluop + operand1 + operand2 + "\n"
#     return final_instruction

def parse_Ri(line, insttype):
    # Regex for removing spaces
    pattern = r"\s+"
    operands = re.sub(pattern, "", line)

    aluop = op_map[insttype]
    operands = operands.split(",#")
    operand1 = reg_map_R[operands[0]]
    operand2 = reg_map_Ri[operands[1]]
    final_instruction = aluop + operand1 + operand2 + "\n"
    return final_instruction

def parse_M(line, insttype):
    # Regex for removing spaces
    pattern = r"\s+"
    operands = re.sub(pattern, "", line)

    aluop = op_map[insttype]
    operands = operands.split(",$")
    operand1 = reg_map_M[operands[0]]
    operand2 = reg_map_M[operands[1]]
    final_instruction = aluop + operand1 + operand2 + "0" + "\n"
    return final_instruction

def parse_Mi(line, insttype):
    # Regex for removing spaces
    pattern = r"\s+"
    operands = re.sub(pattern, "", line)

    aluop = op_map[insttype]
    operands = operands.split(",#")
    operand1 = reg_map_M[operands[0]]
    operand2 = reg_map_Mi[operands[1]]
    final_instruction = aluop + operand1 + operand2 + "\n"
    return final_instruction

def parse_B(line, insttype):
    # Regex for removing spaces
    pattern = r"\s+"
    operands = re.sub(pattern, "", line)

    aluop = op_map[insttype]
    operand1 = B_map[operands]
    final_instruction = aluop + operand1 + "\n"
    return final_instruction


def main(input_file, output_file):
    try:
        with open(input_file, "r") as inputf:
            with open(output_file, "w") as outputf:
                content = inputf.readlines()
                for line in content:
                    # Remove whitespace, labels, comments
                    if line.isspace() or ":" in line:
                        continue
                    if ";" in line:
                        line = line.split(";")[0]
                        if line.isspace():
                            continue
                    line = line.strip()

                    # instructions
                    if line:
                        # Check if the line is a directive or a syscall
                        if line.startswith('.') or line.lower() == "syscall" or line.lower() == "jr $ra":
                            continue

                        # Check if there is a space in the line
                        if " " in line:
                            # Split the instruction type and the operands
                            inst_type, operands = line.split(" ", 1)
                            inst_type = inst_type.upper().strip()

                            if inst_type in B_set:
                                final_instruction = parse_B(operands, inst_type)
                            elif inst_type in R_set:
                                final_instruction = parse_R(operands, inst_type)
                            elif inst_type in M_set:
                                final_instruction = parse_M(operands, inst_type)
                            elif inst_type in Ri_set:
                                final_instruction = parse_Ri(operands, inst_type)
                            elif inst_type in Mi_set:
                                final_instruction = parse_Mi(operands, inst_type)
                            else:
                                continue
                            outputf.write(final_instruction)
                        else:
                            print(f"Invalid line: {line}")

    except Exception as e:
        print(f"Error occurred while processing the input file: {e}")

    finally:
        inputf.close()
        outputf.close()


if __name__ == "__main__":
    # Command line arguments are formatted incorrectly
    if len(sys.argv) != 3:
        print("Usage: python assembler.py <input_file> <output_file>")
        sys.exit(1)

    # Input and output command line argument received
    else:
        input_file, output_file = sys.argv[1], sys.argv[2]
        main(input_file, output_file)