class Queue:
    def __init__(self, capacity: int = 5) -> None:
        if capacity <= 0:
            raise ValueError

        self._data: list[object] = [None] * capacity
        self.capacity: int = capacity
        self._head: int = 0
        self._tail: int = 0
        self._size: int = 0

    def enqueue(self, item: object) -> None:
        if self.is_full():
            raise OverflowError

        self._data[self._tail] = item
        self._tail = (self._tail + 1) % self.capacity
        self._size += 1

    def dequeue(self) -> object:
        if self.is_empty():
            raise IndexError

        item = self._data[self._head]
        self._data[self._head] = None
        self._head = (self._head + 1) % self.capacity
        self._size -= 1
        return item

    def peek(self) -> object:
        if self.is_empty():
            raise IndexError

        return self._data[self._head]

    def length(self) -> int:
        return self._size

    def is_empty(self) -> bool:
        return self._size == 0

    def is_full(self) -> bool:
        return self._size == self.capacity


# ruff: noqa: S101, T201, PLR2004
# pyright: reportPrivateUsage=false
def test_queue() -> None:
    q = Queue(3)

    # FIFO order
    q.enqueue("a")
    q.enqueue("b")
    q.enqueue("c")
    assert q.dequeue() == "a"
    assert q.dequeue() == "b"
    assert q.dequeue() == "c"
    print("FIFO order: OK")

    # Peek without removal
    q.enqueue("a")
    assert q.peek() == "a"
    assert q.length() == 1
    assert q.dequeue() == "a"
    print("Peek without removal: OK")

    # One-item queue
    q.enqueue(42)
    assert q.length() == 1
    assert q.peek() == 42
    assert q.dequeue() == 42
    print("One-item queue: OK")

    # Empty dequeue
    try:
        _ = q.dequeue()
    except IndexError:
        print("Empty dequeue: OK")

    # Empty peek
    try:
        _ = q.peek()
    except IndexError:
        print("Empty peek: OK")

    # Overflow
    q.enqueue(1)
    q.enqueue(2)
    q.enqueue(3)
    assert q.length() == 3

    try:
        q.enqueue(4)
    except OverflowError:
        print("Overflow: OK")

    # Remove one, then insert one
    assert q.dequeue() == 1
    assert q.length() == 2

    q.enqueue(4)
    assert q.length() == 3

    assert q.dequeue() == 2
    assert q.dequeue() == 3
    assert q.dequeue() == 4
    print("Remove and reinsert: OK")

    # isEmpty / isFull, including after head and tail wrap around
    q = Queue(3)
    assert q.is_empty()
    assert not q.is_full()
    q.enqueue(1)
    assert not q.is_empty()
    assert not q.is_full()
    q.enqueue(2)
    q.enqueue(3)
    assert q.is_full()
    assert not q.is_empty()
    assert q.dequeue() == 1
    assert not q.is_full()
    q.enqueue(4)
    assert q._tail == q._head
    assert q.is_full()
    assert not q.is_empty()
    for _ in range(3):
        _ = q.dequeue()
    assert q._tail == q._head
    assert q.is_empty()
    assert not q.is_full()
    print("is_empty / is_full: OK")

    print("All tests passed")
