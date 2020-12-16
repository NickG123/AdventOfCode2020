from typing import Dict, List


def run(starting_nums: List[int], turns: int) -> None:
    turn_spoken: Dict[int, int] = {}
    prev_num_delta = None

    for i in range(turns):
        if i < len(starting_nums):
            next_num = starting_nums[i]
        else:
            next_num = prev_num_delta if prev_num_delta is not None else 0

        prev_num_delta = None if next_num not in turn_spoken else i - turn_spoken[next_num]
        turn_spoken[next_num] = i

    print(next_num)


if __name__ == "__main__":
    lst = [6, 19, 0, 5, 7, 13, 1]
    run(lst, 2020)
    run(lst, 30000000)
