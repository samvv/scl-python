
from collections.abc import Iterable, Iterator, MutableSet
from dataclasses import dataclass
from typing import Generic, TypeVar

from scl.util import Comparable, sort_inserted

Point = TypeVar('Point', bound=Comparable)

@dataclass(frozen=True, order=True)
class Interval(Generic[Point]):
    start: Point
    stop: Point

class IntervalList(MutableSet[Interval[Point]], Generic[Point]):

    def __init__(self, elements: Iterable[Interval[Point]] | None = None) -> None:
        super().__init__()
        self._elements: list[Interval[Point]] = []
        if elements is not None:
            for element in elements:
                self.add(element)

    def within(self, needle: Interval[Point]) -> bool:
        raise NotImplementedError()

    def overlap_point(self, p: Point) -> set[Interval[Point]]:
        raise NotImplementedError()

    def add(self, value: Interval[Point]) -> None:
        n = len(self._elements)
        self._elements.append(value)
        sort_inserted(self._elements, n)

    def addi(self, start: Point, stop: Point) -> None:
        self.add(Interval(start, stop))

    def __contains__(self, x: object) -> bool:
        return isinstance(x, Interval) and self.within(x)

    def __iter__(self) -> Iterator[Interval[Point]]:
        return iter(self._elements)

    def discard(self, value: Interval[Point]) -> None:
        raise NotImplementedError()

    def __len__(self) -> int:
        return len(self._elements)
