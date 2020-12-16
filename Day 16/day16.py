import operator
from functools import reduce
from typing import Dict, Iterable, List, TextIO, Set

INPUT = "input"


class RangeList:
    def __init__(self, ranges: List[range]):
        self.ranges = ranges

    def __contains__(self, value: int) -> bool:
        return any(value in range for range in self.ranges)

    def __str__(self) -> str:
        ranges = ", ".join(f"{r.start}-{r.stop - 1}" for r in self.ranges)
        return f"[{ranges}]"

    def __repr__(self) -> str:
        return str(self)


class TicketProcessor:
    def __init__(self, fields: Dict[str, RangeList]) -> None:
        self.fields = fields
        self.possible_indices = {name: set(range(len(self.fields))) for name in self.fields}

    def process_ticket(self, ticket: List[int]) -> None:
        for i, val in enumerate(ticket):
            for field, options in self.possible_indices.items():
                if i not in options or val in self.fields[field]:
                    continue
                self.remove_option(options, i)

    def remove_option(self, options: Set[int], option: int) -> None:
        if option in options:
            options.remove(option)
            if len(options) == 1:
                self.remove_from_other_sets(next(iter(options)))

    def remove_from_other_sets(self, option: int) -> None:
        for options in self.possible_indices.values():
            if options != {option}:
                self.remove_option(options, option)

    def label_ticket(self, ticket: List[int]) -> Dict[str, int]:
        assert all(len(options) == 1 for options in self.possible_indices.values())
        return {name: ticket[next(iter(options))] for name, options in self.possible_indices.items()}


def parse_range(s: str) -> range:
    lower, upper = s.split("-")
    return range(int(lower), int(upper) + 1)


def read_ranges(fin: TextIO) -> Dict[str, RangeList]:
    result = {}
    for line in fin:
        if not line.strip():
            break
        name, ranges_str = line.split(": ")
        ranges = RangeList([parse_range(r) for r in ranges_str.split(" or ")])
        result[name] = ranges
    return result


def read_tickets(fin: TextIO) -> Iterable[List[int]]:
    fin.readline()  # Skip header
    for line in fin:
        if not line.strip():
            break
        yield [int(x) for x in line.split(",")]


def main() -> None:
    with open(INPUT, "r") as fin:
        ranges = read_ranges(fin)
        all_ranges = RangeList([r for rangelist in ranges.values() for r in rangelist.ranges])
        my_ticket = list(read_tickets(fin)).pop()

        ticket_processor = TicketProcessor(ranges)

        error_rate = 0
        for ticket in read_tickets(fin):
            invalid_values = [x for x in ticket if x not in all_ranges]
            error_rate += sum(invalid_values)
            if len(invalid_values) == 0:
                ticket_processor.process_ticket(ticket)

        print(error_rate)
        labeled = ticket_processor.label_ticket(my_ticket)
        departure_fields = [val for name, val in labeled.items() if name.startswith("departure")]
        print(reduce(operator.mul, departure_fields, 1))


if __name__ == "__main__":
    main()
