from atexit import register
from context import ExecutionContext

class Instruction:
    def __init__(self, opcode: int, name: str):
        self.opcode = opcode
        self.name = name

    def execute(self, context: ExecutionContext) -> None:
        raise NotImplementedError()

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name

INSTRUCTIONS = []
INSTRUCTIONS_BY_OPCODE = {}

def register_instruction(opcode: int, name: str, execute_func: callable):
    instruction = Instruction(opcode, name)
    instruction.execute = execute_func
    INSTRUCTIONS.append(instruction)

    assert opcode not in INSTRUCTIONS_BY_OPCODE
    INSTRUCTIONS_BY_OPCODE[opcode] = instruction

    return instruction

STOP = register_instruction(0x00, "STOP", (lambda ctx: ctx.stop()))
PUSH1 = register_instruction(0x60, "PUSH1", (lambda ctx: ctx.stack.push(ctx.read_code(1))))
ADD = register_instruction(0x01, "ADD", (lambda ctx: ctx.stack.push((ctx.stack.pop() + ctx.stack.pop()) % 2**256)))
MUL = register_instruction(0x02, "MUL", (lambda ctx: ctx.stack.push((ctx.stack.pop() * ctx.stack.pop()) % 2**256)))
MSTORE8 = register_instruction(0x53, "MSTORE8", (lambda ctx: ctx.memory.store(ctx.stack.pop(), ctx.stack.pop() % 256)))
RETURN = register_instruction(0xf3, "RETURN", (lambda ctx: ctx.set_return_data(ctx.stack.pop(), ctx.stack.pop())))

def decode_opcode(context: ExecutionContext) -> Instruction:
    if context.pc < 0:
        raise InvalidCodeOffset({"code": context.code, "pc": context.pc})

    if context.pc >= len(context.code):
        return STOP

    opcode = context.read_code(1)
    instruction = INSTRUCTIONS_BY_OPCODE.get(opcode)
    if instruction is None:
        raise UknownOpcode({"opcode": opcode})

    return instruction

class InvalidCodeOffset(Exception):
    pass

class UknownOpcode(Exception):
    pass