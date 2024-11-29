
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
    assert(Interval(1, 5) not in l)

def test_intervallist_overlap():
    l = IntervalList[int]()
    _assert_invariants_hold(l)
    i1 = Interval(1, 2)
    i2 = Interval(2, 3)
    i3 = Interval(4, 5)
    i4 = Interval(6, 7)
    i5 = Interval(1, 3)
    l.add(i1)
    l.add(i2)
    l.add(i3)
    l.add(i4)
    l.add(i5)
    o1 = l.overlap_point(1)
    assert(len(o1) == 2)
    assert(i1 in o1)
    assert(i5 in o1)
    o2 = l.overlap_point(2)
    assert(len(o2) == 2)
    assert(i2 in o2)
    assert(i5 in o2)
    o3 = l.overlap_point(2)
    assert(len(o3) == 0)

