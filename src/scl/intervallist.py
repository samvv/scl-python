
from collections.abc import Callable, Iterable, Iterator, MutableSet, Sequence
from dataclasses import dataclass
from typing import Generic, TypeVar, cast

from scl.util import Comparable

Point = TypeVar('Point', bound=Comparable)

@dataclass(frozen=True)
class Interval(Generic[Point]):
    start: Point
    stop: Point

_T = TypeVar('_T')

def binary_search_left(elements: Sequence[_T], needle: Comparable, /, key: str | Callable[[_T], Comparable] | None = None) -> int:
    if key is None:
        key = lambda element: cast(Comparable, element)
    if isinstance(key, str):
        keep = key
        key = lambda element: getattr(element, keep)
    min = 0
    max = len(elements)
    while min < max:
        i = (max + min) // 2
        element = elements[i]
        element_key = key(element)
        if element_key < needle:
            min = i+1
        else:
            max = i
    return min


def binary_search_right(elements: Sequence[_T], needle: Comparable, /, key: str | Callable[[_T], Comparable] | None = None) -> int:
    if key is None:
        key = lambda element: cast(Comparable, element)
    if isinstance(key, str):
        keep = key
        key = lambda element: getattr(element, keep)
    min = 0
    max = len(elements)
    while min < max:
        i = (max + min) // 2
        element = elements[i]
        element_key = key(element)
        if element_key > needle:
            max = i
        else:
            min = i+1
    return max

def binary_search(elements: Sequence[_T], needle: Comparable, /, key: str | Callable[[_T], Comparable] | None = None) -> int:
    if key is None:
        key = lambda element: cast(Comparable, element)
    if isinstance(key, str):
        keep = key
        key = lambda element: getattr(element, keep)
    min = 0
    max = len(elements)
    while min < max:
        i = (max + min) // 2
        element = elements[i]
        element_key = key(element)
        if element_key > needle:
            max = i
        elif element_key < needle:
            min = i+1
        else:
            return i
    return -1


class IntervalList(MutableSet[Interval[Point]], Generic[Point]):

    def __init__(self, elements: Iterable[Interval[Point]] | None = None) -> None:
        super().__init__()
        self._elements: list[Interval[Point]] = []
        if elements is not None:
            for element in elements:
                self.add(element)

    def __contains__(self, x: object) -> bool:
        if not isinstance(x, Interval):
            return False
        i = binary_search_left(self._elements, x.start, key='start')
        print(i)
        for k in range(i, len(self._elements)):
            element = self._elements[k]
            if element.start != x.start:
                pass # TODO
        return True

    def add(self, value: Interval[Point]) -> None:
        if not self._elements:
            self._elements.append(value)
        else:
            i = binary_search_right(self._elements, value.start, key='start')
            self._elements.insert(i, value)

    def __iter__(self) -> Iterator[Interval[Point]]:
        return iter(self._elements)

    def discard(self, value: Interval[Point]) -> None:
        raise NotImplementedError()

    def __len__(self) -> int:
        return len(self._elements)
