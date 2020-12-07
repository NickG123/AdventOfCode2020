from dataclasses import dataclass

INPUT = "input"


@dataclass
class Policy:
    character: str
    min: int
    max: int


def parse_policy(policy: str) -> Policy:
    min_max, character = policy.split(" ")
    min_val, max_val = min_max.split("-")
    return Policy(character, int(min_val), int(max_val))


def validate_password_part_1(policy: Policy, password: str) -> bool:
    return policy.min <= password.count(policy.character) <= policy.max


def validate_password_part_2(policy: Policy, password: str) -> bool:
    return (password[policy.min - 1] == policy.character) != (password[policy.max - 1] == policy.character)


def main() -> None:
    valid_part_1 = 0
    valid_part_2 = 0
    with open(INPUT, "r") as fin:
        for line in fin:
            policy_str, password = line.strip().split(": ")
            policy = parse_policy(policy_str)
            if validate_password_part_1(policy, password):
                valid_part_1 += 1
            if validate_password_part_2(policy, password):
                valid_part_2 += 1
    print(valid_part_1)
    print(valid_part_2)


if __name__ == "__main__":
    main()
