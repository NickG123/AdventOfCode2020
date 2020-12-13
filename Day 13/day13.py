from math import ceil
from typing import List, Tuple

INPUT = "input"


def find_next_occurrance(current_time: int, current_interval: int, offset: int, frequency: int) -> int:
    t = current_time
    while (t + offset) % frequency != 0:
        t += current_interval
    return t


def part2(busses: List[Tuple[int, int]]) -> int:
    current_interval = busses[0][1]
    current_time = 0
    for offset, frequency in busses:
        first_occurance = find_next_occurrance(current_time, current_interval, offset, frequency)
        second_occurance = find_next_occurrance(first_occurance + current_interval, current_interval, offset, frequency)
        current_interval = second_occurance - first_occurance
        current_time = first_occurance
    return current_time


def main() -> None:
    with open(INPUT, "r") as fin:
        t = int(fin.readline())
        busses = [(i, int(x)) for i, x in enumerate(fin.readline().split(",")) if x != 'x']
    first_departure_after_t = [
        (int(ceil(t / x)) * x, x)
        for i, x in busses
    ]
    leave_time, bus = min(first_departure_after_t)
    print(bus * (leave_time - t))
    print(part2(busses))


if __name__ == "__main__":
    main()
