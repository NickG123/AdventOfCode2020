from enum import Enum
from typing import List, Set, Tuple

INPUT = "input"


class Operation(Enum):
    acc = "acc"
    jmp = "jmp"
    nop = "nop"


ProgramLines = List[Tuple[Operation, int]]


class Program:
    def __init__(self, lines: ProgramLines):
        self.lines = lines
        self.reset()

    def reset(self) -> None:
        self.position = 0
        self.accumulator = 0
        self.visited_lines: Set[int] = set()

    def run_until_loop(self) -> None:
        while self.position not in self.visited_lines and self.position < len(self.lines):
            self.visited_lines.add(self.position)
            op, arg = self.lines[self.position]
            if op == Operation.acc:
                self.accumulator += arg
                self.position += 1
            elif op == Operation.jmp:
                self.position += arg
            elif op == Operation.nop:
                self.position += 1

    def fix_program(self) -> None:
        for i, (op, arg) in enumerate(self.lines):
            self.reset()
            if op == Operation.jmp:
                replacement = (Operation.nop, arg)
            elif op == Operation.nop:
                replacement = (Operation.jmp, arg)
            else:
                continue
            self.lines[i] = replacement
            self.run_until_loop()
            if self.position == len(self.lines):
                break
            self.lines[i] = (op, arg)
        else:
            raise Exception("No solution found")


def read_program() -> ProgramLines:
    result = []
    with open(INPUT, "r") as fin:
        for line in fin:
            op, val = line.strip().split(" ")
            result.append((Operation(op), int(val)))
    return result


def main() -> None:
    program = Program(read_program())
    program.run_until_loop()
    print(program.accumulator)
    program.fix_program()
    print(program.accumulator)


if __name__ == "__main__":
    main()
