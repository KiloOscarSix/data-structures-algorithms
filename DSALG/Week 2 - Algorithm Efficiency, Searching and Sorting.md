## 1. Core Thesis & Problem Space

- Problem Statement: Compare algorithms solving the same problem by how the work they perform grows with input size n, and apply this to stack/queue array implementations, loop structures, and the elementary sorting and searching algorithms.
- Central Hypothesis / Approach: Count repetitions, include the cost of the loop body, then keep the dominant term and drop constant coefficients and lower-order terms to obtain a Big-O bound. Function calls inside loops must be costed too.
- Core System Invariant: Big-O is an asymptotic upper bound, not an exact running time. Total cost = (number of repetitions) x (cost per repetition). Binary search additionally requires sorted data and O(1) access by index.

## 2. Technical Vocabulary & Formal Definitions

- Big-O: Asymptotic upper bound on growth of work with input size n. Tightest simple bound is reported.
- Dominant term: Term of the operation-count function that grows fastest as n grows; it alone determines the Big-O class.
- Complexity classes: O(1) constant, O(log n) logarithmic, O(n) linear, O(n log n) linearithmic, O(n^2) quadratic, O(n^3) cubic, O(2^n) exponential.
- Best, worst, average case: Minimum, maximum and expected work over inputs of size n (average assumes each target position is equally likely).
- Auxiliary space: Extra memory beyond the input; O(1) for in-place algorithms.
- In-place sort: Sorts by swapping or shifting within the input list.
- Sorted prefix: Left part of the list already in final order (selection, insertion sort).
- Pass: One full traversal of the active range in an iterative algorithm.
- Early-exit flag: Boolean reset each pass and cleared on any swap; a pass with no swaps terminates bubble sort.
- Probe: One inspection of a list element during a search.
- Circular queue: Array treated as a ring so head and tail indices wrap around, reusing freed positions.
- Elementary sorts: Selection, bubble, insertion; two nested loops, O(n^2).
- Advanced sorts: O(n log n) comparisons (merge sort, heapsort). Quicksort is O(n log n) average, O(n^2) worst. Shellsort depends on gap sequence.

## 3. System Mechanics & Governing Principles

- Operation counting (sum of first n integers):
    - A (single loop): n+1 assignments + n additions = 2n+1, O(n).
    - B (dependent nested loop): 1 + n(n+1)/2 assignments + n(n+1)/2 additions = n^2+n+1, O(n^2).
    - C (closed form n(n+1)/2): 4 operations, O(1).
- Loop patterns:
    - Linear loop, step k=k+1 or k=k+2: iterations proportional to n, O(n). Constant step size changes the coefficient only.
    - Logarithmic loop, k=k*2: iterations $\log_2 n$ (n=1000 gives about 10), O(log n). Base is the multiplier.
    - Independent nested loops, n by n: $n \cdot n = n^2$, O(n^2).
    - Dependent nested loop, inner bound is outer index:  
        $$\sum_{k=1}^{n} k = \frac{n(n+1)}{2}$$  
        Where average inner iterations = (n+1)/2; result O(n^2).
    - Linear outer, logarithmic inner (independent): $n \log_2 n$, O(n log n).
- Composition rules:
    - Sequential loops add; keep the larger (two passes = 2n = O(n); loops over n then m = O(n+m)).
    - Loop with a call in the body: if call is O(1) total O(n); if call is O(n) total O(n^2); if call is O(n^2) in a log loop total O(n^2 log n).
    - Nested loop followed by a single loop: O(n^2) + O(n) = O(n^2).
- Growth behaviour: n doubles gives n^2 x4, n^3 x8, n log n slightly more than x2, log n adds a constant, 2^n squares. At n=10^6, n log2 n is about 2x10^7 versus n^2 = 10^12.
- Doubling-ratio estimation: time ratio 2 when n doubles implies O(n); ratio 4 implies O(n^2); ratio 8 implies O(n^3).
- Time estimate: steps x unit time. n=1000, O(n^2), 1 ns per step gives $10^6 \times 10^{-9}$ s = 1 ms. O(n^3) gives $10^9 \times 10^{-9}$ s = 1 s.
- Stack on fixed-capacity array (n stored items), top index marks the end:
    - Push O(1), Pop O(1), Peek O(1); no data movement.
- Queue on fixed-capacity array:
    - Method 1, head fixed at index 0: Enqueue O(1); Dequeue O(n) because all remaining items shift forward.
    - Method 2, head and tail indices advance, no shifting: Enqueue O(1), Dequeue O(1); leaves unused positions at the front and wastes storage.
    - Method 3, circular array: Enqueue O(1), Dequeue O(1); freed positions are reused. The same ADT operation has different cost depending on implementation.
- Linear search (any order, one-off search in unsorted data may beat sort-then-search):
    
    ```python
    def linear_search(List, value):    for index, item in enumerate(List):        if item == value:            return index    return -1
    ```
    
    - Best O(1) (first item), worst O(n) (last item or absent, n comparisons), average O(n) with (n+1)/2 comparisons on success. Auxiliary space O(1).
- Binary search (sorted data, O(1) index access):
    
    ```python
    def binary_search(List, value):    lower, upper = 0, len(List) - 1    while lower <= upper:        midpoint = (lower + upper) // 2        if List[midpoint] == value:            return midpoint        elif value < List[midpoint]:            upper = midpoint - 1        else:            lower = midpoint + 1    return -1
    ```
    
    - Each unsuccessful probe discards half the range. Best O(1), worst and average O(log n), worst-case iterations $1+\log_2 n$. Iterative auxiliary space O(1). Recursive version uses O(log n) stack depth.
    - n=1000 (<2^10): at most 10 iterations; n=10^6 (<2^20): at most 20 iterations. Linear search averages about 500 and 500,000 comparisons on success, and 1000 and 1,000,000 when absent.
- Selection sort: sorted prefix on the left; each pass finds index of minimum in unsorted part and swaps it into position i.
    
    ```python
    def selection_sort(List):    n = len(List)    for i in range(n - 1):        index_smallest = i        for j in range(i + 1, n):            if List[j] < List[index_smallest]:                index_smallest = j        if index_smallest != i:            List[i], List[index_smallest] = List[index_smallest], List[i]
    ```
    
    - Comparisons: $\frac{n(n-1)}{2}$ always (pass i makes n-1-i comparisons). Best, average, worst O(n^2). Space O(1). Descending order: select the maximum, or flip the comparison.
- Bubble sort: compare adjacent pairs, swap if out of order; each pass bubbles the largest item to the end of the active range.
    
    ```python
    def bubble_sort(List):    n = len(List)    sorted = False    while not sorted:        sorted = True        for j in range(n - 1):            if List[j] > List[j + 1]:                List[j], List[j + 1] = List[j + 1], List[j]                sorted = False        n -= 1
    ```
    
    - Basic version: n-1 full passes of n-1 comparisons, O(n^2) in all cases, no early exit.
    - Early-exit version: best O(n) (one pass, no swaps), average and worst O(n^2). Shrinking n each pass is safe because the largest remaining item is already placed. Space O(1).
- Insertion sort: sorted prefix grows; save the item, shift larger prefix items right, drop the item into the gap.
    
    ```python
    def insertion_sort(List):    for i in range(len(List)):        item_to_insert = List[i]        index_hole = i        while index_hole > 0 and List[index_hole - 1] > item_to_insert:            List[index_hole] = List[index_hole - 1]            index_hole -= 1        List[index_hole] = item_to_insert
    ```
    
    - Best O(n) (already sorted, no shifts), worst O(n^2) (distinct items in reverse, about $n(n-1)/2$ shifts). Space O(1). Efficient for nearly sorted input and for adding items to an existing sorted list. The condition order `index_hole > 0 and ...` prevents negative indexing.
- Summary of sort cases:
    - Selection: best, average, worst all O(n^2).
    - Bubble basic: all O(n^2). Bubble with flag: best O(n), worst O(n^2).
    - Insertion: best O(n), worst O(n^2).
    - Every elementary sort uses O(1) auxiliary space.

## 4. Visual & Structural Logic

- Growth chart: Input N on x-axis -> plot n^2, n log2 n, n, log2 n -> n^2 rises steeply (about 625 at N=25), n log2 n reaches about 280 at N=50, n is linear, log2 n is nearly flat.
- Growth table (n = 1, 2, 4, 8, 16, 32): log2 n = 0,1,2,3,4,5; n log2 n = 0,2,8,24,64,160; n^2 = 1,4,16,64,256,1024; 2^n = 2,4,16,256,65536,4294967296.
- Circular queue: array indices form a ring -> Enqueue increments Tail modulo capacity, Dequeue increments Head modulo capacity -> occupied cells lie between Head and Tail with wraparound; no element movement.
- Selection sort trace on [4,6,7,5,9,3,1,8,2]: min index 6 swapped with index 0, then min 2 swapped to index 1, then 3, 4, 5, 6, with the pass at index 6 needing no swap -> sorted prefix grows by one per pass.
- Selection trace on [5,2,4,1,3]: pass 1 min 1 -> [1,2,4,5,3]; pass 2 min 2 -> [1,2,4,5,3]; pass 3 min 3 -> [1,2,3,5,4]; pass 4 min 4 -> [1,2,3,4,5].
- Bubble trace on [6,1,2,3,4,5]: pass 1 swaps 6 past 1,2,3,4,5 -> [1,2,3,4,5,6]; a second pass makes no swaps and confirms sorted.
- Insertion trace on [16,5] after prefix [1,3,7,9]: 16>5 shift, 9>5 shift, 7>5 shift, 3<5 stop -> insert 5 at index 2.
- Insertion trace on [5,2,4,1,3]: i=1 -> [2,5,4,1,3]; i=2 -> [2,4,5,1,3]; i=3 -> [1,2,4,5,3]; i=4 -> [1,2,3,4,5].
- Binary search trace for 67 in [10,12,18,22,31,34,40,46,59,67,69,72,80,84,98]: lower=0, upper=14, mid=7 (46) -> lower=8; mid=11 (72) -> upper=10; mid=9 (67) found. Three probes.
- Binary search for 82 in the same list: mid=7 (46) -> lower=8; mid=11 (72) -> lower=12; mid=13 (84) -> upper=12; mid=12 (80) -> lower=13 > upper=12, not found. Four probes. Linear search needs 15 probes (absent).
- Binary search for 23 in [2,5,8,12,16,23,38,56,72,91]: L=0,H=9,M=4 (16) -> L=5; M=7 (56) -> H=6; M=5 (23) found, returns 5.
- Recursive binary search: call (arr, start, end, item) -> empty range raises or returns not-found; else compute mid, match returns mid, otherwise recurse on one smaller range and return that result. Each call must shrink the range; the caller must return the recursive result.

## 5. Failure Modes, Edge Cases, & Bottlenecks

- Failure Mode 1: Counting only loop iterations. A loop of n iterations calling an O(n) function is O(n^2), not O(n).
- Failure Mode 2: Binary search on unsorted data gives wrong results, since discarding half relies on order. It also degrades if index access is not O(1).
- Failure Mode 3: Fixed-head array queue has O(n) dequeue due to shifting. Head/tail-advancing queue wastes front positions unless made circular.
- Failure Mode 4: Basic bubble sort and selection sort do full O(n^2) work on already sorted input. Selection sort makes n(n-1)/2 comparisons regardless.
- Failure Mode 5: Insertion sort worst case is reverse-sorted distinct items; bubble sort worst case similar.
- Failure Mode 6: Binary search bound updated to `mid` instead of `mid+1` or `mid-1` can loop forever on a two-item list.
- Failure Mode 7: Bubble early-exit flag not reset each pass, or concluding sorted after a single pair needing no swap, ends the sort prematurely.
- Failure Mode 8: Same Big-O does not mean same speed: steps of 1 versus 2 in a linear loop both O(n) yet differ by a constant factor 2.
- Edge Case Behavior:
    - Linear search absent target or last-position target is worst case n comparisons; returns -1.
    - Binary search empty list returns not found immediately; duplicates may return any matching index.
    - Sorting: empty list and single item are no-ops; duplicates must be preserved; negative values compare normally.
    - Linear search remains valid on unsorted data; the index of a value can change after sorting.
    - Binary search does not always use fewer probes than linear search for every individual target (for example, a target at index 0 favours linear).
- Exercise results:
    - Single loop printing n: O(n). Loop calling O(n) Test: O(n^2). Doubling loop calling O(n^2) Test: O(n^2 log n). Triple nested loop to n: O(n^3).
    - Two loops in a row to n and m: O(n+m); if both go to n, O(n). Nested loop then single loop: O(n^2). Inner loop `range(n, i, -1)`: about n(n-1)/2, O(n^2).
    - f constant in a loop: O(n). g linear in its parameter in a loop over i: O(n^2) (sum of i).
    - Runtime 512, 1024, 2048 ms for doubling n: O(n). Runtime 512, 2048, 8192 ms (x4 per doubling): O(n^2).
    - 11(a): i halves (log n) x j doubles (log n) x k step 2 (n/2): O(n log^2 n). 11(c): outer k doubles (log n), i runs k times, inner loops O(n) plus O(log n) per i, giving about $\sum 2^m n$ dominated by the last term: O(n^2).
    - Code with nested n by n loops calling random_value, then good_sort(a) inside the outer loop: inner loop O(n) plus O(n log n) sort per outer iteration, total O(n^2 log n).
- Wedding exercise: pour champagne into n glasses O(n); toast O(1); clink with everybody O(n); everybody does so collectively O(n^2).

## 6. High-Yield Verification Checklist

- [ ] What are the costs of push, pop and peek on a fixed-capacity array stack? -> All O(1); top index gives direct access with no data movement.
- [ ] Why is dequeue O(n) when the head is fixed at index 0, and how is it made O(1)? -> All items shift forward. Advance a Head index instead, and use a circular array to reuse freed slots.
- [ ] Why is $2n+1$ reported as O(n) and $n^2+n+1$ as O(n^2)? -> Keep the dominant term and drop coefficients and lower-order terms.
- [ ] How many iterations does a loop with `k = k * 2` run for n = 1000? -> About $\log_2 1000 \approx 10$, so O(log n).
- [ ] What is the complexity of a dependent nested loop whose inner bound is the outer index? -> $n(n+1)/2$ iterations, O(n^2).
- [ ] What is the complexity of a loop of n iterations calling an O(n^2) routine? -> O(n^3).
- [ ] How many comparisons does selection sort make, and does input order matter? -> $n(n-1)/2$ always, so best, average and worst are all O(n^2).
- [ ] What is bubble sort's best case and what enables it? -> O(n) with the early-exit flag: one pass with no swaps; the basic version stays O(n^2).
- [ ] When is insertion sort best and worst? -> Best O(n) on already sorted input; worst O(n^2) on reverse-sorted distinct items.
- [ ] What are the linear search best, worst and average cases? -> O(1), O(n), O(n) with (n+1)/2 comparisons on average for a successful search.
- [ ] What does binary search require and what is its worst-case iteration count? -> Sorted data and O(1) index access; $1+\log_2 n$ iterations, O(log n).
- [ ] How many probes does binary search need for 67 and for 82 in the 15-element list? -> 3 for 67 and 4 for 82 (absent).
- [ ] If runtime goes 512, 2048, 8192 ms as n doubles, what is the complexity? -> O(n^2), since time quadruples per doubling.
- [ ] What is the auxiliary space of the three elementary sorts and iterative searches? -> O(1).
- [ ] Why can the loop `i=i+1` with `test(data)` not be assumed O(n)? -> Total cost is iterations times per-call cost; an O(n) call makes it O(n^2).