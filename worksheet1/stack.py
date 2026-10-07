from typing import override


class Stack:
    def __init__(self, capacity: int = 5) -> None:
        if capacity < 0:
            raise ValueError

        self._data: list[object] = [None] * capacity
        self._top: int = -1
        self._capacity: int = capacity

    def push(self, new_data: object) -> None:
        if self._top + 1 >= self._capacity:
            raise OverflowError

        self._top += 1
        self._data[self._top] = new_data

    def pop(self) -> object:
        if self._top < 0:
            raise IndexError

        item = self._data[self._top]
        self._data[self._top] = None
        self._top -= 1
        return item

    def peek(self) -> object:
        if self._top < 0:
            raise IndexError

        return self._data[self._top]

    def length(self) -> int:
        return self._top + 1

    @override
    def __str__(self) -> str:
        return str(self._data[: self._top + 1])


# ruff: noqa: S101, T201, PLR2004, SLF001
# pyright: reportPrivateUsage=false
def test_stack() -> None:  # noqa: PLR0915
    # Normal LIFO order
    stack = Stack()

    stack.push("a")
    stack.push("b")
    stack.push("c")

    assert stack.pop() == "c"
    assert stack.pop() == "b"
    assert stack.pop() == "a"
    print("PASS: normal LIFO order")

    # Peek without removal
    stack = Stack()

    stack.push("a")
    stack.push("b")

    assert stack.peek() == "b"
    assert stack.length() == 2
    print("PASS: peek does not remove item")

    # Removing the last item
    stack = Stack()

    stack.push("only")
    assert stack.pop() == "only"
    assert stack.length() == 0
    print("PASS: removing the last item")

    # Empty pop
    stack = Stack()

    try:
        _ = stack.pop()
        print("FAIL: empty pop did not raise IndexError")
    except IndexError:
        print("PASS: empty pop raises IndexError")

    # Empty peek
    try:
        _ = stack.peek()
        print("FAIL: empty peek did not raise IndexError")
    except IndexError:
        print("PASS: empty peek raises IndexError")

    # Capacity 3: fill stack, then attempt fourth push
    stack = Stack(capacity=3)

    stack.push(1)
    stack.push(2)
    stack.push(3)

    before = stack._data.copy()

    try:
        stack.push(4)
        print("FAIL: fourth push did not raise OverflowError")
    except OverflowError:
        print("PASS: fourth push raises OverflowError")

    # Verify stack is unchanged
    assert stack._data == before
    assert stack.length() == 3
    assert stack.peek() == 3
    print("PASS: stack unchanged after failed push")

    # Boundary test: initial state -> operation -> expected vs actual
    stack = Stack(capacity=3)

    expected = {
        "data": ["x", None, None],
        "top": 0,
        "length": 1,
    }

    stack.push("x")

    actual = {
        "data": stack._data,
        "top": stack._top,
        "length": stack.length(),
    }

    print("\nBoundary test:")
    print("Initial state: data=[], top=-1, length=0")
    print("Operation: push('x')")
    print(f"Expected: {expected}")
    print(f"Actual:   {actual}")

    assert actual == expected
    print("PASS: boundary test")
