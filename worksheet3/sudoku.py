class Sudoku:
    def __init__(self, board: list[list[int]]) -> None:
        self.board: list[list[int]] = [row.copy() for row in board]
        self.size: int = 9
        # Placements on the current path, as (row, col, num); popped on backtrack
        self.stack: list[tuple[int, int, int]] = []

    def is_valid(self, row: int, col: int, num: int) -> bool:
        for i in range(self.size):
            if self.board[row][i] == num or self.board[i][col] == num:
                return False

        box_row = row - row % 3
        box_col = col - col % 3
        for r in range(box_row, box_row + 3):
            for c in range(box_col, box_col + 3):
                if self.board[r][c] == num:
                    return False

        return True

    def find_next_empty(self) -> tuple[int | None, int | None]:
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] == 0:
                    return row, col
        return None, None

    def solve(self) -> bool:
        row, col = self.find_next_empty()
        if row is None or col is None:
            return True  # no empty cells left: solved

        for num in range(1, self.size + 1):
            if self.is_valid(row, col, num):
                self.board[row][col] = num
                self.stack.append((row, col, num))

                if self.solve():
                    return True

                # Dead end: undo this placement and try the next digit
                _ = self.stack.pop()
                self.board[row][col] = 0

        return False

    def __str__(self) -> str:
        return "\n".join(" ".join(str(x) for x in row) for row in self.board)


PUZZLE = [
    [1, 0, 7, 5, 0, 0, 0, 0, 8],
    [0, 5, 0, 0, 0, 0, 7, 0, 0],
    [0, 0, 0, 0, 0, 1, 5, 6, 0],
    [0, 9, 3, 8, 1, 0, 0, 0, 0],
    [5, 0, 0, 4, 0, 7, 0, 0, 2],
    [0, 0, 0, 0, 2, 6, 9, 1, 0],
    [0, 1, 4, 2, 0, 0, 0, 0, 0],
    [0, 0, 9, 0, 0, 0, 0, 5, 0],
    [6, 0, 0, 0, 0, 4, 8, 0, 9],
]


# ruff: noqa: S101, T201
def _is_complete(board: list[list[int]]) -> bool:
    digits = set(range(1, 10))
    rows = all(set(row) == digits for row in board)
    cols = all({board[r][c] for r in range(9)} == digits for c in range(9))
    boxes = all(
        {board[r][c] for r in range(br, br + 3) for c in range(bc, bc + 3)} == digits
        for br in (0, 3, 6)
        for bc in (0, 3, 6)
    )
    return rows and cols and boxes


def test_sudoku() -> None:
    sudoku = Sudoku(PUZZLE)
    assert sudoku.board is not PUZZLE
    assert sudoku.board == PUZZLE  # constructor copies, original untouched

    # is_valid and find_next_empty on the initial grid
    assert sudoku.find_next_empty() == (0, 1)
    assert not sudoku.is_valid(0, 1, 1)  # 1 already in row 0
    assert not sudoku.is_valid(0, 1, 5)  # 5 already in column 1
    assert not sudoku.is_valid(0, 1, 9)  # 9 already in column 1
    assert sudoku.is_valid(0, 1, 2)
    print("PASS: is_valid and find_next_empty")

    print("\nPuzzle:")
    print(sudoku)
    assert sudoku.solve()
    print("\nSolution:")
    print(sudoku)

    assert _is_complete(sudoku.board)
    for r in range(9):
        for c in range(9):
            if PUZZLE[r][c] != 0:
                assert sudoku.board[r][c] == PUZZLE[r][c]  # givens preserved
    assert sudoku.find_next_empty() == (None, None)
    assert len(sudoku.stack) == sum(row.count(0) for row in PUZZLE)
    assert PUZZLE[0][1] == 0  # original puzzle not mutated
    print("PASS: sudoku solved")

    # Unsolvable grid: row 0 needs a 9 at (0, 8) but column 8 already has one
    bad = [row.copy() for row in PUZZLE]
    bad[0] = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    bad[1][8] = 9
    unsolvable = Sudoku(bad)
    assert unsolvable.solve() is False
    assert unsolvable.board == bad  # fully backtracked, nothing left behind
    print("PASS: unsolvable grid returns False and is restored")
