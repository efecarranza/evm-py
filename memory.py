from constants import MAX_UINT256, MAX_UINT8, is_valid_uint256, is_valid_uint8

ZERO_WORD = [0] * 32

def ceildiv(a, b):
    return -(a // -b)

class InvalidMemoryAccess(Exception):
    pass

class InvalidMemoryValue(Exception):
    pass

def _validate_offset(offset: int) -> None:
    if not is_valid_uint256(offset):
        raise InvalidMemoryAccess({"offset": offset})

class Memory:
    def __init__(self) -> None:
        self.memory = []

    def store(self, offset: int, value: int) -> None:
        _validate_offset(offset)
        if not is_valid_uint8(value):
            raise InvalidMemoryValue({"offset": offset, "value": value})

        self._expand_if_needed(offset)

        if offset >= len(self.memory):
            self.memory.extend([0] * (offset - len(self.memory) + 1))
        
        self.memory[offset] = value

    def load(self, offset: int) -> int:
        if offset < 0:
            raise InvalidMemoryAccess({"offset": offset})

        if offset >= len(self.memory):
            return 0

        return self.memory[offset]

    def load_range(self, offset: int, length: int) -> bytes:
        if offset < 0:
            raise InvalidMemoryAccess({"offset": offset, "length": length})

        return bytes(self.load(x) for x in range(offset, offset + length))

    def active_words(self) -> int:
        return len(self.memory) // 32

    def _expand_if_needed(self, offset: int) -> None:
        if offset < len(self.memory):
            return
        active_words_after =  max(self.active_words(), ceildiv(offset + 1, 32))
        self.memory.extend(ZERO_WORD * (active_words_after - self.active_words()))
        assert len(self.memory) % 32 == 0

    def __str__(self) -> str:
        return str(self.memory)

    def __repr__(self) -> str:
        return str(self)
