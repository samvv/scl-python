
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
        min = 0
        max = len(self._elements)
        print(self._elements)
        k = needle.start
        while min < max:
            i = (max + min) // 2
            element = self._elements[i]
            if element.stop < needle.start:
                min = i+1
            elif element.start > needle.stop:
                max = i
            else: # They are overlapping
                break;
        for j in range(min, max):
            element = self._elements[j]
            if element.start > k:
                return False
            k = element.stop
            if k >= needle.stop:
                return True
        return False

    def add(self, value: Interval[Point]) -> None:
        n = len(self._elements)
        self._elements.append(value)
        sort_inserted(self._elements, n)

    def __contains__(self, x: object) -> bool:
        return isinstance(x, Interval) and self.within(x)

    def __iter__(self) -> Iterator[Interval[Point]]:
        return iter(self._elements)

    def discard(self, value: Interval[Point]) -> None:
        raise NotImplementedError()

    def __len__(self) -> int:
        return len(self._elements)
