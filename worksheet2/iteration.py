from random import sample
from typing import override


class Iteration:
    def __init__(self, max_size: int = 100) -> None:
        self.data: list[int] = []
        self.max_size: int = max_size

        # Instrumentation used by the tests and analysis.
        # Each method resets the counters it updates.
        self.comparisons: int = 0  # comparisons between list values (sorting)
        self.swaps: int = 0
        self.shifts: int = 0
        self.inspected: int = 0  # items read and compared with the target (searching)
        self.max_active_calls: int = 0  # deepest recursion (recursive search)
        self._active_calls: int = 0

    def initialise(self) -> None:
        self.data = sample(range(1, 3 * self.max_size), self.max_size)

    @override
    def __str__(self) -> str:
        return str(self.data)

    # ------------------------------------------------------------------
    # Exercise 1: Selection Sort
    # ------------------------------------------------------------------
    def selection_sort(self) -> list[int]:
        # For descending order, only the comparison changes: look for the
        # maximum (`>`) instead of the minimum (`<`).
        self.comparisons = 0
        self.swaps = 0

        n = len(self.data)
        for i in range(n - 1):
            ind_min = i
            for j in range(i + 1, n):
                self.comparisons += 1
                if self.data[j] < self.data[ind_min]:
                    ind_min = j

            if ind_min != i:
                self.data[i], self.data[ind_min] = self.data[ind_min], self.data[i]
                self.swaps += 1

        return self.data

    # ------------------------------------------------------------------
    # Exercise 2: Insertion Sort
    # ------------------------------------------------------------------
    def insertion_sort(self) -> list[int]:
        self.comparisons = 0
        self.shifts = 0

        for i in range(1, len(self.data)):
            current = self.data[i]
            j = i - 1

            # Shift larger items right; stop at the start of the list or at the
            # first item that is not larger (keeps equal items in order).
            while j >= 0:
                self.comparisons += 1
                if self.data[j] <= current:
                    break
                self.data[j + 1] = self.data[j]
                self.shifts += 1
                j -= 1

            self.data[j + 1] = current

        return self.data

    # ------------------------------------------------------------------
    # Exercise 3: Bubble Sort
    # ------------------------------------------------------------------
    def bubble_sort(self, early_stop: bool = True) -> list[int]:
        self.comparisons = 0
        self.swaps = 0

        n = len(self.data)
        # After each pass the largest remaining item is at index `last`,
        # so the next pass only needs to compare pairs up to `last - 1`.
        for last in range(n - 1, 0, -1):
            swapped = False
            for j in range(last):
                self.comparisons += 1
                if self.data[j] > self.data[j + 1]:
                    self.data[j], self.data[j + 1] = self.data[j + 1], self.data[j]
                    self.swaps += 1
                    swapped = True

            if early_stop and not swapped:
                break

        return self.data

    # ------------------------------------------------------------------
    # Exercise 4: Linear Search
    # ------------------------------------------------------------------
    def linear_search(self, item: int) -> int:
        self.inspected = 0

        for i in range(len(self.data)):
            self.inspected += 1
            if self.data[i] == item:
                return i

        raise ValueError

    # ------------------------------------------------------------------
    # Exercise 5: Binary Search (iterative)
    # ------------------------------------------------------------------
    def binary_search_iter(self, item: int) -> int:
        self.inspected = 0

        start = 0
        end = len(self.data) - 1
        while start <= end:
            mid = (start + end) // 2
            self.inspected += 1
            if self.data[mid] == item:
                return mid
            if self.data[mid] < item:
                start = mid + 1
            else:
                end = mid - 1

        raise ValueError

    # ------------------------------------------------------------------
    # Exercise 6: Binary Search (recursive)
    # ------------------------------------------------------------------
    def binary_search_recur(self, item: int) -> int:
        self.inspected = 0
        self.max_active_calls = 0
        self._active_calls = 0
        return self._binary_search_recur(self.data, 0, len(self.data) - 1, item)

    def _binary_search_recur(self, arr: list[int], start: int, end: int, item: int) -> int:
        self._active_calls += 1
        self.max_active_calls = max(self.max_active_calls, self._active_calls)
        try:
            if start > end:
                raise ValueError

            mid = (start + end) // 2
            self.inspected += 1
            if arr[mid] == item:
                return mid
            if arr[mid] < item:
                return self._binary_search_recur(arr, mid + 1, end, item)
            return self._binary_search_recur(arr, start, mid - 1, item)
        finally:
            self._active_calls -= 1

    # ------------------------------------------------------------------
    # Exercise 7 (Advanced): Ternary Search
    # ------------------------------------------------------------------
    def ternary_search(self, item: int) -> int:
        self.inspected = 0

        start = 0
        end = len(self.data) - 1
        while start <= end:
            third = (end - start) // 3
            mid1 = start + third
            mid2 = end - third

            self.inspected += 1
            if self.data[mid1] == item:
                return mid1
            if item < self.data[mid1]:
                end = mid1 - 1
                continue
            if mid2 == mid1:  # one item left and it did not match
                break

            self.inspected += 1
            if self.data[mid2] == item:
                return mid2
            if item < self.data[mid2]:
                start = mid1 + 1
                end = mid2 - 1
            else:
                start = mid2 + 1

        raise ValueError
