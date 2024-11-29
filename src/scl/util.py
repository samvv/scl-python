
from collections.abc import Callable, Sequence
from typing import Protocol, TypeVar, cast


_Self = TypeVar('_Self', bound='Comparable')


class Comparable(Protocol):
    def __lt__(self: _Self, value: '_Self', /) -> bool: ...
    def __gt__(self: _Self, value: '_Self', /) -> bool: ...
    def __le__(self: _Self, value: '_Self', /) -> bool: ...
    def __ge__(self: _Self, value: '_Self', /) -> bool: ...

# This type variable is always used to represent the element of a collection.
T = TypeVar('T')


def nonnull(value: T | None) -> T:
    assert(value is not None)
    return value


_T = TypeVar('_T')


def lift_key(arg: str | Callable[[_T], Comparable] | None) -> Callable[[_T], Comparable]:
    if arg is None:
        return lambda element: cast(Comparable, element)
    if isinstance(arg, str):
        name = arg
        return lambda element: getattr(element, name)
    return arg


def sort_inserted(elements: list[_T], i: int, key: str | Callable[[_T], Comparable] | None = None) -> None:
    """
    Function that assumes a sorted list `elements` where a single element at index `i` is out of place.
    """
    key = lift_key(key)
    x = elements[i]
    x_key = key(x)
    j = i
    while j > 0 and key(elements[j-1]) > x_key:
        elements[j] = elements[j-1]
        j = j - 1
    elements[j] = x


def insertionsort(elements: list[_T], key: str | Callable[[_T], Comparable] | None = None) -> None:
    """
    Sort all elements of a list according to insertion sort.
    """
    key = lift_key(key)
    i = 1
    n = len(elements)
    while i < n:
        sort_inserted(elements, i)
        i = i + 1


def binary_search_left(elements: Sequence[_T], needle: Comparable, /, key: str | Callable[[_T], Comparable] | None = None) -> int:
    """
    Get the index of the leftmost element for which the key is no smaller than `needle`.
    """
    key = lift_key(key)
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
    """
    Get the index of the rightmost element for which the key is no larger than `needle`.
    """
    key = lift_key(key)
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
    """
    Get the index of the element that exactly matches keys with `needle`.
    """
    key = lift_key(key)
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


