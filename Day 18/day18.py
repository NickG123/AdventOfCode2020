import operator
from typing import Iterator


INPUT = "input"
OPERATORS = {"+": operator.add, "*": operator.mul}


def parse_expression(tokens: Iterator[str], add_pres: bool) -> int:
    left = parse_factor(tokens, add_pres)
    for elem in tokens:
        if elem == ")":
            break
        op = OPERATORS[elem]
        if add_pres and op == operator.mul:
            return left * parse_expression(tokens, add_pres)
        factor = parse_factor(tokens, add_pres)
        left = op(left, factor)
    return left


def parse_factor(tokens: Iterator[str], add_pres: bool) -> int:
    token = next(tokens)
    if token == "(":
        return parse_expression(tokens, add_pres)
    else:
        return int(token)


def tokenize(s: str) -> Iterator[str]:
    for s in s.split(" "):
        for c in s:
            if c == "(":
                yield "("
            else:
                break
        yield s.strip("()")
        for c in reversed(s):
            if c == ")":
                yield ")"
            else:
                break


def main() -> None:
    p1_total = 0
    p2_total = 0
    with open(INPUT, "r") as fin:
        for line in fin:
            p1_total += parse_expression(tokenize(line.strip()), False)
            p2_total += parse_expression(tokenize(line.strip()), True)
    print(p1_total)
    print(p2_total)


if __name__ == "__main__":
    main()
