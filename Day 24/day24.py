from __future__ import annotations
from typing import Dict, Iterable, List, Optional, Set, Tuple

INPUT = "input"
DIRECTIONS = {
    "e": (1, 0),
    "w": (-1, 0),
    "se": (1, -1),
    "sw": (0, -1),
    "ne": (0, 1),
    "nw": (-1, 1)
}


class Tile:
    def __init__(self, x: int, y: int, black: bool = False) -> None:
        self.x = x
        self.y = y
        self.black = black
        self._neighbours: Optional[List[Tile]] = None

    def get_neighbours(self, tile_dict: Dict[Tuple[int, int], Tile]) -> List[Tile]:
        if self._neighbours is None:
            self._neighbours = []
            for x, y in [(self.x + x, self.y + y) for x, y in DIRECTIONS.values()]:
                if (x, y) not in tile_dict:
                    tile_dict[(x, y)] = Tile(x, y)
                self._neighbours.append(tile_dict[(x, y)])
        return self._neighbours


def parse_directions(line: str) -> Iterable[str]:
    it = iter(line)
    for c in it:
        if c in {"e", "w"}:
            yield c
        else:
            yield c + next(it)


def get_tile(directions: Iterable[str]) -> Tuple[int, int]:
    x = 0
    y = 0
    for d in directions:
        dx, dy = DIRECTIONS[d]
        x += dx
        y += dy
    return x, y


def part2(tiles: Dict[Tuple[int, int], Tile]) -> int:
    can_change = set()
    for tile in list(tiles.values()):
        can_change.add(tile)
        can_change.update(tile.get_neighbours(tiles))

    for _ in range(100):
        changes = []
        new_can_change = set()
        for tile in can_change:
            if tile.black:
                black_neighbours = sum(n.black for n in tile.get_neighbours(tiles))
                if black_neighbours == 0 or black_neighbours > 2:
                    changes.append(tile)
            elif sum(n.black for n in tile.get_neighbours(tiles)) == 2:
                changes.append(tile)
            else:
                continue
            new_can_change.add(tile)
            new_can_change.update(tile.get_neighbours(tiles))

        can_change = new_can_change
        for tile in changes:
            tile.black = not tile.black
    return sum(n.black for n in tiles.values())


def main() -> None:
    black_tiles: Set[Tuple[int, int]] = set()
    with open(INPUT, "r") as fin:
        for line in fin:
            pos = get_tile(parse_directions(line.strip()))
            if pos in black_tiles:
                black_tiles.remove(pos)
            else:
                black_tiles.add(pos)
    print(len(black_tiles))
    print(part2({(x, y): Tile(x, y, True) for x, y in black_tiles}))


if __name__ == "__main__":
    main()
