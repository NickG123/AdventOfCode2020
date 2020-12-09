from enum import Enum
from typing import Dict, List, Set, Tuple

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
        self.winning_lines: Dict[int, bool] = {}

    def reset(self) -> None:
        self.position = 0
        self.accumulator = 0
        self.visited_lines: Set[int] = set()

    def get_next_line_offset(self, op: Operation, arg: int) -> int:
        if op == Operation.jmp:
            return arg
        return 1

    def run_until_loop_or_end(self) -> None:
        while self.position not in self.visited_lines and self.position < len(self.lines):
            self.visited_lines.add(self.position)
            op, arg = self.lines[self.position]
            if op == Operation.acc:
                self.accumulator += arg
            self.position += self.get_next_line_offset(op, arg)

    def is_winning_line(self, line_num: int) -> bool:
        if line_num >= len(self.lines):
            return True
        if line_num in self.winning_lines:
            return self.winning_lines[line_num]
        if line_num in self.visited_lines:
            self.winning_lines[line_num] = False
            return False

        self.visited_lines.add(line_num)

        result = self.is_winning_line(line_num + self.get_next_line_offset(*self.lines[line_num]))
        self.winning_lines[line_num] = result
        return result

    def fix_program(self) -> None:
        position = 0
        while True:
            op, arg = self.lines[position]
            if op == Operation.jmp and self.is_winning_line(position + 1):
                self.lines[position] = (Operation.nop, arg)
                break
            elif op == Operation.nop and self.is_winning_line(position + arg):
                self.lines[position] = (Operation.jmp, arg)
                break
            position += self.get_next_line_offset(op, arg)
        else:
            raise Exception("No solution found")
        self.reset()


def read_program() -> ProgramLines:
    result = []
    with open(INPUT, "r") as fin:
        for line in fin:
            op, val = line.strip().split(" ")
            result.append((Operation(op), int(val)))
    return result


def main() -> None:
    program = Program(read_program())
    program.run_until_loop_or_end()
    print(program.accumulator)
    program.reset()
    program.fix_program()
    program.run_until_loop_or_end()
    print(program.accumulator)


if __name__ == "__main__":
    main()
