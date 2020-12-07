from typing import Iterable, List, Set

INPUT = "input"


def read_groups_from_file() -> Iterable[List[Set[str]]]:
    with open(INPUT, "r") as fin:
        group = []
        for line in fin:
            stripped = line.strip()
            if stripped:
                group.append(set(stripped))
            else:
                yield group
                group = []
    if group:
        yield group


def main() -> None:
    count = 0
    intersection_count = 0

    for group in read_groups_from_file():
        union = set()
        intersection = None

        for person in group:
            union.update(person)
            intersection = person if intersection is None else intersection & person

        count += len(union)
        intersection_count += len(intersection)

    print(count)
    print(intersection_count)


if __name__ == '__main__':
    main()
