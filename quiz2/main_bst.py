from bst import (
    test_are_identical,
    test_balance_bst,
    test_count_leaf_nodes,
    test_count_nodes,
    test_crud,
    test_traversals,
    test_variants,
)


def main() -> None:
    for test in (
        test_crud,
        test_traversals,
        test_count_nodes,
        test_count_leaf_nodes,
        test_are_identical,
        test_balance_bst,
        test_variants,
    ):
        print(f"\n== {test.__name__} ==")  # noqa: T201
        test()


if __name__ == "__main__":
    main()
