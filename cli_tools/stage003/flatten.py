#! env/bin/python3.8
import os,sys
print(os.getcwd())
conf_path = os.getcwd()
sys.path.append(conf_path)


from contextlib import suppress
import subprocess
import multiprocessing
import pathlib

import numpy as np
from tqdm import tqdm
from frow.tools import pdf, common, qr, bubbles
from frow.up import extract_first_st_num

import click


def worker(input_):
    fn, dest, density = input_

    *_, f = os.path.split(fn)
    outfn = os.path.join(dest, f)
    print(fn)
    print(outfn)

    # command = f'gs -dSAFER -dBATCH -dNOPAUSE -dNOCACHE -sDEVICE=pdfwrite -sColorConversionStrategy=/LeaveColorUnchanged  -dAutoFilterColorImages=true -dAutoFilterGrayImages=true -dDownsampleMonoImages=true -dDownsampleGrayImages=true -dDownsampleColorImages=true -sOutputFile="{outfn}" "{fn}"'
    command = f'convert -density {density} {fn} {outfn}'
    
    print(command)
    
    p1 = subprocess.call(command.split())



@click.command()
@click.argument('source')
@click.argument('dest')
@click.option('--density', "-d", default=150, type=int)
@click.option('--processors', "-p", default=1, type=int)
@click.option('--chunksize', "-c", default=1, type=int)
def flatten(source, dest, density, processors, chunksize):
        
    with suppress(FileExistsError):
        os.makedirs(dest)
    
    fns = [str(p) for p in pathlib.Path(source).glob("**/*") if not p.is_dir()]    
    inputs_ = [(fn,dest,density) for fn in fns]
    with multiprocessing.Pool(processes=processors) as pool:
        for _ in tqdm(pool.imap_unordered(worker, inputs_, chunksize=chunksize), total=len(inputs_)):
            pass
        



if __name__ == '__main__':
    flatten()