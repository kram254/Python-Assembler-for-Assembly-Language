# Python-Assembler-for-Assembly-Language
This assembler is a Python program that translates Assembly Language instructions from a provided input file into binary format. It supports various instruction types, including R, Ri, M, Mi, and B-type instructions. The resulting binary output is saved to a specified output file, ready for execution by the target machine.


# Custom Assembly Language Assembler
This Python program serves as an assembler for a custom assembly language. It takes an input file containing assembly instructions and converts them into a binary format that can be executed by the target machine. The assembler supports various instruction types, including R, Ri, M, Mi, and B-type instructions.

## Requirements
Python 3.x
No external packages are required.
Usage
To use the assembler, simply run the following command in your terminal:

```
python assembler.py <input_file> <output_file>
```

Replace `<input_file>` with the path to your assembly code file and `<output_file>` with the path where you'd like the binary output to be saved.

How it works
The assembler reads the input file line by line and processes the assembly instructions. It translates each instruction into its corresponding binary representation and writes the output to the specified output file.

Sets and dictionaries
The assembler uses sets and dictionaries to map instruction mnemonics to their binary representations, and register names to their binary representations. For example:

```
R_set = set(["ADD", "SUB", "LB", "SB", "BNE", "NOR", "XOR", "AND", "OR", "SLL", "SLR", "EQ", "LT", "RXOR"])
op_map = {
    "ADD": "00000",
    "SUB": "00001",
    "LB": "00011",
    ...
}
reg_map_R = {
    "$0": "00",
    "$1": "01",
    "$2": "10",
    "$3": "11",
    ...
}
```
Parsing functions
The assembler utilizes parsing functions to process different types of instructions:
```
parse_R: Parses R-type instructions (e.g., ADD, SUB, LB, SB, BNE, NOR, XOR, AND, OR, SLL, SLR, EQ, LT, and RXOR).
parse_Ri: Parses Ri-type instructions (e.g., ADDI).
parse_M: Parses M-type instructions (e.g., MOVR).
parse_Mi: Parses Mi-type instructions (e.g., MOVI).
parse_B: Parses B-type instructions (e.g., BT).
These functions take a line of assembly code and the instruction type as input, and return the corresponding binary representation of the instruction.
```
Main function
The main function handles reading the input file, processing the assembly instructions, and writing the binary output to the output file. It skips comments, labels, directives, and syscalls in the input file, and processes the remaining assembly instructions. For each instruction, the main function identifies its type and calls the appropriate parsing function to convert it to binary. Finally, the binary instruction is written to the output file.



