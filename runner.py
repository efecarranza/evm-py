from dataclasses import dataclass
from context import ExecutionContext
from opcodes import decode_opcode

@dataclass
class ExecutionLimitReached(Exception):
    context: ExecutionContext

def run(code: bytes) -> None:
    context = ExecutionContext(code=code)

    while not context.stopped:
        pc_before = context.pc
        instruction = decode_opcode(context)
        instruction.execute(context)

        print(f"{instruction} @pc={pc_before}")
        print(context)
        print()
    print(f'Output: 0x{context.returndata.hex()}')
