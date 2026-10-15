from iteration import Iteration  # noqa: CPY001


def run_selection_sort(original: list[int]) -> list[int]:
    it = Iteration()
    it.data = original.copy()
    return it.selection_sort()


def check_sorted(original: list[int]) -> None:
    actual = run_selection_sort(original)
    expected = sorted(original)
    assert actual == expected, f"input {original}: expected {expected}, got {actual}"


def test_empty_list() -> None:
    check_sorted([])


def test_one_item() -> None:
    check_sorted([7])


def test_ascending() -> None:
    check_sorted([1, 2, 3, 4, 5])


def test_descending() -> None:
    check_sorted([5, 4, 3, 2, 1])


def test_repeated_values() -> None:
    check_sorted([3, 1, 3, 2, 1, 3])


def test_all_equal() -> None:
    check_sorted([4, 4, 4, 4])


def test_negative_values() -> None:
    check_sorted([-2, 5, -9, 0, -1])


def main() -> None:
    tests = [
        test_empty_list,
        test_one_item,
        test_ascending,
        test_descending,
        test_repeated_values,
        test_all_equal,
        test_negative_values,
    ]

    failed = 0
    for test in tests:
        try:
            test()
        except AssertionError as e:
            failed += 1
            print(f"FAIL {test.__name__}: {e}")
        else:
            print(f"PASS {test.__name__}")

    print(f"\n{len(tests) - failed}/{len(tests)} passed")


if __name__ == "__main__":
    main()
