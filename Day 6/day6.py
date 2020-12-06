def main() -> None:
    group = set()
    intersection = None
    count = 0
    intersection_count = 0
    with open("input", "r") as fin:
        for line in (l.strip() for l in fin):
            if line:
                group.update(line)
                answers = set(line)
                intersection = answers if intersection is None else intersection & answers
            else:
                count += len(group)
                intersection_count += len(intersection)
                group = set()
                intersection = None
    print(count + len(group))
    print(intersection_count + len(intersection))


if __name__ == '__main__':
    main()
