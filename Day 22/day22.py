from __future__ import annotations
import itertools

from collections import deque
from typing import Deque, TextIO

INPUT = "input"


def read_deck(fin: TextIO) -> Deque[int]:
    result: Deque[int] = deque()
    next(fin)  # Skip header
    for line in fin:
        if not line.strip():
            break
        result.append(int(line))
    return result


def play_round(deck1: Deque[int], deck2: Deque[int]) -> None:
    p1 = deck1.popleft()
    p2 = deck2.popleft()
    target_deck = deck1 if p1 > p2 else deck2
    target_deck.append(max(p1, p2))
    target_deck.append(min(p1, p2))


def recursive_combat(deck1: Deque[int], deck2: Deque[int]) -> int:
    previous_states = set()
    while deck1 and deck2:
        state = (tuple(deck1), tuple(deck2))
        if state in previous_states:
            return 1
        previous_states.add(state)
        p1 = deck1.popleft()
        p2 = deck2.popleft()
        if len(deck1) >= p1 and len(deck2) >= p2:
            result = recursive_combat(deque(itertools.islice(deck1, 0, p1)), deque(itertools.islice(deck2, 0, p2)))
        else:
            result = 1 if p1 > p2 else 2
        if result == 1:
            deck1.append(p1)
            deck1.append(p2)
        else:
            deck2.append(p2)
            deck2.append(p1)
    return 1 if deck1 else 2


def compute_score(deck: Deque[int]) -> int:
    return sum((i + 1) * val for i, val in enumerate(reversed(deck)))


def main() -> None:
    with open(INPUT, "r") as fin:
        d1 = read_deck(fin)
        d1_p2 = deque(d1)
        d2 = read_deck(fin)
        d2_p2 = deque(d2)
    while d1 and d2:
        play_round(d1, d2)
    winning_deck = d1 or d2
    print(compute_score(winning_deck))

    winning_deck = d1_p2 if recursive_combat(d1_p2, d2_p2) == 1 else d2_p2
    print(compute_score(winning_deck))


if __name__ == "__main__":
    main()
