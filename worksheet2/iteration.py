from random import sample  # noqa: CPY001


class Iteration:
    def __init__(self, max_size: int = 100) -> None:
        self.data: list[int] = []
        self.max_size: int = max_size

    def initialise(self) -> None:
        self.data = sample(range(1, 3 * self.max_size), self.max_size)

    def __str__(self) -> str:
        return str(self.data)

    def selection_sort(self) -> list[int]:
        n = len(self.data)
        for i in range(n - 1):
            ind_min = i
            for j in range(i + 1, n):
                if self.data[j] < self.data[ind_min]:
                    ind_min = j

            if ind_min != i:
                self.data[ind_min], self.data[i] = self.data[i], self.data[ind_min]

        return self.data
