from itertools import count

MODULUS = 20201227


def find_loop_count(subject_number: int, public_key: int) -> int:
    for i in count(0, 1):
        if pow(subject_number, i, MODULUS) == public_key:
            return i


def transform(subject_number: int, loop_count: int) -> int:
    return pow(subject_number, loop_count, MODULUS)


def main() -> None:
    pub_key_1 = 16616892
    pub_key_2 = 14505727

    loop_count_1 = find_loop_count(7, pub_key_1)
    loop_count_2 = find_loop_count(7, pub_key_2)

    encryption_key_1 = transform(pub_key_1, loop_count_2)
    encryption_key_2 = transform(pub_key_2, loop_count_1)
    assert encryption_key_1 == encryption_key_2

    print(encryption_key_1)


if __name__ == "__main__":
    main()
