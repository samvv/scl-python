
from .intervallist import Interval, IntervalList

def _assert_invariants_hold(l: IntervalList) -> None:
    if l._elements:
        prev = l._elements[0]
        for interval in l._elements[1:]:
            assert(prev <= interval)


def test_intervallist_add_contains():
    l = IntervalList[int]()
    _assert_invariants_hold(l)
    assert(not Interval(1, 2) in l)
    assert(not Interval(2, 3) in l)
    assert(not Interval(1, 3) in l)
    l.add(Interval(1, 2))
    _assert_invariants_hold(l)
    assert(Interval(1, 2) in l)
    assert(not Interval(2, 3) in l)
    assert(not Interval(1, 3) in l)
    l.add(Interval(2, 3))
    _assert_invariants_hold(l)
    assert(Interval(1, 2) in l)
    assert(Interval(2, 3) in l)
    assert(Interval(1, 3) in l)


