from linked_list import (
    test_bubble_sort,
    test_crud,
    test_merge,
    test_merge_n,
    test_remove_nth_from_end,
    test_reverse,
    test_variants,
)


def main() -> None:
    for test in (
        test_crud,
        test_bubble_sort,
        test_reverse,
        test_remove_nth_from_end,
        test_merge,
        test_merge_n,
        test_variants,
    ):
        print(f"\n== {test.__name__} ==")  # noqa: T201
        test()


if __name__ == "__main__":
    main()
