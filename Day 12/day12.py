from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from math import sin, cos, radians

INPUT = "input"


class Command(Enum):
    N = "N"
    E = "E"
    S = "S"
    W = "W"
    L = "L"
    R = "R"
    F = "F"


class Direction(Enum):
    N = 0
    E = 90
    S = 180
    W = 270


@dataclass
class Point:
    x: int
    y: int

    def __add__(self, other: Point) -> Point:
        return Point(self.x + other.x, self.y + other.y)

    def __iadd__(self, other: Point) -> Point:
        self.x += other.x
        self.y += other.y
        return self

    def __mul__(self, scalar: int) -> Point:
        return Point(self.x * scalar, self.y * scalar)

    def manhatten_distance(self) -> int:
        return abs(self.x) + abs(self.y)

    def rotate_about_origin(self, degrees: int) -> None:
        rad = radians(degrees)
        new_x = self.x * cos(rad) + self.y * sin(rad)
        new_y = - self.x * sin(rad) + self.y * cos(rad)
        self.x = int(round(new_x))
        self.y = int(round(new_y))

    def move(self, direction: Direction, distance: int) -> None:
        self += VECTORS[direction] * distance


MAX_COMPASS = 360


COMMAND_TO_DIR = {
    Command.N: Direction.N,
    Command.E: Direction.E,
    Command.S: Direction.S,
    Command.W: Direction.W
}

ROTATION_DIRECTION = {
    Command.R: 1,
    Command.L: -1
}

VECTORS = {
    Direction.N: Point(0, 1),
    Direction.E: Point(1, 0),
    Direction.S: Point(0, -1),
    Direction.W: Point(-1, 0)
}


class Part1Ship:
    def __init__(self) -> None:
        self.position = Point(0, 0)
        self.direction = Direction.E

    def follow_command(self, command: Command, arg: int) -> None:
        if command in ROTATION_DIRECTION:
            self.direction = Direction((self.direction.value + arg * ROTATION_DIRECTION[command]) % MAX_COMPASS)
        else:
            self.position.move(COMMAND_TO_DIR.get(command, self.direction), arg)


class Part2Ship:
    def __init__(self) -> None:
        self.position = Point(0, 0)
        self.waypoint = Point(10, 1)

    def follow_command(self, command: Command, arg: int) -> None:
        if command in COMMAND_TO_DIR:
            self.waypoint.move(COMMAND_TO_DIR[command], arg)
        elif command == Command.F:
            self.position += self.waypoint * arg
        else:
            self.waypoint.rotate_about_origin(arg * ROTATION_DIRECTION[command])


def main() -> None:
    part_1_ship = Part1Ship()
    part_2_ship = Part2Ship()
    with open(INPUT, "r") as fin:
        for line in fin:
            command = Command(line[0])
            arg = int(line[1:])
            part_1_ship.follow_command(command, arg)
            part_2_ship.follow_command(command, arg)
    print(part_1_ship.position.manhatten_distance())
    print(part_2_ship.position.manhatten_distance())


if __name__ == "__main__":
    main()
