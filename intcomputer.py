import copy

REGISTERS = 5

POS = 0
IMM = 1
REL = 2

# hypothetical access to registers
REG_IMM = None  # - immediate, sets/returns value of a register #N (N - memory[point+x])
REG_ADR = None  # - address, sets/returns value of a register #N (N - memory[memory[point+x])
REG_REL = None  # - relative, sets/returns value of a register #N (# - memory[relative + memory[point+x]])


RET = None  # hypothetical return from subroutine

ADD = 1  # 1,2 - operands, 3 - result
MUL = 2  # 1,2 - operands, 3 - result
INP = 3  # 1 - dest for input value
OUT = 4  # 1 - source for output value
JIT = 5  # 1 - operand, 2 - dest
JIF = 6  # 1 - operand, 2 dest
LES = 7  # 1,2 - operands, 3 - result [0/1]
EQU = 8  # 1,2 - operands, 3 - result [0/1]
AREL = 9  # 1 - adjustment for relative
HLT = 99  # HAMMERZEIT!

# hypothetical actions
JMP = None  # 1 param, dest
JZ = None   # 1 param, 2 - dest
JNZ = None  # 1 param, 2 - dest
JLE = None  # 1, 2 - operands, 3 -dest
JL = None   # jump if less; 1, 2 - operands, 3 - dest
JGE = None  # jump if greater or equal: 1,2 - operands, 3 -dest
JG = None   # jump if greater, 1,2 - operands, 3 - dest
AND = None  # bitwise AND, 1,2 - operands, 3 - result
OR = None   # bitwise OR, 1,2 - operands, 3 - result
NOT = None  # bitwise NOT, 1 - operand, 2 - result
XOR = None  # bitwise XOR, 1,2 - operands, 3 - result
SHL = None  # SHL, 1 - operand, 2 - offset, 3 - result
SHR = None  # SHL, 1 - operand, 2 - offset, 3 - result
PROC = None  # procedure, 1 - entry address


PAUSE_ON_OUTPUT = 1
RUN_TO_HALT = 2

OPCODES = [RET, ADD, MUL, INP, OUT, JIT, JIF, LES, EQU, AREL, HLT, JMP, JZ, JNZ, JLE, JL, JGE, JG, AND, OR, NOT,
           XOR, SHL, SHR]
OPCODES_ZERO = [RET]
OPCODES_ONE = [INP, OUT, AREL, PROC]
OPCODES_TWO = [JIT, JIF, NOT, JZ, JNZ]
OPCODES_THREE = [ADD, MUL, LES, EQU, JLE, JL, JGE, JG, AND, OR, XOR, SHL, SHR]


class IntComputer:
    def __init__(self, memory, run_mode=RUN_TO_HALT):
        # registers are placed at the beginning of the memory
        # [reg0][reg1][reg2]..[regN-1][mem0][mem1]..[memN-1]
        # when accessing the memory, pointer needs to have + len(registers)
        # when accessing registers, the offset doesn't need to be added

        self.registers = [0] * 10
        self.RL = len(self.registers)
        self.pointer = 0
        self.memory = self.registers + copy.deepcopy(memory)
        self.relative = 0
        self.outputs = []
        self.inputs = []
        self.run_mode = run_mode
        self.stack = []
        self.cold = True
        self.halted = False

    def __op_addr(self, p_offset, mode):
        _pointer = self.pointer + self.RL
        if mode == POS:
            self.memory.extend([0] * (self.memory[_pointer + p_offset] + self.RL - len(self.memory) + 1))
            return self.memory[_pointer + p_offset] + self.RL
        elif mode == REL:
            self.memory.extend([0] * (self.relative + self.memory[_pointer + p_offset] +
                                      self.RL - len(self.memory) + 1))
            return self.relative + self.memory[_pointer + p_offset] + self.RL
        elif mode == IMM:
            return _pointer + p_offset
        elif mode == REG_IMM:
            return self.memory[_pointer + p_offset]
        elif mode == REG_ADR:
            return self.memory[self.memory[_pointer + p_offset]]
        elif mode == REG_REL:
            return self.relative + self.memory[_pointer + p_offset]
        else:
            raise ValueError("I have no memory of this mode: {}".format(mode))

    def exec(self, inputs=None):
        self.cold = False
        self.inputs = inputs or []
        while self.memory[self.pointer + self.RL] % 100 != 99:
            act = self.memory[self.pointer + self.RL]
            m1 = act // 100 % 10
            m2 = act // 1000 % 10
            m3 = act // 10000 % 10
            opcode = act % 100

            addr1 = addr2 = addr3 = None
            if opcode not in OPCODES:
                raise ValueError("wrong opcode {} at position {}".format(act, self.pointer))
            if opcode in OPCODES_ONE + OPCODES_TWO + OPCODES_THREE:
                addr1 = self.__op_addr(1, m1)
            if opcode in OPCODES_TWO + OPCODES_THREE:
                addr2 = self.__op_addr(2, m2)
            if opcode in OPCODES_THREE:
                addr3 = self.__op_addr(3, m3)

            if opcode == INP:
                if len(self.inputs) == 0:
                    raise ValueError("No more input values")
                self.memory[addr1] = self.inputs.pop(0)
                self.pointer += 2
            elif opcode == OUT:
                self.outputs.append(self.memory[addr1])
                self.pointer += 2
                if self.run_mode == PAUSE_ON_OUTPUT:
                    return self
            elif opcode == ADD:
                self.memory[addr3] = self.memory[addr1] + self.memory[addr2]
                self.pointer += 4
            elif opcode == MUL:
                self.memory[addr3] = self.memory[addr1] * self.memory[addr2]
                self.pointer += 4
            elif opcode == JIT:
                if self.memory[addr1] != 0:
                    self.pointer = self.memory[addr2]
                else:
                    self.pointer += 3
            elif opcode == JIF:
                if self.memory[addr1] == 0:
                    self.pointer = self.memory[addr2]
                else:
                    self.pointer += 3
            elif opcode == LES:
                self.memory[addr3] = 1 if self.memory[addr1] < self.memory[addr2] else 0
                self.pointer += 4
            elif opcode == EQU:
                self.memory[addr3] = 1 if self.memory[addr1] == self.memory[addr2] else 0
                self.pointer += 4
            elif opcode == AREL:
                self.relative = self.relative + self.memory[addr1]
                self.pointer += 2
            elif opcode == RET:
                if len(self.stack) > 0:
                    self.pointer = self.stack.pop()
                else:
                    raise ValueError("Nowhere to return to!")
            elif opcode == PROC:
                self.stack.append(self.pointer + 2)
                self.pointer = self.memory[addr1]
            else:
                raise ValueError("What is this magic?")

            if self.pointer > len(self.memory) - 1 + self.RL:
                raise ValueError("Pointer out of range")
        self.halted = True
        return self

    def get_memory_at(self, pos):
        return self.memory[pos + len(self.registers)]

    def get_last_output(self):
        return self.outputs[len(self.outputs) - 1] if self.outputs else None

    def get_outputs(self):
        return self.outputs

    def reset_outputs(self):
        self.outputs = []
        return self
