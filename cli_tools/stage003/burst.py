#! env/bin/python3.8
import os,sys
print(os.getcwd())
conf_path = os.getcwd()
sys.path.append(conf_path)


from contextlib import suppress
import collections
import multiprocessing
import pathlib
import itertools


import click

from tqdm import tqdm
from frow.tools import pdf, common, qr, bubbles
from frow.up import extract_first_st_num


def worker(input_):
    fn, dest = input_
    doc = pdf.open_ensuring_pdf(fn)
    
    for p in doc.pages():
        qr_data = qr.read_json_qr_robust(p, relative_rect=(0,.8, .4, 1))
            
        st_num = qr_data["st_num"]
        q = qr_data["doc_id"]
        index = qr_data["page_index"]

        out_fn = os.path.join(dest, f"{st_num}.{q}.{index:0>3}")
        out_d = pdf.doc_from_pages([p])
        out_d.save(out_fn)




@click.command()
@click.argument('source')
@click.argument('dest')
@click.option('--processors', "-p", default=10, type=int)
def burst(source, dest, processors):
        
    with suppress(FileExistsError):
        os.makedirs(dest)        
    
    fns = [str(p) for p in pathlib.Path(source).glob("**/*") if not p.is_dir()]
    inputs = [(fn, dest) for fn in fns]
    
    with multiprocessing.Pool(processors) as pool:
        for _ in tqdm(map(worker, inputs), total=len(inputs)):
            pass

if __name__ == '__main__':
    burst()