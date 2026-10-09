## 1. Core Thesis & Problem Space

- Problem Statement: Programs must store, access and modify data. How the data is organised decides whether the required operations are simple and efficient or cumbersome and inefficient. No single structure suits all applications. Repeating an inefficient operation many times still costs substantial work.
- Central Hypothesis / Approach: Analyse the problem (operations, their frequency, ordering and capacity needs), compare representations, then choose a structure whose relationships match the problem. Hide the representation behind an Abstract Data Type (ADT), so applications depend on behaviour (what) and not on implementation (how). For many problems the structure choice is the main decision, and the algorithms are simple once it is made.
- Core System Invariant: An ADT's data is reachable only through its methods. Stack: only the most recently inserted item (Top) is removable (LIFO). Queue: only the longest-stored item (Head) is removable (FIFO). Illegal calls (push or enqueue on full, pop, peek or dequeue on empty) raise exceptions and leave the structure unchanged.

## 2. Technical Vocabulary & Formal Definitions

- **Data structure**: A way to store and organise data to facilitate access and modification. It has two parts: a collection of elements (each a data type or another data structure) and a set of relationships among them (the structure). For an array, the data is the element sequence and the structure is the positional relationship between elements. The same values can be organised differently to support different operations.
- **Algorithm**: A well-defined computational procedure, a finite sequence of steps transforming input into output. Judged first on correctness, then on time and space efficiency.
- **Efficiency**: Growth of time or memory cost with input size $n$. Ordering of common growth rates: $1 < \log n < n < n\log n < n^2 < n^3 < 2^n$. Examples: indexed access is constant; a loop that halves $n$ each step is logarithmic; one loop over the input is linear; nested loops over the input are quadratic.
- **CRUD**: Create/Insert, Read/Access, Update, Delete. Combined operations built from these: Search, Sort, Reverse, Filter.
- **Address and index**: Memory locations have addresses; an array index identifies an element's position within an array and is not necessarily its byte address. Bits mean nothing until interpreted (instruction, integer, character).
- **Fixed-size (static) storage**: Capacity is fixed once allocated, though it may be chosen at creation time and not at compile time. Values and item count can change. When full, no further item fits. The limit is predictable but space may go unused.
- **Resizable (dynamic) storage**: Capacity can grow on demand (Python list, Java ArrayList). Growth may allocate a larger region and copy existing items. Implementations over-allocate to reduce resize frequency, so append is amortised $O(1)$ with occasional $O(n)$ copies. Removing an item does not necessarily shrink the allocation.
- **Abstract Data Type (ADT)**: A collection of data plus associated methods packaged as one module. It contains the data structure, methods to access it, methods to modify it, and internal methods not accessible from outside. It specifies what information is stored and what can be done, not how.
- **Encapsulation**: Data is reachable only indirectly through methods. The application does not care how storage is managed; the ADT does not care which application uses it. Car analogy: steer, accelerate and brake form a uniform interface; front-wheel and rear-wheel drive are different implementations.
- **Stack**: Linear ADT, Last-In First-Out. Methods: Push, Pop, Peek, Length (Empty and Full as predicates).
- **Queue**: Linear ADT, First-In First-Out (equivalently Last-In Last-Out). Insert at Tail (rear), remove at Head (front). Methods: Enqueue, Dequeue, Peek (First), Length (Empty and Full as predicates).
- **Overflow and underflow**: Overflow is push or enqueue on a full structure. Underflow is pop, peek, dequeue or first on an empty one. In Python the worksheet uses OverflowError and IndexError.
- **Circular queue**: Array treated as a ring; the last position connects back to the first, so freed cells are reused.
- Algorithm design classes (different ways of searching among candidate solutions):
    - **Brute force**: Enumerate every candidate and select the best. Simple and always finds the answer, but infeasible when candidates grow exponentially (a chess search that tries every move sequence).
    - **Divide and conquer**: Recursively split into sub-problems of the same or related type until directly solvable, then combine. Examples: merge sort, quicksort, binary search.
    - **Backtracking**: Extend a partial solution while it stays consistent; on inconsistency, remove the most recent part and try another option. Usually recursive. Examples: maze route, eight queens, knight's tour.
    - **Greedy**: Take the locally best decision at each stage and never reconsider it. Correct only for some problems, because local optima do not always yield a global optimum.

## 3. System Mechanics & Governing Principles

- Selecting a structure: analyse the problem; determine operations, frequency, ordering and capacity needs; compare representations and implementations. The relationship structure and the storage policy (fixed or resizable) are separate design choices. A fixed-size array can still represent a tree, and a fixed-size adjacency matrix can represent a graph.
- Classification by predecessor and successor count:
    - Linear: one predecessor, one successor (stack, queue).
    - Hierarchical: one predecessor, many successors (family tree, management structure).
    - Graph (network): many predecessors, many successors (railway map, social network, computer network).
    - Set: no predecessor, no successor (students in a class).
    - The same group of students can be a waiting line, a reporting hierarchy or a collaboration network. Only the relationships change.
- Efficiency comparison, sum of the first $n$ integers:  
    $$S = \sum_{i=1}^{n} i = \frac{n(n+1)}{2}$$  
    Where: $n$ = count of integers. The loop does $n$ additions, $O(n)$. The formula does a fixed number of operations, $O(1)$. The product $n(n+1)$ is always even, so the division is exact.
- Stack on a static array of capacity $N$ ($top$ = index of last occupied cell):
    
    - Empty: $top = -1$. Full: $top + 1 = N$. Length: $top + 1$.
    - Push: check full, $top \leftarrow top + 1$, store at $top$. Pop: check empty, read $top$, $top \leftarrow top - 1$. Peek: check empty, read $top$, no change. All $O(1)$.
    
    ```python
  class Stack:
      def __init__(self, capacity=5):
          self.data, self.top, self.max_size = [], -1, capacity   # fresh list per instance
      def push(self, x):
          if self.top + 1 == self.max_size: raise OverflowError
          self.data.append(x); self.top += 1
      def pop(self):
          if self.top == -1: raise IndexError
          x = self.data[self.top]; self.data.pop(); self.top -= 1
          return x
      def peek(self):
          if self.top == -1: raise IndexError
          return self.data[self.top]
      def length(self): return self.top + 1
    ```
    
- Queue on a static array, three implementations:
    
    - Version 1 (Head fixed at index 0, $tail$ = last index, initially $-1$): Enqueue increments $tail$, $O(1)$. Dequeue removes index 0 and shifts the rest left, $O(n)$. Length is $tail + 1$.
    - Version 2 (movable Head and Tail): items never move; Enqueue increments Tail, Dequeue increments Head. Both $O(1)$, but cells before Head are never reused, so the array reports full at index $N-1$ while space is free.
    - Version 3 (circular): indices wrap, so freed space is reused:  
        $$tail \leftarrow (tail + 1) \bmod N, \qquad head \leftarrow (head + 1) \bmod N$$  
        Where: $N$ = capacity; $head$ = index of front element; $tail$ = index of last element.
    
    ```python
  # Version 1 core (worksheet Queue)
  def enqueue(self, x):
      if self.tail + 1 == self.max_size: raise OverflowError
      self.data.append(x); self.tail += 1
  def dequeue(self):
      if self.tail == -1: raise IndexError
      x = self.data.pop(0); self.tail -= 1      # pop(0) shifts: O(n)
      return x
    ```
    
- Circular queue with explicit count (disambiguates full from empty):
    
    ```python
  class CircularQueue:
      def __init__(self, N):
          self.a, self.N = [None] * N, N
          self.head, self.tail, self.count = 0, N - 1, 0
      def is_empty(self): return self.count == 0
      def is_full(self):  return self.count == self.N
      def enqueue(self, x):
          if self.is_full(): raise OverflowError
          self.tail = (self.tail + 1) % self.N
          self.a[self.tail] = x; self.count += 1
      def dequeue(self):
          if self.is_empty(): raise IndexError
          x = self.a[self.head]
          self.head = (self.head + 1) % self.N; self.count -= 1
          return x
    ```
    
- Bracket validity with a stack (depends only on the ADT interface; fresh stack per call):
    
    ```python
  def brackets_valid(s):
      pairs = {')': '(', ']': '[', '}': '{'}
      st = Stack(len(s) + 1)                  # capacity must not be the default 5
      for ch in s:
          if ch in '([{':
              st.push(ch)
          elif ch in pairs:
              if st.length() == 0 or st.pop() != pairs[ch]:
                  return False                # unmatched or mismatched closer
      return st.length() == 0                 # leftover openers mean invalid
    ```
    
    - Position-reporting variant (single bracket type): push the index of each '('; on ')' with an empty stack record the index as the rightmost unmatched ')' and stop; after the loop the top of the stack is the index of the unmatched '('.
- Cascading adjacent-duplicate removal with a stack: read left to right; if the stack is non-empty and its top equals the incoming character, pop and discard the incoming character; otherwise push. The result is the stack read bottom to top. Examples: "abbccd" -> "ad", "dsallasg" -> "dg", "abccbadd" -> "".
- Reversing a queue with a stack: dequeue every item and push it, then pop every item and enqueue it. A stack reverses order, and the queue preserves the order in which items re-enter. Cost for $n$ items: $n$ dequeue, $n$ push, $n$ pop, $n$ enqueue calls, so $4n$ calls. The stack capacity must be at least $n$.
- Using the other ADT for the stack-based tasks: a queue can emulate a stack by rotating after each enqueue. After enqueueing, move the $size-1$ older items from front to rear so the newest item is at the front. Push is then $O(n)$ and pop is a plain dequeue. A queue exposes only its Head, so the "most recent retained item" is hard to reach. Alternatively, repeat full passes over a queue until nothing changes, which is $O(n^2)$ in the worst case.
- Pass-the-Potato (Josephus style) with a static array:
    - Holder index $p$; after $m$ passes $p \leftarrow (p + m) \bmod size$. Remove the holder by shifting later elements left ($O(n)$) and decrementing $size$; the next child now sits at index $p$.
    - Limitations: fixed capacity with a shrinking population, shifting cost per elimination, and the alternative of marking cells as removed forces skipping dead cells.
    - With a queue: rotate $m$ times (dequeue then enqueue), then dequeue the front child, who leaves. The next child holds the potato. Repeat until one remains.
- Other stack uses: the recursion call stack (each call has an activation record holding its local namespace and parameters) and evaluation of arithmetic expressions.

## 4. Visual & Structural Logic

- ADT diagram: Data In -> public method -> Data Structure (hidden) -> public method -> Data Out. An internal method is called only by other methods inside the ADT. No arrow enters the Data Structure from outside.
- Stack array: cells $0..N-1$ filled contiguously from 0; the Top arrow marks the last filled cell; cells above Top are free. Push moves Top up, pop moves it down.
- Queue Version 1: Head pinned at index 0, Tail at last filled cell, data flows toward index 0. Version 2: cells $0..2$ already dequeued and empty, Head at 3, Tail at the last filled cell, so the occupied window drifts right toward $N-1$.
- Worksheet traces (capacity 5, start empty):
    - Stack: push("A") returns None, [A], top 0. push("B") returns None, [A,B], top 1. peek() returns B, [A,B], top 1. pop() returns B, [A], top 0. push("C") returns None, [A,C], top 1.
    - Queue: enqueue("A") returns None, [A], tail 0. enqueue("B") returns None, [A,B], tail 1. dequeue() returns A, [B], tail 0. enqueue("C") returns None, [B,C], tail 1. peek() returns B, [B,C], tail 1.
    - Queue reversal on [A,B,C]: start Q=[A,B,C], stack empty. After one transfer Q=[B,C], stack=[A]. After all leave Q: Q empty, stack bottom to top A,B,C (top C). After one return transfer: Q=[C], stack=[A,B]. Finished: Q=[C,B,A], stack empty.
    - Duplicate removal on "abba": a is pushed (retained a); b is pushed (ab); b matches top, popped (a); a matches top, popped (empty). Result is the empty string.
- Stack exercise traces:
    - Push 3,5,7,9,11,13 on S1, then move all to S2 one pop at a time: S2 bottom to top is 13,11,9,7,5,3 and S1 is empty.
    - Same pushes, but each loop iteration pops twice and pushes only the second popped value: S2 bottom to top is 11,7,3. An odd count would underflow on the second pop.
    - Mixed stack and queue sequence: S bottom to top is 3,2,12,5; Q head to tail is 8,12; X=12, Y=5.
- Transfers with extra stacks: S1 to S2 preserving order uses S3 (S1 to S3 reverses, S3 to S2 reverses again). Reversing S1 with S2 and S3: S1 to S2, S2 to S3, S3 to S1.
- Queue utilities with only Enqueue, Dequeue, Empty: count by dequeueing each item into a temporary queue while counting, then restoring. CatQueue: while Q2 is not empty, enqueue each dequeued item onto Q1. CopyQueue: dequeue each item into both the copy and a temporary queue, then restore the original from the temporary queue.
- Two Towns (8 houses, 8 equal roads, start at house 1, visit all, no return):
    - Town 1 (star, hub in the middle): each house-to-house move costs 2 roads, so a full tour is $7 \times 2 = 14$.
    - Town 2 (ring 1-2-...-8-1): neighbours are 1 road apart, so a full tour is 7. Town 1 therefore walks twice as far.
    - Even houses only: Town 1 is $4 \times 2 = 8$; Town 2 is $1 + 2 + 2 + 2 = 7$.
    - A single random house: Town 1 always costs 2 (like direct indexing); Town 2 costs 1 to 4 depending on position (like sequential traversal).
    - Lesson: same elements and edge counts, different structure, different cost per operation. The dominant operation decides the best structure.
- Family tree in a 1D list or 2D array (row per generation): parent-child relationships are not encoded; the fit is hierarchical.
- Underground map in a 1D list or 2D array (row per line): locating a station is a search, and line changes and splitting lines cannot be expressed; the fit is graph.
- Activity 1.4 (Tail = index of last element):
    - Left: one element, Head = 3, Tail = 3. Dequeue gives Head = 4, Tail = 3. The queue is empty and $head = (tail + 1) \bmod N$.
    - Right: one free slot at 3, Tail = 2, Head = 4. Enqueue gives Tail = 3, Head = 4. The queue is full and $head = (tail + 1) \bmod N$.
    - Both states give the same Head/Tail relationship, so the indices alone cannot separate empty from full.
    - Four fixes:
        - Keep an element count.
        - Keep a full/empty flag.
        - Reserve one slot (full when $head = (tail + 2) \bmod N$, usable capacity $N-1$).
        - Use a sentinel for empty: reset to $tail = -1$ when the last element is removed.

## 5. Failure Modes, Edge Cases, & Bottlenecks

- Failure Mode 1: Structure mismatch. Arrays for trees or graphs encode no relationships, so relationship queries need costly searches or are impossible.
- Failure Mode 2: Queue Version 1 dequeue is $O(n)$ because of shifting. Reversing a queue by repeated dequeue is therefore $O(n^2)$ on this representation and $O(n)$ on a circular one.
- Failure Mode 3: Queue Version 2 raises a false overflow when Tail reaches $N-1$ with free cells before Head.
- Failure Mode 4: Circular queue ambiguity: empty and full both satisfy $head = (tail+1) \bmod N$ unless a count, flag, sentinel or reserved slot is used.
- Failure Mode 5: Fixed capacity must be estimated in advance. A default capacity of 5 silently breaks algorithms that need more (six-item queue reversal, six nested brackets). Size auxiliary stacks to the input.
- Failure Mode 6: State leakage between calls (module-level stack, mutable default argument, un-reset instance). A call such as brackets_valid("(") followed by brackets_valid("ds") must still return True for the second. Create a fresh structure in every call and a fresh list inside `__init__`.
- Failure Mode 7: Counting brackets only misses order and type errors ("([)]" has balanced counts but is invalid).
- Trade-off: Resizable storage removes the hard limit, but a growth step costs $O(n)$ copying and reserves extra memory. Fixed storage is predictable but may waste space.
- Edge Case Behavior:
    - Pop, peek or dequeue on empty raises IndexError; push or enqueue on full raises OverflowError. Catch the expected exception in tests and check that the structure is unchanged.
    - A closing bracket on an empty stack returns False and must not raise.
    - Empty string: brackets valid is True; duplicate removal returns "".
    - A one-item queue becomes empty after dequeue.
    - Circular indices wrap from $N-1$ to 0.
    - Fixed-width integer languages may overflow in $n(n+1)$ before dividing; in Python use `n * (n + 1) // 2`.

## 6. High-Yield Verification Checklist

- [ ] What two parts define a data structure? -> A collection of elements and the relationships among them.
- [ ] ADT versus data structure? -> ADT: high-level, what it does, implementation independent. Data structure: concrete, how it is done, implementation dependent.
- [ ] Which class has a unique predecessor and many successors? -> Hierarchical (tree).
- [ ] What does "static" mean for fixed-size storage? -> Fixed capacity only; stored values and item count can still change.
- [ ] Which errors must a Stack ADT signal? -> Overflow on push to a full stack; underflow on pop or peek of an empty stack.
- [ ] Stack empty and full tests with $top$? -> Empty: $top = -1$. Full: $top + 1 = N$. Length: $top + 1$.
- [ ] Why is the formula sum better than the loop? -> $O(1)$ versus $n$ additions, $O(n)$.
- [ ] Cost of dequeue with Head fixed at index 0? -> $O(n)$, since all remaining elements shift.
- [ ] Problem with movable Head and Tail on a linear array? -> Freed front cells are never reused; false full at $N-1$.
- [ ] Circular index update? -> $i \leftarrow (i+1) \bmod N$.
- [ ] Head/Tail relation for both empty and full circular queue? -> $head = (tail+1) \bmod N$; fix with a count, a flag, a sentinel, or one reserved slot.
- [ ] Why does Town 1 cost twice Town 2 for a full tour? -> Every hop in the star passes through the hub (2 roads); ring neighbours are 1 road apart.
- [ ] How many ADT calls does stack-based queue reversal make for $n$ items? -> $n$ dequeue, $n$ push, $n$ pop, $n$ enqueue ($4n$ total), with stack capacity at least $n$.
- [ ] Rule for removing adjacent duplicates with a stack? -> If the incoming character equals the top, pop it; otherwise push it. Read the stack bottom to top.
- [ ] Why does "([)]" fail bracket validation? -> The closer ')' meets '[' on top of the stack, a type mismatch.
- [ ] What does the consecutive-call test (brackets_valid("(") then ("ds")) check? -> That no state persists between calls; each call must use a fresh stack.
- [ ] Stack or queue for undo, layoff of the newest hire, backtracking from a maze dead end, and return addresses of nested calls? -> Stack (most recent first).
- [ ] Stack or queue for print jobs, clinic first-come first-served, bakery ticket numbers, OS resource requests, and checkout simulation? -> Queue (earliest first).
- [ ] Which scenarios suit neither a stack nor a queue? -> Parts processed by part number (keyed or ordered access) and lottery draws (random selection, set-like).
- [ ] Why can the bracket-matching algorithm use any stack implementation? -> It depends only on the ADT operations, not on the representation.