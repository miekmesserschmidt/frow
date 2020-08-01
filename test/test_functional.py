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