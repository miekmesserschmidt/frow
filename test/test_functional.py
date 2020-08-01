import pytest
from frow import functional as frow_func
import functional


def test_zip_map():

    s = functional.seq([1,2,3]).zipmap(func=lambda x : 2*x)
    assert s == [(1,2), (2,4), (3,6)]

def test_map_with_args_kwargs():

    def f(in_, r = 2):
        return in_**r

    s = functional.seq([1,2,3]).map_with_args_kwargs(f, r=3)
    assert s == [1,8,27]


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