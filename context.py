from memory import Memory


from memory import Memory
from stack import Stack

class ExecutionContext:
    def __init__(self, code=bytes(), pc=0, stack=Stack(), memory=Memory()) -> None:
        self.code = code
        self.stack = stack
        self.memory = memory
        self.pc = pc
        self.stopped = False
        self.returndata = bytes()

    def stop(self) -> None:
        self.stopped = True

    def read_code(self, num_bytes) -> int:
        value = int.from_bytes(self.code[self.pc: self.pc + num_bytes], byteorder="big")
        self.pc += num_bytes
        return value

    def set_return_data(self, offset: int, length: int) -> None:
        self.stopped = True
        self.returndata = self.memory.load_range(offset, length)

    def __str__(self) -> str:
        return "Stack: " + str(self.stack) + "\nmemory: " + str(self.memory)

    def __repr__(self) -> str:
        return str(self)
