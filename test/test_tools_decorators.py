import os, pytest
import  frow.tools.decorators as dec


def test_with_silence_errors_toggle():

    @dec.with_silence_errors_toggle
    def f(a=1,b=1,c=1):
        if a == 0:
            raise ValueError()

    with pytest.raises(ValueError):
        f(a=0)

    f(a=0, silence_errors=True)
