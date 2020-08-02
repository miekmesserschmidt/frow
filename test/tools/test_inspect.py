import pytest
import subprocess
import os 
from frow.tools import inspect


img_path = "test/fixtures/img"


@pytest.mark.parametrize("img_fn", [
    ("01.jpg"),
    ("04.png"),
])
def test_is_not_pdf(img_fn):
    fn = os.path.join(img_path, img_fn)
    assert not inspect.is_pdf(fn)

@pytest.mark.parametrize("img_fn", [
    ("00.jpg.pdf"),
])
def test_is_pdf(img_fn):
    fn = os.path.join(img_path, img_fn)
    assert inspect.is_pdf(fn)
