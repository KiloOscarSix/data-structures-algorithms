"""QUIZ 2 CHEAT SHEET: SINGLY LINKED LISTS (Workshop 6 / Worksheet 4).

Run everything:  python3 main_linked_list.py      (from inside quiz2/)

CORE IDEAS
- Node = data + next. head is just a reference; None = empty list / end of chain.
- Only a head reference -> no backwards links -> must walk from head.
- Insert after p:  q.next = p.next  THEN  p.next = q   (order matters! swap = lost suffix)
- Delete: find the PREDECESSOR (prev), then prev.next = prev.next.next.
  Locate is O(n); the relink/bypass is O(1) once prev is known.
- Delete cases: absent, head (head = head.next), middle, tail. Empty list -> no-op.
- Insert cases: empty, at head, at tail, middle.
- Dummy node trick: dummy.next = head gives even the head a predecessor, so no
  head special case. Assign head = dummy.next at the end.
- Insert at head repeatedly -> list ends up in REVERSE of input order.
- Stack on SLL: top at head, push/pop O(1). Queue on SLL: keep head + tail.
- Doubly linked: O(1) delete given the node, but more memory per node.

COMPLEXITY (head reference only, n nodes)
  op                         time        aux space
  insert at head             O(1)        O(1)
  append at tail (no tail)   O(n)        O(1)   walk to node whose next is None
  append with tail ref       O(1)        O(1)
  search / delete by value   O(n)        O(1)
  traverse / len             O(n)        O(1)
  bubble sort (swap data)    best O(n) (sorted: 1 pass, no swaps), worst O(n^2), O(1)
  reverse (prev/cur/next)    O(n)        O(1)   three references
  remove n-th from end       O(L)        O(1)   2-pass ~2L-n steps; 2-pointer 1 pass
  merge 2 sorted (a, b)      O(a+b)      O(1) work + O(a+b) new nodes (local tail)
  merge via insert() loop    O((a+b)^2)  each insert walks the growing result
  merge N lists pairwise     O(T log N)  (T total values) vs one-at-a-time O(T*N)

WORKSHEET ANSWERS TO REMEMBER
- Bubble sort: ONE ordered pair doesn't mean sorted ([3,4,1,2]); stop only after a
  full pass with no swaps. [3,4,1,2] passes: [3,1,2,4] s=2, [1,2,3,4] s=2, s=0.
- swap_data changes .data only; no next references change.
- Reverse: save current.next FIRST, else the unprocessed suffix is unreachable.
  head = prev AFTER the loop (old tail only known when current is None).
  Trace [A,B,C]: (prev,cur) = (A,B), (B,C), (C,None).
- n-th from end is at position L - n + 1 (predecessor at L - n).
  Two-pointer: move first n steps from dummy, then move both until first.next is None;
  second is the predecessor. n=4 on [1..5]: second ends at 1, 1.next becomes 3.
- Test reversal by comparing node identities (nodes()), not just values.
- Merge: ties take list1 (stable). When one list ends, copy the rest of the other.

SORTED vs UNSORTED: SLL vs ARRAY (other student's quiz: "efficiency in sorted and
unsorted SLL", "linear searching")
  operation              unsorted SLL      sorted SLL              unsorted array  sorted array
  search                 O(n) linear       O(n) linear (early      O(n)            O(log n) binary
                                           exit once data > x)
  insert                 O(1) at head      O(n) find spot,         O(1) append     O(n) shift
                                           O(1) relink
  delete by value        O(n) find,        O(n) find (early exit), O(n)            O(n) shift
                         O(1) relink       O(1) relink
  find min               O(n)              O(1) = head             O(n)            O(1) a[0]
  find max               O(n)              O(n) walk to tail       O(n)            O(1) a[-1]
                                           (O(1) with tail ref)
  remove duplicates      O(n^2) (or set)   O(n) adjacent only      -               -
  merge two lists        sort first        O(a+b)                  -               O(a+b)
  KEY POINT: binary search does NOT help a linked list. No index access, so reaching
  the middle costs O(n) every time: still O(n) overall (worse constants). Sorting a
  SLL only buys early exit on a miss and O(1) min, at the cost of O(n) inserts.
  Linear search cost: best 1 comparison (at head), worst n (last/absent),
  average (n+1)/2 if present. Sorted early exit: an absent value stops at the first
  bigger node, but the worst case is still O(n).

QUIZ VARIANTS (all tested in test_variants): search "VARIANTS" below.
insert_at_head, insert_sorted, insert_at, delete_at, delete_all,
remove_duplicates_sorted, index_of, get, middle, has_cycle, max_value, sum_values,
reverse_recursive, equals, copy, interleave,
linear_search, linear_search_count, search_sorted, search_sorted_count,
count_occurrences, all_positions, last_index_of, find_min_sorted, is_sorted,
insert_unsorted, sum_at_positions.
"""

# No imports: plain Python only (no libraries in the quiz).


class Node:
    def __init__(self, data: int) -> None:
        self.data: int = data
        self.next: Node | None = None


class SinglyLinkedList:
    def __init__(self, values: list[int] | tuple[int, ...] = ()) -> None:
        self.head: Node | None = None
        for value in values:
            self.insert(value)

    # Exercise 1: CRUD
    def insert(self, data: int) -> None:
        """Append to the tail. O(n): walk to the node whose next is None."""
        node = Node(data)
        if self.head is None:
            self.head = node
            return
        current = self.head
        while current.next is not None:
            current = current.next
        current.next = node

    def search(self, data: int) -> bool:
        current = self.head
        while current is not None:
            if current.data == data:
                return True
            current = current.next
        return False

    def delete(self, data: int) -> None:
        """Remove the first node holding data; do nothing if it is absent."""
        if self.head is None:
            return
        if self.head.data == data:
            self.head = self.head.next
            return
        prev = self.head
        while prev.next is not None:
            if prev.next.data == data:
                prev.next = prev.next.next  # bypass: O(1) once prev is known
                return
            prev = prev.next

    def traverse(self) -> None:
        current = self.head
        while current is not None:
            print(current.data)
            current = current.next

    def __iter__(self):  # generator: yields each value head -> tail
        current = self.head
        while current is not None:
            yield current.data
            current = current.next

    def __len__(self) -> int:
        return sum(1 for _ in self)

    def __str__(self) -> str:
        return " -> ".join(["head", *(str(value) for value in self)])

    def nodes(self) -> list[Node]:
        """Node objects in order, used by tests to check identity, not values."""
        result: list[Node] = []
        current = self.head
        while current is not None:
            result.append(current)
            current = current.next
        return result

    # Exercise 2: sort
    @staticmethod
    def swap_data(a: Node, b: Node) -> None:
        a.data, b.data = b.data, a.data

    def bubble_sort(self) -> None:
        if self.head is None:
            return
        swapped = True
        while swapped:
            swapped = False
            current = self.head
            while current.next is not None:
                if current.data > current.next.data:
                    self.swap_data(current, current.next)
                    swapped = True
                current = current.next

    def bubble_sort_trace(self) -> list[tuple[list[int], int]]:
        """bubble_sort, recording (values after pass, swaps in pass) per pass."""
        trace: list[tuple[list[int], int]] = []
        if self.head is None:
            return trace
        swaps = -1
        while swaps != 0:
            swaps = 0
            current = self.head
            while current.next is not None:
                if current.data > current.next.data:
                    self.swap_data(current, current.next)
                    swaps += 1
                current = current.next
            trace.append((list(self), swaps))
        return trace

    # Exercise 3: reverse
    def reverse(self) -> None:
        prev: Node | None = None
        current = self.head
        while current is not None:
            saved_next = current.next  # save before redirecting, or the suffix is lost
            current.next = prev
            prev = current
            current = saved_next
        self.head = prev

    # Exercise 4: remove n-th from end
    def remove_nth_from_end(self, n: int) -> int:
        """Remove the n-th node from the end and return its value.

        Raises ValueError for n < 1 or n > length, leaving the list unchanged.
        """
        if n < 1:
            raise ValueError(n)
        dummy = Node(0)
        dummy.next = self.head
        first = second = dummy
        for _ in range(n):
            if first.next is None:
                raise ValueError(n)
            first = first.next
        while first.next is not None:
            first = first.next
            second = second.next
            assert second is not None  # second trails first by n links
        removed = second.next
        assert removed is not None
        second.next = removed.next
        self.head = dummy.next
        return removed.data

    # Exercise 5: merge two sorted lists
    def merge(self, other: SinglyLinkedList) -> SinglyLinkedList:
        """Return a new sorted list of fresh nodes; inputs are left unchanged."""
        return self.merge_trace(other)[0]

    def merge_trace(
        self, other: SinglyLinkedList
    ) -> tuple[SinglyLinkedList, list[tuple[str, int]]]:
        """merge, also recording (source, value) for each append step."""
        result = SinglyLinkedList()
        dummy = Node(0)
        tail = dummy  # local tail: each append is O(1)
        steps: list[tuple[str, int]] = []
        a, b = self.head, other.head
        while a is not None or b is not None:
            if b is None or (a is not None and a.data <= b.data):  # ties: list1
                assert a is not None
                source, value, a = "list1", a.data, a.next
            else:
                source, value, b = "list2", b.data, b.next
            tail.next = Node(value)
            tail = tail.next
            steps.append((source, value))
        result.head = dummy.next
        return result, steps

    # ================= VARIANTS (likely quiz twists, all tested) =================

    def insert_at_head(self, data: int) -> None:
        """O(1). new.next = head, then head = new."""
        node = Node(data)
        node.next = self.head
        self.head = node

    def insert_sorted(self, data: int) -> None:
        """Insert keeping ascending order. O(n). Dummy avoids the head special case."""
        dummy = Node(0)
        dummy.next = self.head
        prev = dummy
        while prev.next is not None and prev.next.data < data:
            prev = prev.next
        node = Node(data)
        node.next = prev.next  # 1) link new node to the rest FIRST
        prev.next = node  # 2) then point the predecessor at it
        self.head = dummy.next

    def insert_at(self, index: int, data: int) -> None:
        """Insert so the new node sits at position index (0 = head). O(n)."""
        if index < 0:
            raise IndexError(index)
        dummy = Node(0)
        dummy.next = self.head
        prev = dummy
        for _ in range(index):
            if prev.next is None:
                raise IndexError(index)
            prev = prev.next
        node = Node(data)
        node.next = prev.next
        prev.next = node
        self.head = dummy.next

    def delete_at(self, index: int) -> int:
        """Remove and return the value at position index (0 = head). O(n)."""
        if index < 0:
            raise IndexError(index)
        dummy = Node(0)
        dummy.next = self.head
        prev = dummy
        for _ in range(index):
            if prev.next is None:
                raise IndexError(index)
            prev = prev.next
        removed = prev.next
        if removed is None:
            raise IndexError(index)
        prev.next = removed.next
        self.head = dummy.next
        return removed.data

    def delete_all(self, data: int) -> int:
        """Remove EVERY node holding data; return how many. O(n)."""
        dummy = Node(0)
        dummy.next = self.head
        prev = dummy
        count = 0
        while prev.next is not None:
            if prev.next.data == data:
                prev.next = prev.next.next  # don't advance: check the new next too
                count += 1
            else:
                prev = prev.next
        self.head = dummy.next
        return count

    def remove_duplicates_sorted(self) -> None:
        """Sorted list: drop adjacent repeats in place. O(n) time, O(1) space."""
        current = self.head
        while current is not None and current.next is not None:
            if current.data == current.next.data:
                current.next = current.next.next
            else:
                current = current.next

    def index_of(self, data: int) -> int:
        """Position of the first match, or -1. O(n)."""
        for i, value in enumerate(self):
            if value == data:
                return i
        return -1

    def get(self, index: int) -> int:
        """Value at position index. O(n): no random access in a linked list."""
        for i, value in enumerate(self):
            if i == index:
                return value
        raise IndexError(index)

    def middle(self) -> int:
        """Middle value via slow/fast pointers (second middle if even). O(n)."""
        if self.head is None:
            raise ValueError("empty")
        slow = fast = self.head
        while fast is not None and fast.next is not None:
            assert slow.next is not None
            slow = slow.next
            fast = fast.next.next
        return slow.data

    def has_cycle(self) -> bool:
        """Floyd: slow moves 1, fast moves 2; they meet iff there is a cycle."""
        slow = fast = self.head
        while fast is not None and fast.next is not None:
            assert slow is not None
            slow = slow.next
            fast = fast.next.next
            if slow is fast:
                return True
        return False

    def max_value(self) -> int:
        if self.head is None:
            raise ValueError("empty")
        best = self.head.data
        current = self.head.next
        while current is not None:
            best = max(best, current.data)
            current = current.next
        return best

    def sum_values(self) -> int:
        total = 0
        current = self.head
        while current is not None:
            total += current.data
            current = current.next
        return total

    def reverse_recursive(self) -> None:
        """Recursive reverse. O(n) time but O(n) call stack (iterative is O(1))."""

        def rev(node: Node | None) -> Node | None:
            if node is None or node.next is None:
                return node  # new head = old tail
            new_head = rev(node.next)
            node.next.next = node  # the node after me now points back at me
            node.next = None
            return new_head

        self.head = rev(self.head)

    def equals(self, other: SinglyLinkedList) -> bool:
        """Same values, same order. O(n)."""
        a, b = self.head, other.head
        while a is not None and b is not None:
            if a.data != b.data:
                return False
            a, b = a.next, b.next
        return a is None and b is None  # both must end together

    def copy(self) -> SinglyLinkedList:
        """Deep copy with fresh nodes, O(n) via a local tail."""
        result = SinglyLinkedList()
        dummy = Node(0)
        tail = dummy
        for value in self:
            tail.next = Node(value)
            tail = tail.next
        result.head = dummy.next
        return result

    # ---------- Search / sorted-vs-unsorted variants (other student's quiz) ----------

    def linear_search(self, target: int) -> int:
        """Position (0-based) of the first match, else -1. O(n), O(1)."""
        position = 0
        current = self.head
        while current is not None:
            if current.data == target:
                return position
            current = current.next
            position += 1
        return -1

    def linear_search_count(self, target: int) -> tuple[bool, int]:
        """(found, comparisons made): shows best 1 / worst n."""
        comparisons = 0
        current = self.head
        while current is not None:
            comparisons += 1
            if current.data == target:
                return True, comparisons
            current = current.next
        return False, comparisons

    def search_sorted(self, target: int) -> bool:
        """Ascending list: stop early once data > target. Still O(n) worst."""
        current = self.head
        while current is not None and current.data <= target:
            if current.data == target:
                return True
            current = current.next
        return False

    def search_sorted_count(self, target: int) -> tuple[bool, int]:
        """search_sorted, also returning comparisons (to compare with unsorted)."""
        comparisons = 0
        current = self.head
        while current is not None:
            comparisons += 1
            if current.data == target:
                return True, comparisons
            if current.data > target:
                return False, comparisons  # early exit: everything after is bigger
            current = current.next
        return False, comparisons

    def count_occurrences(self, target: int) -> int:
        count = 0
        current = self.head
        while current is not None:
            if current.data == target:
                count += 1
            current = current.next
        return count

    def all_positions(self, target: int) -> list[int]:
        positions: list[int] = []
        position = 0
        current = self.head
        while current is not None:
            if current.data == target:
                positions.append(position)
            current = current.next
            position += 1
        return positions

    def last_index_of(self, target: int) -> int:
        """Must scan the whole list (can't walk backwards in a SLL)."""
        last = -1
        position = 0
        current = self.head
        while current is not None:
            if current.data == target:
                last = position
            current = current.next
            position += 1
        return last

    def find_min_sorted(self) -> int:
        """Sorted ascending: min is the head, O(1)."""
        if self.head is None:
            raise ValueError("empty")
        return self.head.data

    def is_sorted(self) -> bool:
        current = self.head
        while current is not None and current.next is not None:
            if current.data > current.next.data:
                return False
            current = current.next
        return True

    def insert_unsorted(self, data: int) -> None:
        """Order doesn't matter, so insert at head: O(1) (vs insert_sorted O(n))."""
        self.insert_at_head(data)

    def sum_at_positions(self, start: int, end: int) -> int:
        """Sum of values at positions start..end inclusive. O(n)."""
        total = 0
        position = 0
        current = self.head
        while current is not None and position <= end:
            if position >= start:
                total += current.data
            current = current.next
            position += 1
        return total

    def interleave(self, other: SinglyLinkedList) -> SinglyLinkedList:
        """New list a1, b1, a2, b2, ... then whatever is left. O(a+b)."""
        result = SinglyLinkedList()
        dummy = Node(0)
        tail = dummy
        a, b = self.head, other.head
        while a is not None or b is not None:
            if a is not None:
                tail.next = Node(a.data)
                tail, a = tail.next, a.next
            if b is not None:
                tail.next = Node(b.data)
                tail, b = tail.next, b.next
        result.head = dummy.next
        return result


# Exercise 6: merge N sorted lists
def merge_n(lists: list[SinglyLinkedList]) -> SinglyLinkedList:
    """Merge N >= 2 sorted lists by merging pairs, round by round.

    Each round halves the number of lists, so there are log2(N) rounds and
    each round touches every one of the T values: O(T log N) overall.
    """
    if len(lists) < 2:
        raise ValueError(len(lists))
    round_ = lists
    while len(round_) > 1:
        merged = [round_[i].merge(round_[i + 1]) for i in range(0, len(round_) - 1, 2)]
        if len(round_) % 2 == 1:
            merged.append(round_[-1].merge(SinglyLinkedList()))  # copy, keep inputs
        round_ = merged
    return round_[0]


# ruff: noqa: S101, T201, PLR2004
def test_crud() -> None:
    sll = SinglyLinkedList()
    print("Prediction table (start empty):")
    rows = [
        ("insert(10)", lambda: sll.insert(10), None, [10]),
        ("insert(20)", lambda: sll.insert(20), None, [10, 20]),
        ("insert(10)", lambda: sll.insert(10), None, [10, 20, 10]),
        ("search(20)", lambda: sll.search(20), True, [10, 20, 10]),
        ("delete(10)", lambda: sll.delete(10), None, [20, 10]),
        ("search(30)", lambda: sll.search(30), False, [20, 10]),
    ]
    for op, call, expected_return, expected_list in rows:
        actual = call()
        print(f"  {op:<11} return={actual!s:<5} list={list(sll)}")
        assert actual == expected_return
        assert list(sll) == expected_list
    print("PASS: CRUD prediction table")

    empty = SinglyLinkedList()
    assert not empty.search(1)
    empty.delete(1)
    assert empty.head is None
    print("PASS: search/delete on empty list")

    one = SinglyLinkedList([5])
    one.delete(5)
    assert one.head is None
    print("PASS: delete only node")

    sll = SinglyLinkedList([1, 2, 3, 4])
    sll.delete(9)
    assert list(sll) == [1, 2, 3, 4]
    sll.delete(1)
    assert list(sll) == [2, 3, 4]
    sll.delete(3)
    assert list(sll) == [2, 4]
    sll.delete(4)
    assert list(sll) == [2]
    print("PASS: delete absent, head, middle, tail")

    sll = SinglyLinkedList([7, 3, 7, 3])
    kept = sll.nodes()[1:]
    sll.delete(7)
    assert list(sll) == [3, 7, 3]
    assert sll.nodes() == kept
    print("PASS: deleting one duplicate keeps the other nodes and their order")

    # Boundary test: delete the tail of a two-node list
    sll = SinglyLinkedList([10, 20])
    print("\nBoundary test:")
    print(f"  Initial:  {sll}")
    print("  Op:       delete(20)")
    print("  Expected: head -> 10, 10.next is None")
    sll.delete(20)
    assert sll.head is not None
    print(f"  Actual:   {sll}, 10.next is {sll.head.next}")
    assert list(sll) == [10]
    assert sll.head.next is None
    print("PASS: boundary test")

    print(f"str(): {SinglyLinkedList([3, 4, 1, 2])}")
    print("traverse():")
    SinglyLinkedList([1, 2]).traverse()


def test_bubble_sort() -> None:
    sll = SinglyLinkedList([3, 4, 1, 2])
    trace = sll.bubble_sort_trace()
    print("Bubble sort passes on [3, 4, 1, 2]:")
    for i, (values, swaps) in enumerate(trace, 1):
        print(f"  pass {i}: {values} swaps={swaps}")
    assert trace == [([3, 1, 2, 4], 2), ([1, 2, 3, 4], 2), ([1, 2, 3, 4], 0)]
    print("PASS: pass table")

    sll = SinglyLinkedList([3, 1, 2])
    before = sll.nodes()
    sll.swap_data(before[0], before[1])
    assert sll.nodes() == before
    assert list(sll) == [1, 3, 2]
    print("PASS: swap_data changes data only, no next references")

    cases = [[], [5], [1, 2, 3], [4, 3, 2, 1], [-2, 5, -9, 0], [3, 1, 3, 1, 2]]
    for values in cases:
        sll = SinglyLinkedList(values)
        sll.bubble_sort()
        assert list(sll) == sorted(values)
        assert len(sll) == len(values)
    print("PASS: empty, one, sorted, reverse, negatives, duplicates")

    values = [5, -1, 3, 3, 0]
    sll = SinglyLinkedList(values)
    print(f"Test: input {values}, predicted {sorted(values)}", end="")
    sll.bubble_sort()
    print(f", actual {list(sll)}")
    assert list(sll) == sorted(values)


def test_reverse() -> None:
    sll = SinglyLinkedList([1, 2, 3])
    a, b, c = sll.nodes()
    labels = {id(a): "A", id(b): "B", id(c): "C", id(None): "None"}
    prev: Node | None = None
    current = sll.head
    print("Reverse trace (A=1, B=2, C=3):")
    trace: list[tuple[str, str]] = []
    while current is not None:
        saved_next = current.next
        current.next = prev
        prev, current = current, saved_next
        trace.append((labels[id(prev)], labels[id(current)]))
        print(f"  prev={trace[-1][0]} current={trace[-1][1]}")
    sll.head = prev
    assert trace == [("A", "B"), ("B", "C"), ("C", "None")]
    assert sll.nodes() == [c, b, a]
    print("PASS: reference trace")

    for values in [[], [1], [1, 2], [1, 2, 3, 4], [2, 2, 1, 2]]:
        sll = SinglyLinkedList(values)
        original = sll.nodes()
        sll.reverse()
        assert list(sll) == values[::-1]
        assert sll.nodes() == original[::-1]  # same node objects, relinked
        sll.reverse()
        assert sll.nodes() == original
    print("PASS: empty, one, two, many, duplicates; twice restores node order")

    sll = SinglyLinkedList([1, 2, 3, 4])
    print(f"Test: {sll}, expected head -> 4 -> 3 -> 2 -> 1", end="")
    sll.reverse()
    print(f", actual {sll}")


def test_remove_nth_from_end() -> None:
    print("remove_nth_from_end on fresh [1, 2, 3, 4, 5]:")
    expected: dict[int, tuple[int | str, list[int]]] = {
        1: (5, [1, 2, 3, 4]),
        4: (2, [1, 3, 4, 5]),
        5: (1, [2, 3, 4, 5]),
        0: ("ValueError", [1, 2, 3, 4, 5]),
        6: ("ValueError", [1, 2, 3, 4, 5]),
    }
    for n, (want_removed, want_list) in expected.items():
        sll = SinglyLinkedList([1, 2, 3, 4, 5])
        try:
            removed: int | str = sll.remove_nth_from_end(n)
        except ValueError:
            removed = "ValueError"
        print(f"  n={n}: removed={removed} list={list(sll)}")
        assert (removed, list(sll)) == (want_removed, want_list)
    print("PASS: prediction table")

    empty = SinglyLinkedList()
    try:
        _ = empty.remove_nth_from_end(1)
        raise AssertionError
    except ValueError:
        assert empty.head is None
    one = SinglyLinkedList([9])
    assert one.remove_nth_from_end(1) == 9
    assert one.head is None
    print("PASS: empty list raises, one-node list becomes empty")

    sll = SinglyLinkedList([1, 2, 3, 4, 5])
    nodes = sll.nodes()
    _ = sll.remove_nth_from_end(4)
    assert len(sll) == 4
    assert sll.nodes() == [nodes[0], *nodes[2:]]
    print("PASS: valid removal drops exactly one node")


def test_merge() -> None:
    list1 = SinglyLinkedList([1, 4, 7])
    list2 = SinglyLinkedList([2, 4, 8])
    merged, steps = list1.merge_trace(list2)
    print("Merge [1, 4, 7] with [2, 4, 8]:")
    so_far: list[int] = []
    for i, (source, value) in enumerate(steps, 1):
        so_far.append(value)
        print(f"  step {i}: {source} -> {value}, result {so_far}")
    assert steps == [
        ("list1", 1), ("list2", 2), ("list1", 4),
        ("list2", 4), ("list1", 7), ("list2", 8),
    ]  # fmt: skip
    print("PASS: append-step table")

    cases = [
        ([], []), ([], [1, 2]), ([1, 3, 5], [2, 4, 6]),
        ([1, 2], [8, 9]), ([2, 2], [2, 2]), ([1], [0, 3, 5, 7]),
    ]  # fmt: skip
    for a, b in cases:
        la, lb = SinglyLinkedList(a), SinglyLinkedList(b)
        before = la.nodes() + lb.nodes()
        out = la.merge(lb)
        assert list(out) == sorted(a + b)
        assert len(out) == len(a) + len(b)
        assert list(la) == a
        assert list(lb) == b
        assert la.nodes() + lb.nodes() == before
        assert not {id(n) for n in out.nodes()} & {id(n) for n in before}
    print("PASS: empties, interleaved, disjoint, duplicates, unequal lengths")
    print("PASS: inputs unchanged, result nodes are new")

    print(f"Test: {list1} + {list2}, expected [1, 2, 4, 4, 7, 8], actual {merged}")


def test_merge_n() -> None:
    inputs = [[1, 5, 9], [2, 6], [0, 3, 7, 10], [4, 8]]
    lists = [SinglyLinkedList(v) for v in inputs]
    merged = merge_n(lists)
    expected = sorted(v for vs in inputs for v in vs)
    print(f"merge_n({inputs}) = {list(merged)}")
    assert list(merged) == expected
    assert [list(sll) for sll in lists] == inputs
    assert list(merge_n([SinglyLinkedList(), SinglyLinkedList([1])])) == [1]
    assert list(merge_n([SinglyLinkedList([3]), SinglyLinkedList([1]),
                         SinglyLinkedList([2])])) == [1, 2, 3]  # fmt: skip
    try:
        _ = merge_n([SinglyLinkedList()])
        raise AssertionError
    except ValueError:
        pass
    print("PASS: merge_n (even and odd N, empty input, N < 2 raises)")


def test_variants() -> None:
    sll = SinglyLinkedList()
    for v in (3, 2, 1):
        sll.insert_at_head(v)
    assert list(sll) == [1, 2, 3]
    sll = SinglyLinkedList()
    for v in (5, 1, 3, 1, 9):
        sll.insert_sorted(v)
    assert list(sll) == [1, 1, 3, 5, 9]
    sll = SinglyLinkedList([1, 3])
    sll.insert_at(0, 0)
    sll.insert_at(2, 2)
    sll.insert_at(4, 4)
    assert list(sll) == [0, 1, 2, 3, 4]
    assert sll.delete_at(0) == 0 and sll.delete_at(3) == 4 and list(sll) == [1, 2, 3]
    sll = SinglyLinkedList([7, 7, 1, 7, 2, 7])
    assert sll.delete_all(7) == 4 and list(sll) == [1, 2]
    sll = SinglyLinkedList([1, 1, 2, 3, 3, 3])
    sll.remove_duplicates_sorted()
    assert list(sll) == [1, 2, 3]
    assert sll.index_of(3) == 2 and sll.index_of(9) == -1 and sll.get(1) == 2
    assert SinglyLinkedList([1, 2, 3, 4, 5]).middle() == 3
    assert SinglyLinkedList([1, 2, 3, 4]).middle() == 3
    cyc = SinglyLinkedList([1, 2, 3])
    assert not cyc.has_cycle()
    nodes = cyc.nodes()
    nodes[-1].next = nodes[0]
    assert cyc.has_cycle()
    sll = SinglyLinkedList([4, -2, 9, 1])
    assert sll.max_value() == 9 and sll.sum_values() == 12
    sll.reverse_recursive()
    assert list(sll) == [1, 9, -2, 4]
    assert sll.equals(sll.copy()) and sll.copy().nodes()[0] is not sll.head
    assert not sll.equals(SinglyLinkedList([1, 9]))
    inter = SinglyLinkedList([1, 3, 5, 7]).interleave(SinglyLinkedList([2, 4]))
    assert list(inter) == [1, 2, 3, 4, 5, 7]
    print("PASS: variants")


def test_search_variants() -> None:
    unsorted = SinglyLinkedList([7, 3, 9, 3, 1])
    assert unsorted.linear_search(9) == 2 and unsorted.linear_search(4) == -1
    assert unsorted.linear_search_count(7) == (True, 1)  # best case: head
    assert unsorted.linear_search_count(4) == (False, 5)  # worst case: absent, n
    assert unsorted.count_occurrences(3) == 2 and unsorted.all_positions(3) == [1, 3]
    assert unsorted.last_index_of(3) == 3 and not unsorted.is_sorted()
    srt = SinglyLinkedList([1, 3, 5, 7, 9])
    assert srt.is_sorted() and srt.search_sorted(7) and not srt.search_sorted(4)
    assert srt.search_sorted_count(4) == (False, 3)  # stops at 5
    assert SinglyLinkedList([9, 1, 7, 5, 3]).linear_search_count(4) == (False, 5)
    assert srt.find_min_sorted() == 1 and srt.sum_at_positions(1, 3) == 15
    srt.insert_unsorted(0)
    assert list(srt) == [0, 1, 3, 5, 7, 9]
    empty = SinglyLinkedList()
    assert empty.linear_search(1) == -1 and empty.is_sorted() and not empty.search_sorted(1)
    print("search: linear (best 1 / worst n), sorted early exit, counts, positions OK")
