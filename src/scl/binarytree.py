
from abc import abstractmethod
from collections.abc import Callable, Iterator
from typing import Any, Generic, TypeIs, TypeVar

from scl.tree import T, Node, Tree

from .intervaltree import nonnull
from .util import Comparable


_K = TypeVar('_K', bound=Comparable)


class BinaryNode(Node[T]):

    def __init__(self, value: T) -> None:
        super().__init__(value)
        self.left: BinaryNode[T] | None = None
        self.right: BinaryNode[T] | None = None

    def get_leftmost(self) -> 'BinaryNode[T] | None':
        node = self
        while node.left is not None:
            node = node.left
        return node

    def get_rightmost(self) -> 'BinaryNode[T] | None':
        node = self
        while node.right is not None:
            node = node.right
        return node

    @property
    def next(self) -> 'BinaryNode[T] | None':
        if self.right is not None:
            return self.right.get_leftmost()
        node = self
        while node.parent is not None:
            assert(_is_binary_node(node.parent))
            if node != node.parent.right:
                break
            node = node.parent
        return node.parent

    @property
    def prev(self) -> 'BinaryNode[T] | None':
        if self.left is not None:
            return self.left.get_rightmost()
        node = self
        while node.parent is not None:
            assert(_is_binary_node(node.parent))
            if node != node.parent.left:
                break
            node = node.parent
        return node.parent


def _is_binary_node(value: Any) -> TypeIs[BinaryNode]:
    return True


class BinaryTree(Tree[T], Generic[T, _K]):

    def __init__(self, key: str | Callable[[T], _K] | None = None) -> None:
        super().__init__()
        if key is None:
            get_key = lambda value: value
        elif isinstance(key, str):
            name = key
            get_key = lambda value: getattr(value, name)
        else:
            get_key = key
        self._get_key = get_key

    def get_add_hint(self, value: T) -> Any:
        key = self._get_key(value)
        node = self._root
        assert(_is_binary_node(node))
        while node is not None:
            node_key = self._get_key(node.value)
            if node.left is not None and key < node_key:
                node = node.left
            elif node.right is not None and key > node_key:
                node = node.right
            else:
                break
        return node

    def rotate_left(self, node: BinaryNode[T]) -> BinaryNode[T]:
        """
        Moves `node` to the left, causing `node.right` to become the new root.
        """
        right = nonnull(node.right)
        new_node = right
        if node == self._root:
            self._root = new_node
        else:
            parent = nonnull(node.parent)
            assert(_is_binary_node(parent))
            if parent.left == node:
                parent.left = new_node
            else:
                parent.right = new_node
        new_node.parent = node.parent
        node.right = right.left
        if right.left is not None:
            right.left.parent = node
        right.left = node
        return right

    def rotate_right(self, node: BinaryNode[T]) -> BinaryNode[T]:
        """
        Moves `node` to the right, causing `node.left` to become the new root.
        """
        left = nonnull(node.left)
        new_node = left
        if node == self._root:
            self._root = new_node
        else:
            parent = nonnull(node.parent)
            assert(_is_binary_node(parent))
            if parent.left == node:
                parent.left = new_node
            else:
                parent.right = new_node
        new_node.parent = node.parent
        node.parent = left
        node.left = left.right
        if left.right is not None:
            left.right.parent = node
        left.right = node
        return left

    def rotate_right_then_left(self, x: BinaryNode[T]) -> BinaryNode[T]:

        z = nonnull(x.right)
        y = nonnull(z.left)
        t2 = y.left
        t3 = y.right

        z.left = t3
        if t3 is not None:
            t3.parent = z
        y.right = z
        z.parent = y
        x.right = t2

        # Attach to the parent node
        if t2 is not None:
            t2.parent = x
        if x == self._root:
            self._root = y
        else:
            parent = nonnull(x.parent)
            assert(_is_binary_node(parent))
            if x == parent.left:
                parent.left = y
            else:
                parent.right = y

        y.left = x
        y.parent = x.parent
        x.parent = y

        return y

    def rotate_left_then_right(self, x: BinaryNode[T]) -> BinaryNode[T]:

        z = nonnull(x.left)
        y = nonnull(z.right)
        t2 = y.left
        t3 = y.right

        z.right = t2
        if t2 is not None:
            t2.parent = z
        y.left = z
        z.parent = y
        x.left = t3
        if t3 is not None:
            t3.parent = x

        # Attach to the parent node
        if x == self._root:
            self._root = y
        else:
            parent = nonnull(x.parent)
            assert(_is_binary_node(parent))
            if x == parent.left:
                parent.left = y
            else:
                parent.right = y

        y.right = x
        y.parent = x.parent
        x.parent = y

        return y

    def __iter__(self) -> Iterator[T]:
        if self._root is None:
            return
        assert(_is_binary_node(self._root))
        stack: list[BinaryNode[T]] = [ self._root ]
        while stack:
            node = stack.pop()
            yield node.value
            if node.left is not None:
                stack.append(node.left)
            if node.right is not None:
                stack.append(node.right)

    @abstractmethod
    def add(self, value: T, /, hint: Any) -> None: ...


