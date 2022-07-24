
import pytest
from context import ExecutionContext
from opcodes import *
from runner import run, ExecutionLimitReached


def test_infinite_loop():
    code = assemble([
        JUMPDEST,
        PUSH1, 0,
        JUMP
    ])
    with pytest.raises(ExecutionLimitedReached) as excinfo:
        run(code, max_steps=100)
