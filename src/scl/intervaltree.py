
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any, Generic, TypeIs, TypeVar, cast

from scl.tree import Node

from .util import Comparable, nonnull
from .binarytree import BinaryTree, BinaryNode


class PointLike(Comparable):
    pass


Point = TypeVar('Point', bound=PointLike)
Data = TypeVar('Data', default=None)


@dataclass(frozen=True)
class Interval(Generic[Point, Data]):

    start: Point
    stop: Point
    data: Data | None = None

    @staticmethod
    def overlaps(a: 'Interval[Point, Any]', b: 'Interval[Point, Any]') -> bool:
        return a.stop >= b.start and a.start <= b.stop


class IntervalNode(BinaryNode[Interval[Point, Data]], Generic[Point, Data]):

    def __init__(self, value: Interval[Point, Data]) -> None:
        super().__init__(value)
        self.max = value.stop

    def update_max(self) -> None:
        new_max = self.value.stop
        assert(_is_optional_interval_node(self.left))
        assert(_is_optional_interval_node(self.right))
        if self.left is not None and cast(IntervalNode, self.left).max > new_max:
            new_max = self.left.max
        if self.right is not None and self.right.max > new_max:
            new_max = self.right.max
        self.max = new_max


def _is_optional_interval_node(value: Any) -> TypeIs[IntervalNode | None]:
    return True


def _is_interval_node(value: Any) -> TypeIs[IntervalNode]:
    return True


def _as_interval_node(value: Node[Interval[Point, Data]]) -> IntervalNode[Point, Data]:
    return cast(IntervalNode[Point, Data], value)


def _as_optional_interval_node(value: Node[Interval[Point, Data]] | None) -> IntervalNode[Point, Data] | None:
    return cast(IntervalNode[Point, Data] | None, value)


class IntervalTree(BinaryTree[Interval[Point, Data], Point]):

    def __init__(self, values: Iterable[Interval[Point, Data]] | None = None) -> None:
        super().__init__()
        self._count = 0
        if values is not None:
            for value in values:
                self.add(value)

    def rotate_left(self, node: BinaryNode[Interval[Point, Data]]) -> BinaryNode[Interval[Point, Data]]:
        right = nonnull(node.right)
        assert(_is_interval_node(node))
        assert(_is_interval_node(right))
        super().rotate_left(node)
        node.update_max()
        right.update_max()
        return right

    def rotate_right(self, node: BinaryNode[Interval[Point, Data]]) -> BinaryNode[Interval[Point, Data]]:
        left = nonnull(node.left)
        assert(_is_interval_node(node))
        assert(_is_interval_node(left))
        super().rotate_right(node)
        node.update_max()
        left.update_max()
        return left

    def rotate_right_then_left(self, x: BinaryNode[Interval[Point, Data]]) -> BinaryNode[Interval[Point, Data]]:
        return super().rotate_right_then_left(x)

    def rotate_left_then_right(self, x: BinaryNode[Interval[Point, Data]]) -> BinaryNode[Interval[Point, Data]]:
        return super().rotate_left_then_right(x)

    def get_add_hint(self, value: Interval[Point, Data]) -> Any:
        key = value.stop
        assert(_is_interval_node(self._root))
        node = self._root
        while node is not None:
            if node.left is not None and key < node.value.stop:
                node = node.left
            elif node.right is not None and key > node.value.stop:
                node = node.right
            else:
                break
        return node

    def add(self, value: Interval[Point, Data], hint: Any = None) -> tuple[bool, Any]: # type: ignore
        parent = cast(IntervalNode[Point, Data], hint) if hint is not None else self.get_add_hint(value)
        if parent is None:
            self._root = IntervalNode(value)
            self._count += 1
            return True, self._root
        node = IntervalNode(value)
        if value.stop < parent.value.stop:
            parent.left = node
        else:
            parent.right = node
        node.parent = parent
        self._count += 1
        return True, node

    def overlapping(self, interval: Interval[Point, Data]) -> Iterable[Interval[Point, Data]]:
        x = _as_optional_interval_node(self._root)
        while x is not None and not Interval.overlaps(x.value, interval):
            assert(_is_optional_interval_node(x.left))
            if x.left is not None and x.left.max >= interval.start:
                x = x.left
            else:
                x = x.right
        while x is not None:
            yield x.value
            if not Interval.overlaps(x.value, interval):
                break
            x = x.next

    def addi(self, start: Point, stop: Point, data: Data | None = None):
        self.add(Interval(start, stop, data))

    def __contains__(self, value: object) -> bool:
        if not isinstance(value, Interval):
            return False
        key = value.stop
        node = _as_optional_interval_node(self._root)
        while node is not None:
            if node.value.stop < key:
                node = _as_optional_interval_node(node.left)
            elif node.value.stop > key:
                node = _as_optional_interval_node(node.right)
            else:
                break
        return node is not None and node.value == value

    def __len__(self) -> int:
        return self._count

    def discard(self, value: Interval[Point, Data]) -> None:
        raise NotImplementedError()
