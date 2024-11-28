
from typing import Generic

from scl.util import T


class Node(Generic[T]):

    def __init__(self, value: T) -> None:
        super().__init__()
        self.value = value
        self.parent: Node[T] | None = None

    @property
    def root(self) -> 'Node[T]':
        node = self
        while True:
            if node.parent is None:
                break
            node = node.parent
        return node

class Tree(Generic[T]):

    def __init__(self) -> None:
        super().__init__()
        self._root: Node[T] | None = None

