#! env/bin/python3.8
import os,sys
print(os.getcwd())
conf_path = os.getcwd()
sys.path.append(conf_path)

import click
from contextlib import suppress
import numpy as np
import pathlib
import multiprocessing

from tqdm import tqdm
from frow.other import itools
from frow.tools import pdf, common, qr, bubbles
from frow.up import extract_first_st_num


BUBBLEARRAY = np.array([
    [0,.5],
    [10,1],
    [20,2],
    [30,3],
    [40,4],
    [50,5],
    [60,6],
    [70,7],
    [80,8],
    [90,9],
])


def worker(input_):
    fn, dest = input_
    *_, only_fn = os.path.split(fn)
    
    d = pdf.open_ensuring_pdf(fn)
    for p in d.pages():
        bubble_array = bubbles.read_robust(p,(.8,0,1,.5))
        page_total = np.sum(bubble_array * BUBBLEARRAY)
        
        pdf.place_text(p, str(page_total), relative_rect=(.9,0,1,.1))
        
    out_fn = os.path.join(dest, only_fn)
    d.save(out_fn)


@click.command()
@click.argument('source')
@click.argument('dest')
# @click.option('--zoom', "-z", default=None, type=object)
@click.option('--processors', "-p", default=10, type=int)
@click.option('--chucksize', "-c", default=1, type=int)
def write_marks(source, dest, processors, chucksize):

    with suppress(FileExistsError):
        os.makedirs(dest)
    
    inputs = [(str(p), dest) for p in pathlib.Path(source).glob("**/*")]
    
    with multiprocessing.Pool(processors) as pool:
        for _ in tqdm(pool.imap_unordered(worker, inputs, chunksize=chucksize), total=len(inputs)):
            pass
            


if __name__ == '__main__':
    write_marks()