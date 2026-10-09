![[Data Structures & Algorithms.mp3]]
Last updated: 2026-W41
Not yet condensed: none (Weeks 1-3 in the vault, all condensed).

## Week 3: Recursion, divide and conquer, backtracking

**Key ideas**
- Recursion needs a base case, a recursive step on a strictly smaller input, and guaranteed progress to the base case. Missing any one gives `RecursionError`.
- Each call gets its own stack frame (parameters, locals, resume point). Frames return LIFO.
- Cost recursion two ways: time = work over all calls; space = maximum depth of active calls.
- Divide and conquer: split, solve each part recursively, combine (merge sort, quicksort, binary search).
- Backtracking: make a choice, recurse, undo the choice if it fails. Returning from a call does not undo changes to shared state.

**Key terms**
- **Tail recursion**: the recursive call is the last action. `reverse_array` is tail recursive; `array_sum` is not (it adds after the call returns). Tail recursion converts to a loop.
- **Overlapping subproblems**: the same subcall recomputed (naive Fibonacci). Fix with memoisation or iteration.
- **Pivot**: after partitioning it sits in its final sorted position. Neither side is sorted yet.
- **Auxiliary space**: extra memory beyond the input, including the call stack.

**Costs to know**

| Algorithm | Time | Space |
|---|---|---|
| Factorial, triangular, array sum, reversal | O(n) | O(n) stack (loop: O(1)) |
| Naive Fibonacci | Θ(φ^n), bounded by O(2^n) | O(n) stack |
| Iterative Fibonacci | O(n), n-2 additions | O(1) |
| Hanoi, M(n) = 2M(n-1)+1 = 2^n - 1 moves | O(2^n) | O(n) |
| Recursive binary search | O(log n) | O(log n) stack |
| Merge sort, T(n) = 2T(n/2)+Θ(n) | Θ(n log n), all cases | O(n) merge list + O(log n) stack |
| Quicksort | avg O(n log n), worst O(n^2) | O(log n) stack, worst O(n) |

**Mechanics**
- Recursive binary search base cases: `lower > upper` (return -1) and `A[mid] == target`.
- Quicksort partition (last-element pivot): `index = start`; for each k, if `arr[k] <= pivot` swap into `arr[index]`, `index += 1`; finally swap the pivot into `arr[index]`. `[10,80,30,90,40,50,70]` gives `[10,30,40,50,70,90,80]`, returns 4.
- Lecture uses `<= pivot`; worksheet uses strict `<`. Check which the question asks for.
- Backtracking template: `if complete: return True` → for each valid choice: apply, `if solve(): return True`, undo → `return False`.
- Eight queens: 92 solutions. Maze: track visited cells; finds a path, not the shortest.

**Exam traps**
- Naive Fibonacci is slow because of overlapping subproblems, not because recursion is slow. F(30): 28 additions iteratively vs 832,039 recursively.
- Quicksort worst case: an extreme pivot every time (sorted or all-equal input with a first or last pivot).
- Merge sort is stable only if ties take from the left half first.
- Iterations, total calls and maximum depth are three different counts. Factorial(4) has 5 frames at the deepest point.
- Backtracking that forgets to undo (cell, queen, path mark) corrupts later branches.

Full notes: [[Week 3 - Recursion, Divide and Conquer, and Backtracking]]

## Week 2: Algorithm efficiency, searching and sorting

**Key ideas**
- Big-O is an upper bound on growth. Keep the dominant term; drop constants and lower terms (2n+1 → O(n)).
- Total cost = repetitions × cost per repetition. A call inside a loop counts.
- Doubling n: O(n) time ×2, O(n^2) ×4, O(n^3) ×8. Runtimes 512, 2048, 8192 ms per doubling means O(n^2).
- Same Big-O does not mean same speed (a step of 2 is still O(n)).

**Loop patterns**

| Pattern | Big-O |
|---|---|
| `k += 1` or `k += 2` | O(n) |
| `k *= 2` (n = 1000: ~10 iterations) | O(log n) |
| Nested, independent n × n | O(n^2) |
| Nested, inner bound = outer index: n(n+1)/2 | O(n^2) |
| Linear outer, doubling inner | O(n log n) |
| Sequential blocks | add, keep the max |
| n iterations calling an O(n) function | O(n^2) |

**Sorts and searches**

| Algorithm | Best | Worst | Notes |
|---|---|---|---|
| Selection | O(n^2) | O(n^2) | always n(n-1)/2 comparisons |
| Bubble, basic | O(n^2) | O(n^2) | no early exit |
| Bubble, flag | O(n) | O(n^2) | flag reset each pass |
| Insertion | O(n) sorted | O(n^2) reversed | good for nearly sorted data |
| Linear search | O(1) | O(n) | avg (n+1)/2; works unsorted |
| Binary search | O(1) | O(log n) | sorted + O(1) index access; ≤ 1+log2 n iterations (1000 → 10, 10^6 → 20) |

All elementary sorts and iterative searches: O(1) auxiliary space.

**Exam traps**
- Counting loop iterations and forgetting the cost of the body.
- Binary search on unsorted data gives wrong answers.
- Setting `upper = mid` instead of `mid - 1` can loop forever.
- Bubble sort that never resets the flag, or stops after one clean pair, ends early.
- Insertion sort: `index_hole > 0 and ...` must come first, or the index goes negative.
- Queue method 1 (head fixed at 0) has O(n) dequeue. Methods 2 and 3 are O(1).

Full notes: [[Week 2 - Algorithm Efficiency, Searching and Sorting]]

## Week 1: Introduction to data structures, DS and ADT

**Key ideas**
- Pick the structure by the operations you need (which, how often, in what order, how much capacity). No structure is best for everything.
- A data structure = elements + the relationships between them.
- An ADT hides the representation: callers use methods (what), never the implementation (how). Data is reachable only through its methods.
- Stack is LIFO (push, pop, peek). Queue is FIFO (enqueue at tail, dequeue at head). Both must raise overflow (full) and underflow (empty).
- Efficiency is how cost grows with `n`. Sum 1..n: loop is O(n), `n(n+1)/2` is O(1).
- Structure classes by predecessor/successor: linear (1 to 1), hierarchical (1 to many), graph (many to many), set (none).
- Algorithm design classes: brute force, divide and conquer, backtracking, greedy.

**Key terms**
- **ADT vs data structure**: ADT = what (behaviour, implementation-independent). Data structure = how (concrete, implementation-dependent). Lost a mark on this in Moodle mock 1.
- **CRUD**: create, read, update, delete. Search, sort, reverse, filter are built from these.
- **Static storage**: fixed capacity; contents and count can still change.
- **Dynamic storage**: grows by allocating a bigger block and copying. Append is amortised O(1) with an occasional O(n) copy.
- **Encapsulation**: no direct access to the data, only via methods.

**Mechanics to remember**
- Array stack: empty is `top = -1`, full is `top = N-1`. Push and pop are O(1).
- Queue, three versions:
  1. Head fixed at index 0: dequeue shifts everything, O(n).
  2. Movable head and tail: both O(1), but cells before head are never reused (false full).
  3. Circular: `i = (i + 1) mod N`, reuses space.
- Circular queue ambiguity: empty and full both give `head = (tail + 1) mod N`. Fix with a count, a full/empty flag, or one wasted slot (capacity N-1).
- Bracket matching: push openers, pop on a closer and compare, balanced only if the stack is empty at the end. Uses only the ADT interface.
- Two Towns: star graph costs 2 roads per hop, ring costs 1. Same elements, different structure, different costs. Dominant operation decides the best structure.

**Exam traps**
- Wrong structure for the data (arrays for trees or graphs) makes relationship queries impossible or slow.
- "Static" means fixed capacity, not fixed contents.
- Fixed-width ints can overflow in `n(n+1)` before the divide; in Python use `n * (n + 1) // 2`.
- Pop, peek, dequeue or first on empty is underflow; push or enqueue on full is overflow. Both raise exceptions.
- Default capacity 5 silently breaks algorithms that need more; size auxiliary stacks to the input. Create a fresh stack per call (no state leaking between calls).

Full notes: [[Week 1 - Data Structures and ADTs]]
