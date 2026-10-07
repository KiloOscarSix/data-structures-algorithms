from array_queue import Queue
from stack import Stack


def remove_duplicates_stack(s: str) -> str:
    stack = Stack(capacity=len(s))

    for ch in s:
        if stack.length() > 0 and stack.peek() == ch:
            _ = stack.pop()
        else:
            stack.push(ch)

    # Popping reverses the order, so move everything onto a second stack
    # to reverse it back
    reversed_stack = Stack(capacity=stack.length())
    while stack.length() > 0:
        reversed_stack.push(stack.pop())

    result = ""
    while reversed_stack.length() > 0:
        result += str(reversed_stack.pop())
    return result


def remove_duplicates_queue(s: str) -> str:
    capacity = max(len(s), 1)
    current = Queue(capacity)
    for ch in s:
        current.enqueue(ch)

    removed = True
    while removed:
        removed = False
        following = Queue(capacity)
        pending: object = None  # last kept character not yet enqueued

        while current.length() > 0:
            ch = current.dequeue()
            if pending is None:
                pending = ch
            elif pending == ch:
                pending = None  # drop both
                removed = True
            else:
                following.enqueue(pending)
                pending = ch

        if pending is not None:
            following.enqueue(pending)
        current = following

    result = ""
    while current.length() > 0:
        result += str(current.dequeue())
    return result


# ruff: noqa: S101, T201
def test_remove_duplicates() -> None:
    cases = [
        ("abbccd", "ad"),
        ("dsallasg", "dg"),
        ("abccbadd", ""),
        ("", ""),
        ("a", "a"),
        ("abc", "abc"),
        ("aa", ""),
        ("aaa", "a"),
        ("abba", ""),
    ]
    for s, expected in cases:
        for name, fn in (
            ("stack", remove_duplicates_stack),
            ("queue", remove_duplicates_queue),
        ):
            actual = fn(s)
            print(f"{name}: {s!r} expected={expected!r} actual={actual!r}")
            assert actual == expected
    print("PASS: remove duplicates (stack and queue)")
