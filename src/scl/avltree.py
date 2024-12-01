
from typing import Any, TypeIs

from scl.binarytree import K, BinaryNode, BinaryTree
from scl.util import T, nonnull


class AVLNode(BinaryNode[T]):

    def __init__(self, value: T) -> None:
        super().__init__(value)
        self.balance = 0


def _is_avl_node(value: Any) -> TypeIs[AVLNode]:
    return True


class AVLTree(BinaryTree[T, K]):

    def rotate_left(self, node: BinaryNode[T]) -> BinaryNode[T]:
        right = nonnull(node.right)
        assert(_is_avl_node(node))
        assert(_is_avl_node(right))
        if right.balance == 0:
            node.balance = +1
            right.balance = -1
        else:
            node.balance = 0
            right.balance = 0
        return super().rotate_left(node)

    def rotate_right(self, node: BinaryNode[T]) -> BinaryNode[T]:
        left = nonnull(node.left)
        assert(_is_avl_node(node))
        assert(_is_avl_node(left))
        if left.balance == 0:
            node.balance = -1
            left.balance = +1
        else:
            left.balance = 0
            node.balance = 0
        return super().rotate_right(node)

    def rotate_right_then_left(self, x: BinaryNode[T]) -> BinaryNode[T]:
        z = nonnull(x.left)
        y = nonnull(z.right)
        assert(_is_avl_node(x))
        assert(_is_avl_node(y))
        assert(_is_avl_node(z))
        if y.balance == 0:
            x.balance = 0
            z.balance = 0
        elif y.balance > 0:
            x.balance = -1
            z.balance = 0
        else:
            x.balance = 0
            z.balance = +1
        y.balance = 0
        return super().rotate_right_then_left(x)

    def rotate_left_then_right(self, x: BinaryNode[T]) -> BinaryNode[T]:
        z = nonnull(x.left)
        y = nonnull(z.right)
        assert(_is_avl_node(x))
        assert(_is_avl_node(y))
        assert(_is_avl_node(z))
        if y.balance == 0:
            x.balance = 0
            z.balance = 0
        elif y.balance < 0:
            x.balance = +1
            z.balance = 0
        else:
            x.balance = 0
            z.balance = -1
        y.balance = 0
        return super().rotate_left_then_right(x)

    def add_node(self, node: BinaryNode[T], /, hint: Any = None) -> None:
        assert(_is_avl_node(node))
        super().add_node(node, hint)
        parent = node.parent
        while parent is not None:
            assert(_is_avl_node(parent))
            if node == parent.right:
                if parent.balance > 0:
                    if node.balance < 0:
                        self.rotate_right_then_left(parent)
                    else:
                        self.rotate_left(parent)
                    break
                elif parent.balance < 0:
                        parent.balance = 0
                        break
                else:
                    parent.balance = +1
                    node = parent
            else:
                if parent.balance < 0:
                    if node.balance > 0:
                        self.rotate_left_then_right(parent)
                    else:
                        self.rotate_right(parent)
                    break
                elif parent.balance > 0:
                    parent.balance = 0
                    break
                else:
                    parent.balance  = -1
                    node = parent
            parent = node.parent

    def add(self, value: T, /, hint: Any = None) -> None:
        node = AVLNode(value)
        return self.add_node(node, hint)
