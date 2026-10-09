from random import sample


class Recursion:
    def __init__(self, max_size: int = 100) -> None:
        self.data: list[int] = []
        self.max_size: int = max_size

    def initialise(self) -> None:
        self.data = sample(range(1, 3 * self.max_size), self.max_size)

    def __str__(self) -> str:
        return str(self.data)

    # 1. Fibonacci: F(1) = F(2) = 1, F(n) = F(n - 1) + F(n - 2)
    def fib_iter(self, n: int) -> int:
        if n < 1:
            raise ValueError
        if n <= 2:  # noqa: PLR2004
            return 1

        previous, current = 1, 1
        for _ in range(3, n + 1):
            previous, current = current, previous + current
        return current

    def fib_recur(self, n: int) -> int:
        if n < 1:
            raise ValueError
        if n <= 2:  # noqa: PLR2004
            return 1

        return self.fib_recur(n - 1) + self.fib_recur(n - 2)

    def fib_memo(self, n: int, memo: dict[int, int] | None = None) -> int:
        if n < 1:
            raise ValueError
        if n <= 2:  # noqa: PLR2004
            return 1

        # A fresh dict per top-level call, so state never leaks between calls
        if memo is None:
            memo = {}
        if n not in memo:
            memo[n] = self.fib_memo(n - 1, memo) + self.fib_memo(n - 2, memo)
        return memo[n]

    # 2. Greatest common divisor by repeated subtraction
    def gcd(self, n: int, m: int) -> int:
        if n <= 0 or m <= 0:
            raise ValueError
        if n == m:
            return n

        return self.gcd(abs(n - m), min(n, m))

    # 3. Merge sort (inclusive bounds)
    def merge_sort(self) -> list[int]:
        self._merge_sort(self.data, 0, len(self.data) - 1)
        return self.data

    def _merge_sort(self, arr: list[int], start: int, end: int) -> None:
        if start >= end:
            return

        mid = (start + end) // 2
        self._merge_sort(arr, start, mid)
        self._merge_sort(arr, mid + 1, end)
        self._merge(arr, start, mid, end)

    def _merge(self, arr: list[int], start: int, mid: int, end: int) -> None:
        merged: list[int] = []
        left, right = start, mid + 1

        while left <= mid and right <= end:
            # <= takes the left item first on ties, which keeps the sort stable
            if arr[left] <= arr[right]:
                merged.append(arr[left])
                left += 1
            else:
                merged.append(arr[right])
                right += 1

        merged.extend(arr[left : mid + 1])
        merged.extend(arr[right : end + 1])
        arr[start : end + 1] = merged

    # 4. Quick sort (Lomuto partition, last item as pivot)
    def quick_sort(self) -> list[int]:
        self._quick_sort(self.data, 0, len(self.data) - 1)
        return self.data

    def _quick_sort(self, arr: list[int], start: int, end: int) -> None:
        if start >= end:
            return

        pivot_index = self._partition(arr, start, end)
        self._quick_sort(arr, start, pivot_index - 1)
        self._quick_sort(arr, pivot_index + 1, end)

    def _partition(self, arr: list[int], start: int, end: int) -> int:
        pivot = arr[end]
        i = start

        for j in range(start, end):
            if arr[j] < pivot:
                arr[i], arr[j] = arr[j], arr[i]
                i += 1

        arr[i], arr[end] = arr[end], arr[i]
        return i

    # 5. Palindrome (index based, no slicing)
    def palindrome(self, text: str) -> bool:
        return self._palindrome(text, 0, len(text) - 1)

    def _palindrome(self, text: str, left: int, right: int) -> bool:
        if left >= right:
            return True
        if text[left] != text[right]:
            return False

        return self._palindrome(text, left + 1, right - 1)


# ruff: noqa: S101, T201, PLR2004
class _CountingRecursion(Recursion):
    """Counts total fib_recur calls and the deepest active call depth."""

    def __init__(self) -> None:
        super().__init__()
        self.calls: int = 0
        self.depth: int = 0
        self.max_depth: int = 0

    def fib_recur(self, n: int) -> int:
        self.calls += 1
        self.depth += 1
        self.max_depth = max(self.max_depth, self.depth)
        try:
            return super().fib_recur(n)
        finally:
            self.depth -= 1


def test_fibonacci() -> None:
    r = Recursion()

    print("n  predicted  iter  recur  memo")
    for n, expected in [(1, 1), (2, 1), (3, 2), (5, 5), (6, 8), (10, 55)]:
        actual = (r.fib_iter(n), r.fib_recur(n), r.fib_memo(n))
        print(f"{n:<2} {expected:<10} {actual[0]:<5} {actual[1]:<6} {actual[2]}")
        assert actual == (expected, expected, expected)
    print("PASS: fibonacci values (iterative, recursive, memoised agree)")

    for n in (0, -1, -10):
        for name, fn in (
            ("fib_iter", r.fib_iter),
            ("fib_recur", r.fib_recur),
            ("fib_memo", r.fib_memo),
        ):
            try:
                _ = fn(n)
                print(f"FAIL: {name}({n}) did not raise ValueError")
                raise AssertionError
            except ValueError:
                pass
    print("PASS: n < 1 raises ValueError")

    # Loop iterations, total recursive calls and maximum depth are different
    # quantities: calls = 2 * F(n) - 1 (exponential), depth = n - 1 (linear),
    # iterations = n - 2 (linear)
    print("\nn  loop iterations  recursive calls  max depth")
    for n in (5, 10, 15, 20):
        counter = _CountingRecursion()
        _ = counter.fib_recur(n)
        iterations = max(n - 2, 0)
        print(f"{n:<2} {iterations:<16} {counter.calls:<16} {counter.max_depth}")
        assert counter.calls == 2 * r.fib_iter(n) - 1
        assert counter.max_depth == n - 1
    print("PASS: call counts and depth match 2*F(n)-1 and n-1")

    # Memoisation removes the repeated work and handles large n
    assert r.fib_memo(90) == r.fib_iter(90)
    print("PASS: fib_memo(90) matches fib_iter(90)")


def test_gcd() -> None:
    r = Recursion()

    cases = [
        ((12, 12), 12),
        ((27, 18), 9),
        ((18, 27), 9),
        ((28, 19), 1),
        ((7, 1), 1),
        ((1, 7), 1),
        ((48, 36), 12),
    ]
    for (n, m), expected in cases:
        actual = r.gcd(n, m)
        print(f"gcd{(n, m)}: expected={expected} actual={actual}")
        assert actual == expected
    print("PASS: gcd values")

    for n, m in [(0, 5), (5, 0), (-3, 6), (6, -3), (0, 0)]:
        try:
            _ = r.gcd(n, m)
            print(f"FAIL: gcd({n}, {m}) did not raise ValueError")
            raise AssertionError
        except ValueError:
            pass
    print("PASS: zero and negative inputs raise ValueError")

    # gcd(k, 1) needs about k calls: O(k) time and O(k) call-stack space
    for k in (1, 5, 10, 50, 200):
        calls = 0

        class Counter(Recursion):
            def gcd(self, n: int, m: int) -> int:
                nonlocal calls
                calls += 1
                return super().gcd(n, m)

        assert Counter().gcd(k, 1) == 1
        print(f"gcd({k}, 1): {calls} calls")
        assert calls == k
    print("PASS: gcd(k, 1) takes k calls")


def _sort_cases() -> list[tuple[str, list[int]]]:
    return [
        ("empty", []),
        ("one item", [1]),
        ("odd length", [5, 2, 9, 1, 7]),
        ("even length", [6, 3, 5, 2]),
        ("ascending", [1, 2, 3, 4, 5, 6]),
        ("descending", [6, 5, 4, 3, 2, 1]),
        ("duplicates", [4, 2, 4, 1, 2, 4]),
        ("negatives", [3, -1, -7, 0, 2, -1]),
        ("all equal", [5, 5, 5, 5, 5]),
    ]


def _check_sort(label: str, method: str) -> None:
    r = Recursion()
    for name, original in _sort_cases():
        r.data = original.copy()  # restore a fresh copy for each method
        actual = getattr(r, method)()
        expected = sorted(original)
        print(f"{label} {name}: input={original} expected={expected} actual={actual}")
        assert actual == expected
        assert len(actual) == len(original)  # no duplicates lost

    for max_size in (10, 50, 100):
        r = Recursion(max_size)
        r.initialise()
        original = r.data.copy()
        actual = getattr(r, method)()
        assert actual == sorted(original)
    print(f"PASS: {label}")


def test_merge_sort() -> None:
    # Plan from the worksheet: [6, 3, 5, 2]
    #   merge 1: [6] + [3]   -> [3, 6]
    #   merge 2: [5] + [2]   -> [2, 5]
    #   merge 3: [3, 6] + [2, 5] -> [2, 3, 5, 6]
    r = Recursion()
    r.data = [6, 3, 5, 2]
    assert r.merge_sort() == [2, 3, 5, 6]
    print("PASS: merge sort trace [6, 3, 5, 2]")

    _check_sort("merge sort", "merge_sort")


def test_quick_sort() -> None:
    # One partition: [5, 2, 4, 1, 3] with pivot 3
    #   j=0: 5 !< 3                  i=0 [5, 2, 4, 1, 3]
    #   j=1: swap 5,2                i=1 [2, 5, 4, 1, 3]
    #   j=2: 4 !< 3                  i=1 [2, 5, 4, 1, 3]
    #   j=3: swap 5,1                i=2 [2, 1, 4, 5, 3]
    #   pivot swap with arr[2]       i=2 [2, 1, 3, 5, 4]
    r = Recursion()
    arr = [5, 2, 4, 1, 3]
    pivot_index = r._partition(arr, 0, len(arr) - 1)  # noqa: SLF001
    print(f"partition [5, 2, 4, 1, 3] -> {arr}, pivot index {pivot_index}")
    assert pivot_index == 2
    assert arr == [2, 1, 3, 5, 4]
    print("PASS: partition trace")

    _check_sort("quick sort", "quick_sort")

    # Both sorts must agree on the same original list
    r = Recursion(100)
    r.initialise()
    original = r.data.copy()
    merged = r.merge_sort()
    r.data = original.copy()
    quick = r.quick_sort()
    assert merged == quick == sorted(original)
    print("PASS: merge sort and quick sort agree")


def test_palindrome() -> None:
    r = Recursion()

    cases = [
        ("", True),
        ("a", True),
        ("aa", True),
        ("ab", False),
        ("hannah", True),
        ("Hannah", False),  # case sensitive: 'H' != 'h'
        ("!_asddsa_!", True),
        ("abcdba", False),
        ("12321", True),  # odd length
        ("abca", False),  # mismatch at the first comparison
        ("abcdeba", False),  # mismatch near the centre
        ("racecar", True),
    ]
    for text, expected in cases:
        actual = r.palindrome(text)
        print(f"palindrome({text!r}): expected={expected} actual={actual}")
        assert actual == expected
    print("PASS: palindrome cases")

    # Repeated calls must not depend on previous inputs
    assert r.palindrome("abca") is False
    assert r.palindrome("hannah") is True
    assert r.palindrome("hannah") is True
    print("PASS: repeated calls independent")
