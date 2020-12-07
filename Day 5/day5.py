from typing import Optional

INPUT = "input"
ROW_SPECIFIERS = 7
POSITIVE_INDICATORS = {"B", "R"}


def parse_seat_part(seat_part: str) -> int:
    result = 0
    for i, v in enumerate(reversed(seat_part)):
        if v in POSITIVE_INDICATORS:
            result |= 1 << i
    return result


def parse_seat(seat: str) -> int:
    return parse_seat_part(seat[:ROW_SPECIFIERS]) * 8 + parse_seat_part(seat[ROW_SPECIFIERS:])


def sum_a_to_b_inclusive(a: int, b: int) -> int:
    n = b - a + 1
    return (a - 1) * n + (n * (n + 1) // 2)


def main() -> None:
    total = 0
    min_id: Optional[int] = None
    max_id: Optional[int] = None

    with open(INPUT, "r") as fin:
        for line in fin:
            seat_id = parse_seat(line.strip())
            total += seat_id
            min_id = seat_id if min_id is None else min(min_id, seat_id)
            max_id = seat_id if max_id is None else max(max_id, seat_id)

    print(max_id)
    print(sum_a_to_b_inclusive(min_id, max_id) - total)


if __name__ == "__main__":
    main()
