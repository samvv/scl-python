
from .intervallist import Interval, IntervalList, binary_search_right


def test_binary_search_nearest():
    l = [1,2,3]
    assert(binary_search_right(l, 0) == 0)
    assert(binary_search_right(l, 1) == 1)
    assert(binary_search_right(l, 2) == 2)
    assert(binary_search_right(l, 3) == 3)
    assert(binary_search_right(l, 4) == 3)
    # assert(binary_search_nearest(l, 4) == 2)


def test_intervallist_add_contains():
    l = IntervalList[int]()
    assert(not Interval(1, 2) in l)
    assert(not Interval(2, 3) in l)
    assert(not Interval(1, 3) in l)
    l.add(Interval(1, 2))
    assert(Interval(1, 2) in l)
    assert(not Interval(2, 3) in l)
    assert(not Interval(1, 3) in l)
    l.add(Interval(2, 3))
    assert(Interval(1, 2) in l)
    assert(Interval(2, 3) in l)
    assert(Interval(1, 3) in l)


