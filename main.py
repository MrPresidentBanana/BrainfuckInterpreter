
# * interpreter for brainfuck implemented in python (I know it's ridiculous, but it's just for fun)
# * takes code from the command line for now, file system possibly later

from enum import Enum
from enum import auto


tape_length: int = 30_000

code: str = input("Please input you Brainfuck Source Code: \n") # the code to be interpreted
tape = [0] * tape_length # "memory tape" like in a turing machine
pointer: int = 0 # position of the read-write-head on the tape

program_counter = 0

loop_stack = [] # stack to track which ] belongs to which [


while program_counter < len(code):

    instruction = code[program_counter]


    # executes current instruction
    match instruction:

        # moving on tape
        case ">":
            if program_counter < tape_length:
                pointer += 1
            else:
                print(f"ERROR at instruction {program_counter+1}: pointer can't go past end of tape")

        case "<":
            if program_counter >= 0:
                pointer -= 1
            else:
                print(f"ERROR at instruction {program_counter+1}: pointer can't go behind beginning of tape")
        

        # inc/dec numbers
        case "+":
            if tape[pointer] >= 255: # implementation of overflow
                tape[pointer] = 0
            else:   
                tape[pointer] += 1

        case "-":
            if tape[pointer] <= 0: # imlementation of overflow
                tape[pointer] = 255
            else:
                tape[pointer] -= 1


        #input/output
        case ".":
            val = tape[pointer]
            if val >= 0 and val <= 255:
                print(chr(val), end="")
            else:
                print(f"ERROR at instruction {program_counter+1}: value at current position can't be converted to char")

        case ",":
            given_input = input()
            tape[pointer] = ord(given_input[0]) # if input longer than 1 character, only take first character


        # loops
        case "[":
            loop_stack.append(program_counter)

        case "]":
            if tape[pointer] == 0:
                loop_stack.pop() # removes reference to completed loop from loop_stack
            else:
                program_counter = loop_stack.pop()-1 # sets program counter back to beginning of this loop; -1 neccessary to counter prog_counter inc below

    
    program_counter += 1