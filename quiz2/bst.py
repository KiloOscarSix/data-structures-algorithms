r"""QUIZ 2 CHEAT SHEET: BINARY SEARCH TREES (Workshop 7 / Worksheet 5).

Run everything:  python3 main_bst.py      (from inside quiz2/)
NOTE: node key is stored in node.value (not node.key / node.data).

TERMS
- Root = level 0. Leaf = no children. Degree = number of children.
- HEIGHT (worksheet convention) = number of NODES on the longest root-to-leaf path:
  empty tree = 0, single node = 1, so height = max level + 1.
- Max nodes in a tree of height h = 2^h - 1. Min height for n nodes = ceil(log2(n+1)).
- Full: every node has 0 or 2 children. Complete: all levels full except the last,
  filled left to right. Perfect: all levels completely full.
- BST rule: left subtree < node < right subtree, distinct keys, DUPLICATES IGNORED.

OPERATIONS (n nodes, h height)
  op                    time                    aux space
  search/insert/delete  O(h)                    O(h) recursion stack (O(1) iterative)
                        balanced h~log2 n -> O(log n); skewed/sorted input h=n -> O(n)
  build from sorted     chain, O(n^2) total to build
  traversals (DFT)      O(n)                    O(h) stack
  BFT (level order)     O(n)                    O(w) queue, w = max width
  count nodes/leaves    O(n)                    O(h)
  are_identical         O(n) worst              O(h); short-circuits on first mismatch
  balance_bst           O(n) (inorder + build)  O(n) key list + O(log n) recursion

SEARCH: each comparison discards a whole subtree (BST rule), moves down one level,
  so at most h comparisons. search_path(60) on EXAMPLE = [50, 70, 60].

DELETE (3 cases):
  1. no child  -> return None (remove)
  2. one child -> return that child (it replaces the node)
  3. two children -> copy INORDER SUCCESSOR (smallest in right subtree: go right once,
     then left all the way) into the node, then delete the successor from the right
     subtree. (Alternative: inorder PREDECESSOR = largest in left subtree.)
  MUST assign back: node.left = _delete(node.left, k) / self.root = _delete(...),
  because the subtree's root may change (e.g. deleting a single-node root -> None).

TRAVERSALS (V visit, L left, R right) on EXAMPLE [50, 30, 20, 40, 70, 60, 80]:
          50
        /    \
      30      70
     /  \    /  \
   20   40  60   80
  preorder  VLR: [50, 30, 20, 40, 70, 60, 80]   (copy a tree / rebuild same shape)
  inorder   LVR: [20, 30, 40, 50, 60, 70, 80]   (ALWAYS ascending for a BST)
  postorder LRV: [20, 40, 30, 60, 80, 70, 50]   (delete/free a tree)
  BFT level:     [50, 30, 70, 20, 40, 60, 80]   (queue: deque append/popleft;
                                                list.pop(0) is O(n) per pop)
  Iterative preorder: push RIGHT before LEFT (stack is LIFO, so left pops first).
  Iterative postorder: two stacks (or reverse of a V R L preorder).
  Skewed [4, 3, 2, 1]: inorder [1,2,3,4], preorder [4,3,2,1], postorder [1,2,3,4].

WORKSHEET ANSWERS TO REMEMBER
- Inorder alone can't tell trees apart (it ignores shape): [1,2,3] vs [2,3,1] both
  give inorder [1,2,3] but different trees. Need preorder+inorder or postorder+inorder
  to rebuild a unique tree.
- [8, 4, 12, 2, 6]: subtree sizes 8:5, 4:3, 12:1, 2:1, 6:1. count = 1 + L + R.
- Leaves: leaf returns 1 (no +1 for internal nodes). In [8, 4, 12, 2], 4 is not a
  leaf (has left child 2). Delete 2 -> 4 becomes a leaf.
- are_identical: both None -> True; one None -> False; else value == AND left AND right.
- Number of distinct BSTs on 3 keys = 5; binary trees on 3 labelled nodes = 30.
- Tree sort = insert all into BST then inorder.
- Balanced from sorted list: middle element = root, recurse on halves.
  Skewed [1..7] height 7 -> 3, BFT [4, 2, 6, 1, 3, 5, 7].

QUIZ VARIANTS (all tested in test_variants): search "VARIANTS" below.
find_min, find_max, insert_iterative, search_iterative, kth_smallest, range_query,
count_in_range, sum_values, depth_of, successor_of, lca, is_bst, count_internal,
nodes_at_level, closest_value, mirror, delete_predecessor, from_preorder_inorder.
"""

from collections import deque  # ONLY import: Worksheet 5 hint explicitly allows deque for BFT


class Node:
    def __init__(self, key: int) -> None:
        self.value: int = key
        self.left: Node | None = None
        self.right: Node | None = None


class BST:
    def __init__(self) -> None:
        self.root: Node | None = None

    # ---------- Exercise 1: CRUD + breadth-first traversal ----------

    def insert(self, key: int) -> None:
        self.root = self._insert(self.root, key)

    def _insert(self, node: Node | None, key: int) -> Node:
        if node is None:
            return Node(key)
        if key < node.value:
            node.left = self._insert(node.left, key)
        elif key > node.value:
            node.right = self._insert(node.right, key)
        return node  # equal key: duplicate ignored

    def search(self, key: int) -> bool:
        return self._search(self.root, key)

    def _search(self, node: Node | None, key: int) -> bool:
        if node is None:
            return False
        if key == node.value:
            return True
        if key < node.value:
            return self._search(node.left, key)
        return self._search(node.right, key)

    def search_path(self, key: int) -> list[int]:
        """Values compared, from the root, while searching for key."""
        path: list[int] = []
        node = self.root
        while node is not None:
            path.append(node.value)
            if key == node.value:
                break
            node = node.left if key < node.value else node.right
        return path

    def delete(self, key: int) -> None:
        self.root = self._delete(self.root, key)

    def _delete(self, node: Node | None, key: int) -> Node | None:
        if node is None:
            return None
        if key < node.value:
            node.left = self._delete(node.left, key)
        elif key > node.value:
            node.right = self._delete(node.right, key)
        elif node.left is None:
            return node.right
        elif node.right is None:
            return node.left
        else:
            successor = node.right
            while successor.left is not None:
                successor = successor.left
            node.value = successor.value
            node.right = self._delete(node.right, successor.value)
        return node

    def bft(self) -> list[int]:
        if self.root is None:
            return []
        output: list[int] = []
        queue: deque[Node] = deque([self.root])
        while queue:
            node = queue.popleft()
            output.append(node.value)
            if node.left is not None:
                queue.append(node.left)
            if node.right is not None:
                queue.append(node.right)
        return output

    # ---------- Exercise 2: depth-first traversals ----------

    def inorder(self) -> list[int]:
        output: list[int] = []
        self._inorder(self.root, output)
        return output

    def _inorder(self, node: Node | None, output: list[int]) -> None:
        if node is None:
            return
        self._inorder(node.left, output)
        output.append(node.value)
        self._inorder(node.right, output)

    def preorder(self) -> list[int]:
        output: list[int] = []
        self._preorder(self.root, output)
        return output

    def _preorder(self, node: Node | None, output: list[int]) -> None:
        if node is None:
            return
        output.append(node.value)
        self._preorder(node.left, output)
        self._preorder(node.right, output)

    def postorder(self) -> list[int]:
        output: list[int] = []
        self._postorder(self.root, output)
        return output

    def _postorder(self, node: Node | None, output: list[int]) -> None:
        if node is None:
            return
        self._postorder(node.left, output)
        self._postorder(node.right, output)
        output.append(node.value)

    def inorder_iterative(self) -> list[int]:
        output: list[int] = []
        stack: list[Node] = []
        current = self.root
        while current is not None or stack:
            while current is not None:
                stack.append(current)
                current = current.left
            current = stack.pop()
            output.append(current.value)
            current = current.right
        return output

    def preorder_iterative(self) -> list[int]:
        if self.root is None:
            return []
        output: list[int] = []
        stack: list[Node] = [self.root]
        while stack:
            node = stack.pop()
            output.append(node.value)
            # Right pushed first so left is popped (visited) first.
            if node.right is not None:
                stack.append(node.right)
            if node.left is not None:
                stack.append(node.left)
        return output

    def postorder_iterative(self) -> list[int]:
        if self.root is None:
            return []
        first: list[Node] = [self.root]
        second: list[Node] = []
        while first:
            node = first.pop()
            second.append(node)
            if node.left is not None:
                first.append(node.left)
            if node.right is not None:
                first.append(node.right)
        return [node.value for node in reversed(second)]

    # ---------- Exercise 3: count nodes ----------

    def count_nodes(self) -> int:
        return self._count_nodes(self.root)

    def _count_nodes(self, node: Node | None) -> int:
        if node is None:
            return 0
        return 1 + self._count_nodes(node.left) + self._count_nodes(node.right)

    # ---------- Exercise 4: count leaves ----------

    def count_leaf_nodes(self) -> int:
        return self._count_leaf_nodes(self.root)

    def _count_leaf_nodes(self, node: Node | None) -> int:
        if node is None:
            return 0
        if node.left is None and node.right is None:
            return 1
        return self._count_leaf_nodes(node.left) + self._count_leaf_nodes(node.right)

    def leaf_values(self) -> list[int]:
        """Leaf values in ascending order (used to check predictions)."""
        return [v for v in self.inorder() if self._is_leaf(self._find(self.root, v))]

    def _find(self, node: Node | None, key: int) -> Node | None:
        while node is not None and node.value != key:
            node = node.left if key < node.value else node.right
        return node

    @staticmethod
    def _is_leaf(node: Node | None) -> bool:
        return node is not None and node.left is None and node.right is None

    # ---------- Exercise 5: identical trees ----------

    def are_identical(self, other_tree: "BST") -> bool:
        return self._are_identical(self.root, other_tree.root)

    def _are_identical(self, node_a: Node | None, node_b: Node | None) -> bool:
        if node_a is None and node_b is None:
            return True
        if node_a is None or node_b is None:
            return False
        return (
            node_a.value == node_b.value
            and self._are_identical(node_a.left, node_b.left)
            and self._are_identical(node_a.right, node_b.right)
        )

    # ---------- Exercise 6 (advanced): balance ----------

    def height(self) -> int:
        return self._height(self.root)

    def _height(self, node: Node | None) -> int:
        if node is None:
            return 0
        return 1 + max(self._height(node.left), self._height(node.right))

    def balance_bst(self) -> None:
        keys = self.inorder()  # sorted, O(n)
        self.root = self._build_balanced(keys, 0, len(keys) - 1)

    def _build_balanced(self, keys: list[int], lo: int, hi: int) -> Node | None:
        if lo > hi:
            return None
        mid = (lo + hi) // 2
        node = Node(keys[mid])
        node.left = self._build_balanced(keys, lo, mid - 1)
        node.right = self._build_balanced(keys, mid + 1, hi)
        return node

    # ================= VARIANTS (likely quiz twists, all tested) =================

    def find_min(self) -> int:
        """Go left until you can't. O(h)."""
        if self.root is None:
            raise ValueError("empty")
        node = self.root
        while node.left is not None:
            node = node.left
        return node.value

    def find_max(self) -> int:
        """Go right until you can't. O(h)."""
        if self.root is None:
            raise ValueError("empty")
        node = self.root
        while node.right is not None:
            node = node.right
        return node.value

    def insert_iterative(self, key: int) -> None:
        """Same as insert, no recursion: O(h) time, O(1) space."""
        new = Node(key)
        if self.root is None:
            self.root = new
            return
        node = self.root
        while True:
            if key < node.value:
                if node.left is None:
                    node.left = new
                    return
                node = node.left
            elif key > node.value:
                if node.right is None:
                    node.right = new
                    return
                node = node.right
            else:
                return  # duplicate ignored

    def search_iterative(self, key: int) -> bool:
        node = self.root
        while node is not None:
            if key == node.value:
                return True
            node = node.left if key < node.value else node.right
        return False

    def kth_smallest(self, k: int) -> int:
        """k-th smallest (1-based) = k-th value of the inorder traversal. O(h + k)."""
        stack: list[Node] = []
        current = self.root
        count = 0
        while current is not None or stack:
            while current is not None:
                stack.append(current)
                current = current.left
            current = stack.pop()
            count += 1
            if count == k:
                return current.value
            current = current.right
        raise IndexError(k)

    def range_query(self, lo: int, hi: int) -> list[int]:
        """Sorted keys in [lo, hi]. Prunes subtrees that can't contain matches."""
        out: list[int] = []

        def walk(node: Node | None) -> None:
            if node is None:
                return
            if lo < node.value:  # left side may still hold keys >= lo
                walk(node.left)
            if lo <= node.value <= hi:
                out.append(node.value)
            if node.value < hi:  # right side may still hold keys <= hi
                walk(node.right)

        walk(self.root)
        return out

    def count_in_range(self, lo: int, hi: int) -> int:
        return len(self.range_query(lo, hi))

    def sum_values(self) -> int:
        def s(node: Node | None) -> int:
            if node is None:
                return 0
            return node.value + s(node.left) + s(node.right)

        return s(self.root)

    def depth_of(self, key: int) -> int:
        """Level of key (root = 0), or -1 if absent. O(h)."""
        node, level = self.root, 0
        while node is not None:
            if key == node.value:
                return level
            node = node.left if key < node.value else node.right
            level += 1
        return -1

    def successor_of(self, key: int) -> int | None:
        """Smallest key > key (None if none). O(h): last left turn, or right min."""
        node, best = self.root, None
        while node is not None:
            if key < node.value:
                best = node.value  # candidate; try for a smaller one on the left
                node = node.left
            else:
                node = node.right
        return best

    def predecessor_of(self, key: int) -> int | None:
        """Largest key < key (None if none). O(h)."""
        node, best = self.root, None
        while node is not None:
            if key > node.value:
                best = node.value
                node = node.right
            else:
                node = node.left
        return best

    def lca(self, a: int, b: int) -> int | None:
        """Lowest common ancestor: first node where a and b split. O(h)."""
        node = self.root
        while node is not None:
            if a < node.value and b < node.value:
                node = node.left
            elif a > node.value and b > node.value:
                node = node.right
            else:
                return node.value
        return None

    def is_bst(self) -> bool:
        """Valid BST check with min/max bounds (checking only parent-child is WRONG)."""

        def check(node: Node | None, lo: float, hi: float) -> bool:
            if node is None:
                return True
            if not lo < node.value < hi:
                return False
            return check(node.left, lo, node.value) and check(
                node.right, node.value, hi
            )

        return check(self.root, float("-inf"), float("inf"))

    def count_internal(self) -> int:
        """Non-leaf nodes = count_nodes - count_leaf_nodes."""
        return self.count_nodes() - self.count_leaf_nodes()

    def nodes_at_level(self, level: int) -> list[int]:
        """Values at a given level (root = 0), left to right."""
        out: list[int] = []

        def walk(node: Node | None, d: int) -> None:
            if node is None:
                return
            if d == level:
                out.append(node.value)
                return
            walk(node.left, d + 1)
            walk(node.right, d + 1)

        walk(self.root, 0)
        return out

    def closest_value(self, target: int) -> int:
        """Key nearest target (smaller wins ties). O(h)."""
        if self.root is None:
            raise ValueError("empty")
        node: Node | None = self.root
        best = self.root.value
        while node is not None:
            if abs(node.value - target) < abs(best - target) or (
                abs(node.value - target) == abs(best - target) and node.value < best
            ):
                best = node.value
            node = node.left if target < node.value else node.right
        return best

    def mirror(self) -> None:
        """Swap every left/right (result is a 'reverse' BST: inorder descending)."""

        def m(node: Node | None) -> None:
            if node is None:
                return
            node.left, node.right = node.right, node.left
            m(node.left)
            m(node.right)

        m(self.root)

    def delete_predecessor(self, key: int) -> None:
        """Delete, using the inorder PREDECESSOR (max of left) for the 2-child case."""

        def d(node: Node | None, k: int) -> Node | None:
            if node is None:
                return None
            if k < node.value:
                node.left = d(node.left, k)
            elif k > node.value:
                node.right = d(node.right, k)
            elif node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            else:
                pred = node.left
                while pred.right is not None:  # largest in left subtree
                    pred = pred.right
                node.value = pred.value
                node.left = d(node.left, pred.value)
            return node

        self.root = d(self.root, key)

    @staticmethod
    def from_preorder_inorder(pre: list[int], ino: list[int]) -> "BST":
        """Rebuild a tree: pre[0] is the root; split inorder around it."""

        def b(pre: list[int], ino: list[int]) -> Node | None:
            if not pre:
                return None
            root = Node(pre[0])
            i = ino.index(pre[0])  # i nodes in the left subtree
            root.left = b(pre[1 : i + 1], ino[:i])
            root.right = b(pre[i + 1 :], ino[i + 1 :])
            return root

        tree = BST()
        tree.root = b(pre, ino)
        return tree


# ---------- Tests ----------
# ruff: noqa: S101, T201, PLR2004, PT018, SLF001
# pyright: reportPrivateUsage=false

EXAMPLE = [50, 30, 20, 40, 70, 60, 80]


def build(keys: list[int]) -> BST:
    tree = BST()
    for key in keys:
        tree.insert(key)
    return tree


def is_valid_bst(tree: BST) -> bool:
    def check(node: Node | None, lo: float, hi: float) -> bool:
        if node is None:
            return True
        if not lo < node.value < hi:
            return False
        return check(node.left, lo, node.value) and check(node.right, node.value, hi)

    return check(tree.root, float("-inf"), float("inf"))


def root_value(tree: BST) -> int | None:
    return None if tree.root is None else tree.root.value


def test_crud() -> None:
    tree = build(EXAMPLE)
    rows: list[tuple[str, object]] = [
        ("search(40)", tree.search(40)),
        ("search(100)", tree.search(100)),
    ]
    tree.insert(40)
    rows.append(("insert(40)", None))
    for key in (20, 30, 50):
        tree.delete(key)
        rows.append((f"delete({key})", None))
        assert is_valid_bst(tree)
    print("Prediction table replayed:")
    replay = build(EXAMPLE)
    for op, ret in rows:
        name, arg = op.rstrip(")").split("(")
        result = getattr(replay, name)(int(arg))
        assert result == ret
        keys = replay.inorder()
        print(f"  {op:<12} -> {result!s:<5} root={root_value(replay)} keys={keys}")
        assert is_valid_bst(replay)
    assert replay.inorder() == [40, 60, 70, 80]
    assert root_value(replay) == 60

    assert build(EXAMPLE).search_path(60) == [50, 70, 60]
    print("  search_path(60) on original tree:", build(EXAMPLE).search_path(60))

    empty = BST()
    assert not empty.search(1)
    empty.delete(1)  # absent key, empty tree
    assert empty.root is None and empty.bft() == []
    print("Empty tree: search False, delete no-op, bft [] OK")

    single = build([5])
    assert single.search(5) and single.bft() == [5]
    single.delete(5)
    assert single.root is None
    print("Single node: delete root -> empty OK")

    dup = build(EXAMPLE)
    dup.insert(30)
    assert dup.inorder() == sorted(EXAMPLE)
    print("Duplicate insert ignored OK")

    absent = build(EXAMPLE)
    absent.delete(99)
    assert absent.bft() == build(EXAMPLE).bft()
    print("Delete absent key leaves tree unchanged OK")

    leaf = build(EXAMPLE)
    leaf.delete(80)  # leaf
    assert leaf.bft() == [50, 30, 70, 20, 40, 60]
    one = build([50, 30, 20, 70])
    one.delete(30)  # one child (left)
    assert one.bft() == [50, 20, 70] and is_valid_bst(one)
    two = build(EXAMPLE)
    two.delete(50)  # root, two children -> successor 60
    assert two.bft() == [60, 30, 70, 20, 40, 80] and is_valid_bst(two)
    print("Delete leaf / one child / two children (root) OK")
    print("bft of original:", build(EXAMPLE).bft())


def test_traversals() -> None:
    tree = build(EXAMPLE)
    print("inorder  :", tree.inorder())
    print("preorder :", tree.preorder())
    print("postorder:", tree.postorder())
    assert tree.inorder() == [20, 30, 40, 50, 60, 70, 80]
    assert tree.preorder() == [50, 30, 20, 40, 70, 60, 80]
    assert tree.postorder() == [20, 40, 30, 60, 80, 70, 50]
    for keys in ([], [8], EXAMPLE, [1, 2, 3, 4], [4, 3, 2, 1]):
        t = build(keys)
        before = t.bft()
        assert t.inorder() == t.inorder_iterative() == sorted(keys)
        assert t.preorder() == t.preorder_iterative()
        assert t.postorder() == t.postorder_iterative()
        for out in (t.inorder(), t.preorder(), t.postorder()):
            assert sorted(out) == sorted(keys)  # every key exactly once
        assert t.bft() == before  # tree unchanged
    print("recursive == iterative (empty, single, balanced, skewed): OK")


def test_count_nodes() -> None:
    cases = {(): 0, (8,): 1, (8, 4, 12, 2, 6): 5, (1, 2, 3, 4): 4, (5, 5, 5): 1}
    for keys, expected in cases.items():
        actual = build(list(keys)).count_nodes()
        print(f"  {list(keys)!s:<18} count={actual}")
        assert actual == expected
    tree = build([8, 4, 12, 2, 6])
    assert tree._count_nodes(tree.root.left if tree.root else None) == 3
    tree.insert(10)
    assert tree.count_nodes() == 6
    tree.insert(10)
    assert tree.count_nodes() == 6
    tree.delete(4)
    assert tree.count_nodes() == 5
    tree.delete(99)
    assert tree.count_nodes() == 5
    assert tree.count_nodes() == tree.count_nodes()
    print("insert 10 -> 6, dup 10 -> 6, delete 4 -> 5, delete 99 -> 5: OK")


def test_count_leaf_nodes() -> None:
    cases = {
        (): [],
        (8,): [8],
        (8, 4, 12, 2, 6): [2, 6, 12],
        (1, 2, 3, 4): [4],
        (8, 4, 12, 2): [2, 12],
        (4, 3, 2, 1): [1],
    }
    for keys, leaves in cases.items():
        t = build(list(keys))
        count = t.count_leaf_nodes()
        print(f"  {list(keys)!s:<18} leaves={t.leaf_values()} count={count}")
        assert t.leaf_values() == leaves
        assert t.count_leaf_nodes() == len(leaves)
    tree = build([8, 4, 12, 2])
    tree.delete(2)
    assert tree.leaf_values() == [4, 12] and tree.count_leaf_nodes() == 2
    tree.delete(99)
    assert tree.count_leaf_nodes() == 2
    print("[8, 4, 12, 2] delete 2 -> leaves [4, 12], count 2; delete 99 -> 2: OK")


def test_are_identical() -> None:
    cases = [
        ([], [], True),
        ([], [2], False),
        ([1, 2, 3], [2, 3, 1], False),
        ([2, 1, 3], [2, 3, 1], True),
        ([2, 1, 3], [2, 1, 4], False),
    ]
    for a, b, expected in cases:
        actual = build(a).are_identical(build(b))
        print(f"  {a!s:<10} vs {b!s:<10} -> {actual}")
        assert actual == expected
    tree = build(EXAMPLE)
    assert tree.are_identical(tree)
    assert tree.are_identical(build(EXAMPLE))
    # Same root and left subtree, different right subtree.
    assert not tree.are_identical(build([50, 30, 20, 40, 70, 60, 90]))
    print("self, separate copy, differing right subtree: OK")


def test_balance_bst() -> None:
    skewed = build(list(range(1, 8)))
    assert skewed.height() == 7
    skewed.balance_bst()
    print("[1..7] skewed: height 7 ->", skewed.height(), "bft", skewed.bft())
    assert skewed.height() == 3 and skewed.inorder() == list(range(1, 8))
    assert skewed.bft() == [4, 2, 6, 1, 3, 5, 7] and is_valid_bst(skewed)
    for n in (0, 1, 2, 10, 100):
        t = build(list(range(n)))
        t.balance_bst()
        assert t.count_nodes() == n and is_valid_bst(t)
        assert t.height() == n.bit_length()  # ceil(log2(n + 1)), the minimum
    print("balance_bst: minimum height for n = 0, 1, 2, 10, 100 OK")


def test_variants() -> None:
    t = build(EXAMPLE)
    assert t.find_min() == 20 and t.find_max() == 80
    it = BST()
    for k in EXAMPLE + [30]:
        it.insert_iterative(k)
    assert it.are_identical(t) and it.search_iterative(60) and not it.search_iterative(65)
    assert [t.kth_smallest(k) for k in (1, 4, 7)] == [20, 50, 80]
    assert t.range_query(35, 70) == [40, 50, 60, 70] and t.count_in_range(0, 25) == 1
    assert t.sum_values() == 350
    assert (t.depth_of(50), t.depth_of(70), t.depth_of(60), t.depth_of(99)) == (0, 1, 2, -1)
    assert t.successor_of(40) == 50 and t.successor_of(80) is None
    assert t.predecessor_of(60) == 50 and t.predecessor_of(20) is None
    assert t.lca(20, 40) == 30 and t.lca(20, 80) == 50 and t.lca(60, 70) == 70
    assert t.is_bst() and t.count_internal() == 3
    assert t.nodes_at_level(2) == [20, 40, 60, 80]
    assert t.closest_value(44) == 40 and t.closest_value(66) == 70
    re = BST.from_preorder_inorder(t.preorder(), t.inorder())
    assert re.are_identical(t)
    m = build(EXAMPLE)
    m.mirror()
    assert m.inorder() == sorted(EXAMPLE, reverse=True) and not m.is_bst()
    p = build(EXAMPLE)
    p.delete_predecessor(50)
    assert root_value(p) == 40 and p.is_bst() and p.inorder() == [20, 30, 40, 60, 70, 80]
    print("variants: min/max, iterative, kth, range, depth, succ/pred, lca, rebuild OK")
