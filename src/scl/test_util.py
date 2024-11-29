
from .util import binary_search_right


def test_binary_search_nearest():
    l = [1,2,3]
    assert(binary_search_right(l, 0) == 0)
    assert(binary_search_right(l, 1) == 1)
    assert(binary_search_right(l, 2) == 2)
    assert(binary_search_right(l, 3) == 3)
    assert(binary_search_right(l, 4) == 3)
    # assert(binary_search_nearest(l, 4) == 2)
