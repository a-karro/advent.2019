POS = 0
IMM = 1
REL = 2
REG = 3

ADD = 1
MUL = 2
INP = 3
OUT = 4
JIT = 5
JIF = 6
LES = 7
EQU = 8
AREL = 9
HLT = 99

PAUSE_ON_OUTPUT = 1
RUN_TO_HALT = 2


def intcomputer(mem, pointer, input_values, rel=0, op_mode=RUN_TO_HALT, print_output=False):
    def op_addr(p_offset, mode):
        if mode == POS:
            mem.extend([0] * (mem[pointer + p_offset] - len(mem) + 1))
            return mem[pointer + p_offset]
        elif mode == REL:
            mem.extend([0] * (relative + mem[pointer + p_offset] - len(mem) + 1))
            return relative + mem[pointer + p_offset]
        else:
            return pointer + p_offset

    pointer = pointer
    last_output = None
    input_counter = 0
    relative = rel

    while mem[pointer] != 99:
        act = mem[pointer]
        opcode = act % 100
        if opcode not in [ADD, MUL, INP, OUT, JIT, JIF, LES, EQU, AREL, HLT]:
            raise ValueError("wrong opcode {} at position {}".format(act, pointer))
        m1 = act // 100 % 10
        m2 = act // 1000 % 10
        m3 = act // 10000 % 10

        addr1 = op_addr(1, m1)
        addr2 = addr3 = None
        if opcode not in [INP, OUT, AREL]:
            addr2 = op_addr(2, m2)

        if opcode in [ADD, MUL, LES, EQU]:
            addr3 = op_addr(3, m3)

        if opcode == INP:
            if len(input_values) == 0 or input_counter > len(input_values):
                raise ValueError("No more input values")
            mem[addr1] = input_values[input_counter]
            input_counter += 1
            pointer += 2
        elif opcode == OUT:
            last_output = mem[addr1]
            if print_output:
                print(mem[addr1])
            pointer += 2
            if op_mode == PAUSE_ON_OUTPUT:
                return last_output, pointer, relative
        elif opcode == ADD:
            mem[addr3] = mem[addr1] + mem[addr2]
            pointer += 4
        elif opcode == MUL:
            mem[addr3] = mem[addr1] * mem[addr2]
            pointer += 4
        elif opcode == JIT:
            if mem[addr1] != 0:
                pointer = mem[addr2]
            else:
                pointer += 3
        elif opcode == JIF:
            if mem[addr1] == 0:
                pointer = mem[addr2]
            else:
                pointer += 3
        elif opcode == LES:
            mem[addr3] = 1 if mem[addr1] < mem[addr2] else 0
            pointer += 4
        elif opcode == EQU:
            mem[addr3] = 1 if mem[addr1] == mem[addr2] else 0
            pointer += 4
        elif opcode == AREL:
            relative = relative + mem[addr1]
            pointer += 2
        else:
            raise ValueError("What is this magic?")

        if pointer > len(mem) - 1:
            raise ValueError("Pointer out of range")
    return last_output, -1, relative
