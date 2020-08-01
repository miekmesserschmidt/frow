import pytest
from frow import functional as frow_func
import functional


def test_zip_map():
    s = functional.seq([1,2,3]).zip_map(func=lambda x : 2*x)
    assert s == [(1,2), (2,4), (3,6)]

def test_zip_starmap():
    s = functional.seq([(1,2),(3,4)]).zip_starmap(func=lambda x,y : x*y)
    assert s == [((1,2), 2), ((3,4), 12)]


def test_map_with_args_kwargs():
    def f(in_, r = 2):
        return in_**r

    s = functional.seq([1,2,3]).map_with_args_kwargs(f, r=3)
    assert s == [1,8,27]


def test_starmap_with_args_kwargs():
    def f(a,b, c, r = 2):
        return a*b*r + c

    s = functional.seq([(1,2),(3,4)]).starmap_with_args_kwargs(f, -1, r=3)
    assert s == [5, 35]


def test_silent_errors():

    def f(in_, r = 2):
        if in_==3:
            raise ValueError()
        else:
            return in_**r

    s = functional.seq([1,2,3]).map_with_args_kwargs(f, r=3).silent_errors()
    assert s == [1,8]    

def test_silent_errors_key_intr():

    def f(in_, r = 2):
        if in_==3:
            raise KeyboardInterrupt
        else:
            return in_**r
    with pytest.raises(KeyboardInterrupt):
        s = functional.seq([1,2,3]).map_with_args_kwargs(f, r=3).silent_errors()
        assert s == [1,8]        