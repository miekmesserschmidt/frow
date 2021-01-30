#! env/bin/python3.8

import os, sys
print(os.getcwd())
conf_path = os.getcwd()
sys.path.append(conf_path)

from contextlib import suppress
import multiprocessing
import pathlib

import click
from tqdm import tqdm

from frow.tools import pdf, common
from frow.other import itools
from frow.up import extract_first_st_num


from data.allocations import students
d = {student["stnum"] : student for student in students}



def refit_(doc):
    try:
        doc = pdf.refit_pdf(doc, relative_paste_rect=(0,0,.85,.85))
        return doc
    except ValueError:
        print(f"WARNING: unable to refit {doc}")      
        return

def add_doc_id(doc, st_num, doc_id, var_id):
    
    doc = common.add_page_id_marks(
        doc, 
        {
            "st_num" : st_num, 
            "doc_id": doc_id,
            "var": d.get(st_num, {}).get(f"{var_id}", "unknown"),
        }, 
        relative_rect=(.05, .88, .5, .96)
    )
    return doc
    
def add_mark_recorder(doc):
    # mark_rec = fitz.open("other/mark_recorder0.pdf")
    mark_rec = pdf.open_ensuring_pdf("other/mark_recorder0.pdf")
    pdf.paste_pdf_on_every_page(
        doc, 
        mark_rec, 
        relative_rect=(.87, .03, .98, .5) 
    )
    
    return doc


def worker(inputs_):
    fn, dest, doc_id, var_id = inputs_
    _, st_num = os.path.split(fn)

    doc = pdf.open_ensuring_pdf(fn)
    doc = refit_(doc)
    doc = add_doc_id(doc, st_num, doc_id, var_id)
    doc = add_mark_recorder(doc)
    
    doc.save(os.path.join(dest, st_num))
    
    
@click.command()
@click.argument('source')
@click.argument('dest')
@click.argument('doc_id')
@click.argument('var_id')
@click.option('--processors', "-p", default=10, type=int)
def refit(source, dest, doc_id, var_id, processors):
    
    with suppress(FileExistsError):
        os.makedirs(dest)
        

    fns = [str(p) for p in pathlib.Path(source).glob("**/*")]
    inputs = [(fn, dest, doc_id, var_id) for fn in fns]
    with multiprocessing.Pool(processors) as pool:
        for _ in tqdm(pool.imap_unordered(worker,inputs, chunksize=10), total=len(inputs)):
            pass

        
       
        
if __name__ == '__main__':
    refit()