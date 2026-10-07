from array_queue import Queue
from stack import Stack

_PAIRS = {")": "(", "]": "[", "}": "{"}
_OPENERS = set(_PAIRS.values())


def is_valid_stack(text: str) -> bool:
    stack = Stack(capacity=max(len(text), 1))

    for char in text:
        if char in _OPENERS:
            stack.push(char)
        elif char in _PAIRS:
            has_opener = stack.length() > 0
            matches_opener = has_opener and stack.pop() == _PAIRS[char]
            if not matches_opener:
                return False

    return stack.length() == 0


brackets_valid = is_valid_stack


def is_valid_queue(text: str) -> bool:
    brackets = [c for c in text if c in _OPENERS or c in _PAIRS]
    queue = Queue(capacity=max(len(brackets), 1))
    for char in brackets:
        queue.enqueue(char)

    while queue.length() > 0:
        removed = False
        remaining = queue.length()
        while remaining > 0:
            char = queue.dequeue()
            remaining -= 1

            if (
                remaining > 0
                and char in _OPENERS
                and _PAIRS.get(str(queue.peek())) == char
            ):
                _ = queue.dequeue()
                remaining -= 1
                removed = True
            else:
                queue.enqueue(char)

        if not removed:
            return False

    return True


# ruff: noqa: S101, T201
def test_valid_brackets() -> None:
    cases = [
        ("(abc)", True),
        ("ds", True),
        ("[a{b]c}", False),
        ("", True),
        ("()[]{}", True),
        ("{[()]}", True),
        ("((", False),
        ("))", False),
        ("(]", False),
        ("([)]", False),
        ("a(b[c]d)e", True),
        ("([)]", False),
        (")", False),
        ("{a[b(c)d]e}", True),
        ("((((((" + "))))))", True),
        (")(", False),
    ]

    for text, expected in cases:
        for name, func in (("stack", is_valid_stack), ("queue", is_valid_queue)):
            actual = func(text)
            print(f"{name}: {text!r} expected={expected} actual={actual}")
            assert actual == expected
    print("PASS: valid brackets (stack and queue)")

    # Consecutive calls: state from an invalid call must not leak into the next
    first = brackets_valid("(")
    second = brackets_valid("ds")
    print(f'brackets_valid("(") = {first}, brackets_valid("ds") = {second}')
    assert first is False
    assert second is True
    print("PASS: consecutive calls")
