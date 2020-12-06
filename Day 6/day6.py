def main() -> None:
    group = set()
    count = 0
    with open("input", "r") as fin:
        for line in (l.strip() for l in fin):
            if line:
                group.update(line)
            else:
                count += len(group)
                group = set()
    print(count + len(group))


if __name__ == '__main__':
    main()
