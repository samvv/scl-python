
from dataclasses import dataclass
from collections.abc import Generator, Hashable, Iterable, Iterator
from typing import Generic, TypeVar

_K = TypeVar('_K')
_T = TypeVar('_T')
_V = TypeVar('_V', bound=Hashable)

class _MultiDict(Generic[_K, _T]):

    def __init__(self) -> None:
        super().__init__()
        self._mapping = dict[_K, set[_T]]()
        self._count = 0

    def add(self, k: _K, v: _T) -> None:
        if k not in self._mapping:
            m = self._mapping[k] = set()
        else:
            m = self._mapping[k]
        if v not in m:
            self._mapping[k].add(v)
            self._count += 1

    def has(self, k: _K, v: _T) -> bool:
        m = self._mapping.get(k)
        return m is not None and v in m

    def count(self, k: _K) -> int:
        m = self._mapping.get(k)
        return len(m) if m is not None else 0

    def remove_key(self, k: _K) -> None:
        m = self._mapping.get(k)
        if m is not None:
            self._count -= len(m)
            del self._mapping[k]

    def remove(self, k: _K, v: _T) -> None:
        m = self._mapping.get(k)
        if m is not None:
            try:
                m.remove(v)
            except KeyError:
                return
            self._count -= 1

    def __getitem__(self, key: _K) -> Iterable[_T]:
        return self._mapping.get(key, [])

    def __len__(self) -> int:
        return self._count

class GraphVertices(Generic[_V]):

    def __init__(self, vertices: set[_V]) -> None:
        super().__init__()
        self._vertices = vertices

    def __len__(self) -> int:
        return len(self._vertices)

    def __iter__(self) -> Iterator[_V]:
        return iter(self._vertices)

class Graph(Generic[_V]):

    def __init__(self) -> None:
        super().__init__()
        self._vertices = set[_V]()
        self._src_to_dst = _MultiDict[_V, _V]()
        self._edge_count = 0

    def add_vertex(self, v: _V) -> None:
        self._vertices.add(v)

    def has_vertex(self, v: _V) -> bool:
        return v in self._vertices

    def count_vertices(self) -> int:
        return len(self._vertices)

    @property
    def vertices(self) -> GraphVertices[_V]:
        return GraphVertices(self._vertices)

    def remove_vertex(self, v: _V) -> None:
        try:
            self._vertices.remove(v)
        except KeyError:
            return
        edges_to_remove = []
        for dst in self._vertices:
            for dst_2 in self._src_to_dst[dst]:
                if dst_2 == v:
                    edges_to_remove.append((dst, dst_2))
        self._edge_count -= len(edges_to_remove) + self._src_to_dst.count(v)
        for dst, src in edges_to_remove:
            self._src_to_dst.remove(dst, src)
        self._src_to_dst.remove_key(v)

    def add_edge(self, src: _V, dst: _V) -> None:
        self._vertices.add(src)
        self._vertices.add(dst)
        if not self._src_to_dst.has(src, dst):
            self._src_to_dst.add(src, dst)
            self._edge_count += 1

    def count_edges(self) -> int:
        return self._edge_count

    def remove_edge(self, src: _V, dst: _V) -> None:
        if self._src_to_dst.has(src, dst):
            self._src_to_dst.remove(src, dst)
            self._edge_count -= 1

    def has_edge(self, src: _V, dst: _V) -> bool:
        return self._src_to_dst.has(src, dst)

    def get_out_vertices(self, src: _V) -> Iterable[_V]:
        return self._src_to_dst[src]

def dump_graph(graph: Graph[_V]) -> None:
    for src in graph.vertices:
        for dst in graph.get_out_vertices(src):
            print(f' - {src} -> {dst}')

def strongconnect(g: Graph[_V]) -> Generator[set[_V]]:

    @dataclass
    class Data:
        index: int | None = None
        low_link: int | None = None
        on_stack: bool = False

    mapping = dict[_V, Data]()
    index = 0
    stack = list[_V]()

    def get_data(v: _V) -> Data:
        data = mapping.get(v)
        if data is None:
            data = Data()
            mapping[v] = data
        return data

    def visit(v: _V) -> Generator[set[_V]]:
        nonlocal index

        v_data = get_data(v)
        v_data.index = index
        v_data.low_link = index
        index += 1
        stack.append(v)
        v_data.on_stack = True

        for w in g.get_out_vertices(v):
            w_data = get_data(w)
            if w_data.index is None:
                yield from visit(w)
                assert(w_data.low_link is not None)
                v_data.low_link = min(v_data.low_link, w_data.low_link)
            elif w_data.on_stack:
                v_data.low_link = min(v_data.low_link, w_data.index)

        if v_data.low_link == v_data.index:
            scc = set[_V]()
            while True:
                w = stack.pop()
                w_data = get_data(w)
                w_data.on_stack = False
                scc.add(w)
                if w == v:
                    break
            yield scc

    for v in g.vertices:
        if v not in mapping:
            yield from visit(v)

