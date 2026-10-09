## 1. Core Thesis & Problem Space

- Problem Statement: Repetition can be expressed without loops by defining a problem in terms of smaller instances of itself. The material covers how to construct such solutions correctly (base case, progress, termination), how to cost them (time over all calls, space over the maximum active call depth), and how to extend them to divide and conquer (Mergesort, Quicksort, binary search) and exhaustive search with undo (backtracking).
- Central Hypothesis / Approach: Define the solution for the simplest input directly (base case). Express every other input through one or more calls on strictly smaller inputs (recursive step). The call stack stores pending work and returns results LIFO. Backtracking adds explicit state restoration after each failed recursive branch.
- Core System Invariant: Every chain of recursive calls must strictly shrink a measure (n, interval length, `right - left`, sum of arguments, number of empty cells) toward a base case. Shared mutable state must be restored to its pre-call value before the next alternative is tried.

## 2. Technical Vocabulary & Formal Definitions

- Iteration: explicit repetition with `for`/`while`, updating variables between passes.
- Recursion: implicit repetition by a function calling itself; each call has its own parameters and local state.
- Base (stopping) case: input solved directly with no further recursive call. Missing or wrong base cases give infinite recursion (`recursive_print_example`, the Captain's Story).
- Recursive step: reduces the current instance to smaller or simpler instances of the same form.
- Termination: guaranteed when each recursive step moves strictly toward a base case.
- Stack frame: per-call record holding parameters, local state and the resume point. The most recent active call returns first (LIFO). Returning pops the frame and resumes the caller.
- Tail recursion: the recursive call is the last action of the call, with no work after it returns. `reverse_array` is tail recursive. `array_sum` is not, because it adds `A[n-1]` after the call returns. Simple tail recursion converts to a loop by updating parameters each iteration.
- Overlapping subproblems: identical subinstances recomputed across the call tree (naive Fibonacci). Memoisation stores results by input and reuses them.
- Divide and conquer: split into smaller independent parts, solve recursively, combine.
- Pivot / partition (Quicksort): the pivot lands in its final position; elements on each side are not yet sorted.
- Backtracking: build a solution one choice at a time; on failure undo the choice and try the next. Returning from a call does not undo changes to shared data.
- Auxiliary space: extra memory beyond input, including the recursion stack and temporary lists.

## 3. System Mechanics & Governing Principles

- Design checklist: identify the base case; identify the smaller instance; confirm each call makes progress; combine returned values on unwinding.
- Factorial: $n! = n \cdot (n-1)!$ for $n \ge 1$, $0! = 1$.
- Triangular numbers: $T(n) = n + T(n-1)$, $T(1) = 1$. Time $O(n)$ for recursive and iterative versions; stack $O(n)$ versus auxiliary $O(1)$.
- Array sum: `array_sum(A, n)` returns 0 at `n == 0`, else `array_sum(A, n-1) + A[n-1]`. Time $O(n)$, stack $O(n)$ (no slicing).
- Array reversal: stop when `left >= right`; swap `A[left]`, `A[right]`; recurse on `(left+1, right-1)`. Time $O(n)$, stack $O(n)$.
- Mystery: `mystery(n, m)` returns $n + m$ for non-negative $n$; terminates because $n$ decreases to 0.
- Fibonacci (F(1) = F(2) = 1):  
    $$F(n) = F(n-1) + F(n-2)$$  
    Iterative: $n-2$ additions, $O(n)$ time, $O(1)$ space. Naive recursive: $F(n)-1$ additions; calls $C(n) = C(n-1) + C(n-2) + 1 = 2F(n) - 1$. Time grows as $\Theta(\varphi^n)$ with $\varphi = (1+\sqrt5)/2$ (bounded by $O(2^n)$); stack depth $O(n)$. Example: F(30) = 832040 takes 28 additions iteratively versus 832039 recursively. Memoised version: $O(n)$ time, $O(n)$ space (table plus stack).
- Loop iterations, total calls and maximum call depth differ because iterations count sequential passes, calls count all tree nodes, and depth counts only the longest root-to-leaf chain alive at once.
- GCD by subtraction: equal arguments return the value; otherwise recurse on (positive difference, smaller value). The sum of the two arguments decreases by the smaller value each call and stays positive. `gcd(k, 1)` needs about $k$ calls, so time and stack are $O(k)$. Zero or negative input raises `ValueError`. Python's default recursion limit (about 1000) bounds usable $k$.
- Towers of Hanoi: move $n-1$ discs to temp, move disc $n$ to target, move $n-1$ discs onto it.  
    $$M(1) = 1,\quad M(n) = 2M(n-1) + 1 \Rightarrow M(n) = 2^n - 1$$  
    Time $O(2^n)$, stack $O(n)$.
- Binary search (sorted A): base cases are `lower > upper` (return -1) and `A[mid] == target`; recurse on `[lower, mid-1]` or `[mid+1, upper]`. Time $O(\log n)$, stack $O(\log n)$.
- Mergesort:  
    $$T(n) = 2T(n/2) + \Theta(n) \Rightarrow \Theta(n \log n)$$  
    Best and worst case are equal. Depth $O(\log n)$; auxiliary space $O(n)$ for the temporary merge list plus $O(\log n)$ stack. Stable if ties take the left element first.
- Quicksort: partition about a pivot, then recurse on both sides excluding the pivot.
    - Balanced splits: $T(n) = 2T(n/2) + \Theta(n)$, giving $O(n \log n)$ and stack $O(\log n)$.
    - Worst case (one side empty, e.g. all-equal or already sorted data with last/first pivot): $\sum_{k=1}^{n-1} k = \Theta(n^2)$, stack $O(n)$.
    - Average: $O(n \log n)$. Pivot options: first, last, random, median.
    - Note: the lecture notes use `<= pivot`; the worksheet uses strict `< pivot`, so the left side is strictly smaller and the right side is `>=` pivot.
- Palindrome (index-based): return True when `left >= right`; False if `text[left] != text[right]`; else recurse on `(left+1, right-1)`. Best case $O(1)$, worst case $O(n)$ time and $O(n)$ stack. Do not treat every two-character string as a palindrome.
- Backtracking template:
    
    ```python
  def solve(state):
      if is_complete(state):
          return True
      for choice in candidates(state):
          if is_valid(state, choice):
              apply(state, choice)       # make
              if solve(state):           # explore
                  return True
              undo(state, choice)        # restore shared state
      return False
    ```
    
- Sudoku: `find_next_empty()` returns (row, col) or (None, None). Try digits 1 to 9 where `is_valid` (row, column and 3x3 box). Recurse; on failure reset the cell to empty. Complete when no empty cell remains. Worst case is exponential.
- Eight Queens: one queen per row; choose a column not attacked by earlier queens (column or diagonal); if none, remove the previous queen and take its next column. 92 solutions exist.
- Maze: 2D grid, moves N/S/E/W, `#` blocked, `+` marks the current path. Track visited cells to avoid cycles; remove a cell from the path when its branch fails. Finds a path, not necessarily the shortest.
- Knight's tour: record visited squares, mark on move, unmark on failure; complete when all squares are visited.

## 4. Visual & Structural Logic

- Factorial(4) call chain: factorial(4) -> factorial(3) -> factorial(2) -> factorial(1) -> factorial(0) returns 1. Unwinding: 1x1 = 1, 2x1 = 2, 3x2 = 6, 4x6 = 24. Five active frames at deepest point (n = 4, 3, 2, 1, 0).
- cheers(2): prints Hip on entry, recurses, prints Hooray after return. Output: Hip Hip Hip Hooray Hooray Hooray.
- Triangular(6): 6 + T(5) -> 5 + T(4) -> 4 + T(3) -> 3 + T(2) -> 2 + T(1) -> 1 (base). Unwinding: 1, 3, 6, 10, 15, 21.
- Fibonacci(6) call tree: Fib(6) -> Fib(5), Fib(4). Fib(5) -> Fib(4), Fib(3). Fib(4) -> Fib(3), Fib(2). Leaves are Fib(2) and Fib(1). Fib(4) is evaluated twice and Fib(3) three times.
- Hanoi: Hanoi(n, A, C, B) = Hanoi(n-1, A, B, C); move n from A to C; Hanoi(n-1, B, C, A). Input is the disc count and pole roles, output is a move sequence, and the roles of target and temp swap at each level.
- Mergesort on [14, 33, 27, 10, 35, 19, 42, 44]: split to [14,33,27,10] and [35,19,42,44], then to pairs, then singles. Merge pairs: [14,33], [10,27], [19,35], [42,44]. Merge to [10,14,27,33] and [19,35,42,44]. Final merge: [10,14,19,27,33,35,42,44]. Execution order is depth first, left half before right half.
- Quicksort partition of [10,80,30,90,40,50,70], pivot 70 (last), index = start:
    - k=0: 10 <= 70, swap with itself, index 1.
    - k=1: 80 > 70, no action.
    - k=2: 30 <= 70, swap with arr[1], index 2.
    - k=3: 90 > 70, no action.
    - k=4: 40 <= 70, swap with arr[2], index 3.
    - k=5: 50 <= 70, swap with arr[3], index 4.
    - Final swap arr[4] with arr[6]: [10,30,40,50,70,90,80], return 4.
- Worksheet partition of [5,2,4,1,3], pivot 3, strict `<`: after j=0 i=0 [5,2,4,1,3]; after j=1 i=1 [2,5,4,1,3]; after j=2 i=1 unchanged; after j=3 i=2 [2,1,4,5,3]; final swap gives [2,1,3,5,4], return 2.
- Backtracking state tree: root is the empty board; each node is a partial assignment; edges are choices. Valid choice -> descend. Dead end -> return False, undo, try the next sibling. Success propagates True up the stack.
- Maze: S at (0,0), G at (4,5). Visit neighbour -> mark `+`; if all four neighbours fail -> unmark and return to the previous cell.

## 5. Failure Modes, Edge Cases, & Bottlenecks

- Failure Mode 1: Missing or incorrect base case, or a recursive step that does not shrink the input. Result is infinite recursion and a stack overflow (Python `RecursionError`).
- Failure Mode 2: Overlapping subproblems (naive Fibonacci) give exponential time; memoisation or iteration fixes this.
- Failure Mode 3: Excessive depth. Linear-depth recursion (factorial, array sum, reversal, GCD with input 1) uses $O(n)$ stack versus $O(1)$ for loops, which matters when depth nears the interpreter limit.
- Failure Mode 4: Quicksort with last/first pivot on sorted or all-equal input yields maximally unbalanced partitions, $O(n^2)$ time and $O(n)$ stack.
- Failure Mode 5: Backtracking that fails to undo state (unreset cell, unremoved queen, path mark left in place) corrupts later branches. Maze search without a visited set can cycle.
- Failure Mode 6: Backtracking and Hanoi grow exponentially with input size; Sudoku worst case is exponential even though pruning helps in practice.
- Edge Case Behavior: factorial(0) = 1; array_sum with n = 0 returns 0; reversal of an empty or one-element array returns immediately; empty string or single character is a palindrome; Mergesort and Quicksort on empty or one-element ranges stop at `start >= end`; GCD of equal inputs returns at once; Fibonacci with n < 1 should raise an error; duplicates must not be lost in sorting.
- Trade-off: recursion is shorter and natural for recursive structures (trees, divide and conquer, backtracking). Iteration is typically cheaper in memory. Choose recursion when it is clearer and time and space limits are acceptable; otherwise use iteration.

## 6. High-Yield Verification Checklist

- [ ] What three elements must a correct recursive solution have? -> Base case, recursive step on a smaller instance, and guaranteed progress to the base case.
- [ ] How many frames are active at the deepest point of factorial(4)? -> Five (n = 4, 3, 2, 1, 0).
- [ ] Is `array_sum` tail recursive? -> No, an addition remains after the call returns. `reverse_array` is.
- [ ] What does mystery(4, 5) return? -> 9 (it computes n + m).
- [ ] Why is naive Fibonacci slow, and what are its time and stack costs? -> Overlapping subproblems; $\Theta(\varphi^n)$ time (O(2^n) bound), $O(n)$ stack.
- [ ] Iterative additions for the nth Fibonacci number? -> $n-2$ (versus $F(n)-1$ recursively).
- [ ] How many moves does Hanoi need for n discs? -> $2^n - 1$, from $M(n) = 2M(n-1) + 1$.
- [ ] Why does each subtraction-GCD call make progress? -> The sum of the arguments drops by the smaller value and both stay positive.
- [ ] Mergesort time, depth and space? -> $\Theta(n \log n)$ in all cases, depth $O(\log n)$, auxiliary space $O(n)$ plus $O(\log n)$ stack.
- [ ] Which side should be taken first on equal items to keep Mergesort stable? -> The left range.
- [ ] After partitioning, what is guaranteed about the pivot? -> It is in its final sorted position; neither side is sorted yet.
- [ ] Quicksort worst case and its trigger? -> $O(n^2)$ time, $O(n)$ stack; extreme pivot each time (sorted or all-equal input with a first/last pivot).
- [ ] Binary search base cases? -> `lower > upper` (not found, -1) and `A[mid] == target`.
- [ ] What distinguishes backtracking from plain recursion? -> Explicit undo of the choice after a failed branch, plus pruning invalid choices before recursing.
- [ ] How many solutions does Eight Queens have? -> 92.
- [ ] Does a maze backtracking search find the shortest path? -> No, only a path if one exists.