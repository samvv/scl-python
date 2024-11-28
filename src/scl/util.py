
from typing import Protocol, TypeVar


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

