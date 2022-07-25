from dataclasses import dataclass
from context import ExecutionContext

@dataclass
class EVMException(Exception):
    context: ExecutionContext

class UnknownOpcode(EVMException):
    pass

class InvalidCodeOffset(EVMException):
    pass

@dataclass
class InvalidJumpDestination(EVMException):
    target_pc: int
