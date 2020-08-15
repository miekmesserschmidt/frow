import pickle
import uuid
import fitz
import subprocess
import fitz
import os
import pytest
from frow.tools import pdf, inspect, multiprocess


def test_multi_process_fitz_doc(tmp_path):

    d = multiprocess.PickableFitzDoc("test/fixtures/orientation/tl.pdf")

    outfn = os.path.join(tmp_path, str(uuid.uuid1()))
    d.save(outfn)
    pickle.dumps(d)

    print(d.name)

    print(list(d.pages()))

    d[0]
    assert isinstance(d[0], multiprocess.PickableFitzPage)

    d[0].bound()

    pickle.dumps(d[0])
    # subprocess.call(["xdg-open", outfn])

