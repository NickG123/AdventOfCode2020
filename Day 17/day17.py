from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
from typing import Iterable, List, Set, TextIO

INPUT = "input"


class CubeStatus(Enum):
    ACTIVE = "#"
    INACTIVE = "."


@dataclass(order=True, frozen=True)
class Position:
    x: int
    y: int
    z: int


class Grid:
    def __init__(self, fin: TextIO) -> None:
        self.could_change = set()
        self.grid = defaultdict(lambda: CubeStatus.INACTIVE)
        for y, line in enumerate(fin):
            for x, val in enumerate(line.strip()):
                pos = Position(x, y, 0)
                self.grid[pos] = CubeStatus(val)
                self.could_change.add(pos)
                self.could_change.update(self.neighbours(pos))

    def toggle_cell(self, position: Position) -> None:
        if self.grid[position] == CubeStatus.ACTIVE:
            self.grid[position] = CubeStatus.INACTIVE
        else:
            self.grid[position] = CubeStatus.ACTIVE

    def neighbours(self, position: Position) -> Iterable[Position]:
        for x in range(-1, 2):
            for y in range(-1, 2):
                for z in range(-1, 2):
                    if x != 0 or y != 0 or z != 0:
                        yield Position(x + position.x, y + position.y, z + position.z)

    def step(self) -> None:
        changes: List[Position] = []
        new_could_change: Set[Position] = set()
        for pos in self.could_change:
            neighbours = list(self.neighbours(pos))
            status = self.grid[pos]

            if status == CubeStatus.ACTIVE and not sum(self.grid[c] == CubeStatus.ACTIVE for c in neighbours) in {2, 3}:
                changes.append(pos)
            elif status == CubeStatus.INACTIVE and sum(self.grid[c] == CubeStatus.ACTIVE for c in neighbours) == 3:
                changes.append(pos)
            else:
                continue
            new_could_change.update(neighbours)
            new_could_change.add(pos)

        self.could_change = new_could_change
        for update in changes:
            self.toggle_cell(update)

    def num_active(self) -> int:
        return sum(cell_state == CubeStatus.ACTIVE for cell_state in self.grid.values())

    def __str__(self) -> str:
        min_pos = min(self.grid)
        max_pos = max(self.grid)
        result = []
        for z in range(min_pos.z, max_pos.z + 1):
            result.append(f"z={z}")
            for y in range(min_pos.y, max_pos.y + 1):
                result.append("".join(self.grid[Position(x, y, z)].value for x in range(min_pos.x, max_pos.x + 1)))
        return "\n".join(result) + "\n"


def main() -> None:
    with open(INPUT, "r") as fin:
        grid = Grid(fin)
    for i in range(6):
        grid.step()
    print(grid.num_active())


if __name__ == "__main__":
    main()
