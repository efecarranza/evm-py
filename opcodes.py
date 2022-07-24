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
DUP1 = register_instruction(0x80, "DUP1", (lambda ctx: ctx.stack.push(ctx.stack.peek(0))))
DUP2 = register_instruction(0x80, "DUP2", (lambda ctx: ctx.stack.push(ctx.stack.peek(1))))
DUP3 = register_instruction(0x80, "DUP3", (lambda ctx: ctx.stack.push(ctx.stack.peek(2))))
DUP4 = register_instruction(0x80, "DUP4", (lambda ctx: ctx.stack.push(ctx.stack.peek(3))))
DUP5 = register_instruction(0x80, "DUP5", (lambda ctx: ctx.stack.push(ctx.stack.peek(4))))
DUP6 = register_instruction(0x80, "DUP6", (lambda ctx: ctx.stack.push(ctx.stack.peek(5))))
DUP7 = register_instruction(0x80, "DUP7", (lambda ctx: ctx.stack.push(ctx.stack.peek(6))))
DUP8 = register_instruction(0x80, "DUP8", (lambda ctx: ctx.stack.push(ctx.stack.peek(7))))
DUP9 = register_instruction(0x80, "DUP9", (lambda ctx: ctx.stack.push(ctx.stack.peek(8))))
DUP10 = register_instruction(0x80, "DUP10", (lambda ctx: ctx.stack.push(ctx.stack.peek(9))))
DUP11 = register_instruction(0x80, "DUP11", (lambda ctx: ctx.stack.push(ctx.stack.peek(10))))
DUP12 = register_instruction(0x80, "DUP12", (lambda ctx: ctx.stack.push(ctx.stack.peek(11))))
DUP13 = register_instruction(0x80, "DUP13", (lambda ctx: ctx.stack.push(ctx.stack.peek(12))))
DUP14 = register_instruction(0x80, "DUP14", (lambda ctx: ctx.stack.push(ctx.stack.peek(13))))
DUP15 = register_instruction(0x80, "DUP15", (lambda ctx: ctx.stack.push(ctx.stack.peek(14))))
DUP16 = register_instruction(0x80, "DUP16", (lambda ctx: ctx.stack.push(ctx.stack.peek(15))))


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