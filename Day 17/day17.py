from __future__ import annotations

from collections import defaultdict
from enum import Enum
from typing import Iterable, List, Set, TextIO, Tuple

INPUT = "input"


class CubeStatus(Enum):
    ACTIVE = "#"
    INACTIVE = "."


Position = Tuple[int, ...]


def compute_position_offsets(dimension: int) -> Iterable[Position]:
    if dimension == 0:
        yield ()
    else:
        for i in range(-1, 2):
            for subdimension in compute_position_offsets(dimension - 1):
                yield (i,) + subdimension


class Grid:
    def __init__(self, fin: TextIO, dimensions: int) -> None:
        self.could_change = set()
        self.grid = defaultdict(lambda: CubeStatus.INACTIVE)
        self.position_offsets = [offset for offset in compute_position_offsets(dimensions) if not all(o == 0 for o in offset)]
        for y, line in enumerate(fin):
            for x, val in enumerate(line.strip()):
                pos = (x, y) + (0,) * (dimensions - 2)
                self.grid[pos] = CubeStatus(val)
                self.could_change.add(pos)
                self.could_change.update(self.neighbours(pos))

    def toggle_cell(self, position: Position) -> None:
        if self.grid[position] == CubeStatus.ACTIVE:
            self.grid[position] = CubeStatus.INACTIVE
        else:
            self.grid[position] = CubeStatus.ACTIVE

    def neighbours(self, position: Tuple[int, ...]) -> Iterable[Tuple[int, ...]]:
        for offset in self.position_offsets:
            yield tuple(p + o for (p, o) in zip(position, offset))

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


def main() -> None:
    with open(INPUT, "r") as fin:
        grid_3 = Grid(fin, 3)
    with open(INPUT, "r") as fin:
        grid_4 = Grid(fin, 4)
    for i in range(6):
        grid_3.step()
        grid_4.step()
    print(grid_3.num_active())
    print(grid_4.num_active())


if __name__ == "__main__":
    main()
