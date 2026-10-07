from array_queue import Queue
from stack import Stack


def reverse_queue(q: Queue) -> None:
    stack = Stack(capacity=q.length())

    while q.length() > 0:
        stack.push(q.dequeue())

    while stack.length() > 0:
        q.enqueue(stack.pop())


# ruff: noqa: S101, T201
def _drain(q: Queue) -> list[object]:
    items: list[object] = []
    while q.length() > 0:
        items.append(q.dequeue())
    return items


def _check(name: str, items: list[object]) -> None:
    q = Queue(max(len(items), 1))
    for item in items:
        q.enqueue(item)

    expected = items[::-1]
    reverse_queue(q)
    actual = _drain(q)

    print(f"{name}: input={items} expected={expected} actual={actual}")
    assert actual == expected
    print(f"PASS: {name}")


def test_reverse_queue() -> None:
    _check("empty queue", [])
    _check("one item", [1])
    _check("[1, 2, 3, 4, 5]", [1, 2, 3, 4, 5])
    _check("repeated values", [2, 2, 3])
    _check("six items (exceeds default Stack capacity 5)", [1, 2, 3, 4, 5, 6])
