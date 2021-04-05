import os
import pathlib
import re
from frow.pipe import Pipe
from frow.suite import suite
import subprocess
fixture_path = "test/fixtures/suite/"


def test_key_merge(tmp_path):
    
    fns = [str(p )for p in pathlib.Path(fixture_path + "raw").glob("**/*") if not re.match(r'.*.txt', str(p))]
    
    p = (
        Pipe(fns)
        .group_by(key= suite.extract_first_st_num)
        .starmap(suite.key_merge, kwargs={"output_path" : tmp_path}, eager=True)        
    )
    
    print(p.list_items)
    
    # for item in p.list_items:
    #     subprocess.call(["xdg-open", item])
    
    
def test_refit(tmp_path):
    
    fns = [str(p )for p in pathlib.Path(fixture_path + "torefit").glob("**/*") ]
    
    
    out = fixture_path + "topaste_mark_recorder"
    p = (
        Pipe(fns)
        .map(suite.refit, kwargs={"output_path" : tmp_path}, eager=True)
    )

    print(p.list_items)
    
    # for item in p.list_items:
    #     subprocess.call(["xdg-open", item])


def test_image_grind(tmp_path):
    
    fns = [str(p )for p in pathlib.Path(fixture_path + "to_image_grind").glob("**/*") ]
    
    tmp0 = os.path.join(tmp_path, "tmp0")
    tmp1 = os.path.join(tmp_path, "tmp1")
    
    p = (
        Pipe(fns)
        .map(suite.grind_through_image, kwargs={"output_path" : tmp1, "tmp_path":tmp0}, eager=True)
    )

    print(p.list_items)
    
    # for item in p.list_items:
    #     subprocess.call(["xdg-open", item])
    
    
    
def test_paste_mark_recorder(tmp_path):
    
    fns = [str(p )for p in pathlib.Path(fixture_path + "topaste_mark_recorder").glob("**/*") ]


    p = (
        Pipe(fns)
        .map(suite.paste_markrecorder, kwargs={"output_path" : tmp_path}, eager=True)
    )

    print(p.list_items)
    
    # for item in p.list_items:
    #     subprocess.call(["xdg-open", item])
    
    
    
    
def test_add_page_id_mark(tmp_path):
    
    fns = [str(p )for p in pathlib.Path(fixture_path + "topaste_mark_recorder").glob("**/*") ]

    
    
    def make_data_dict(sn):        
        return {
            "sn" : sn,
            "jobname" : "prac0",
        }
        
    p = (
        Pipe(fns)
        .map(lambda fn: (fn, make_data_dict(suite.extract_first_st_num(fn))) )
        .starmap(suite.add_page_id_marks, kwargs={"output_path" : tmp_path}, eager=True)
    )

    print(p.list_items)
    
    # for item in p.list_items:
    #     subprocess.call(["xdg-open", item])
    
    
            

def test_read_id_marks(tmp_path):
    
    fns = [str(p )for p in pathlib.Path(fixture_path + "to_read_id_marks").glob("**/*") ]
        
    p = (
        Pipe(fns)
        .map(suite.read_id_marks, eager=True)
    )

    print(p.list_items)    
    
    
def test_read_bubble_array(tmp_path):
    
    fns = [str(p )for p in pathlib.Path(fixture_path + "toread_mark_recorder").glob("**/*") ]
        
    tmp0 = os.path.join(tmp_path, "tmp0")
    tmp1 = os.path.join(tmp_path, "tmp1")
    p = (
        Pipe(fns)
        .map(suite.grind_through_image, kwargs={"output_path" : tmp1, "tmp_path":tmp0}, eager=True)
        .map(suite.read_bubble_array, eager=True)
    )

    # suite.grind_through_image()
    
    print(p.list_items)    
        
    
    
    
    
    
        
    
    
    
    
    
    
        
    
    
    
    
    
    
    
    
    
    