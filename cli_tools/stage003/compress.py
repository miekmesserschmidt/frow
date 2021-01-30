#! env/bin/python3.8
import os,sys
print(os.getcwd())
conf_path = os.getcwd()
sys.path.append(conf_path)


import multiprocessing
import subprocess
import itertools
import pathlib
from contextlib import suppress

from tqdm import tqdm
from frow.tools import pdf, common, qr, bubbles
from frow.up import extract_first_st_num

import click


def worker(input_):
    fn, dest, quality = input_
    *_, f = os.path.split(fn)
    outfn = os.path.join(dest, f)

    # command = f'gs -dSAFER -dBATCH -dNOPAUSE -dNOCACHE -sDEVICE=pdfwrite -sColorConversionStrategy=/LeaveColorUnchanged  -dAutoFilterColorImages=true -dAutoFilterGrayImages=true -dDownsampleMonoImages=true -dDownsampleGrayImages=true -dDownsampleColorImages=true -sOutputFile="{outfn}" "{fn}"'
    # command = f'convert -density {density} {fn} {outfn}'
    command = f'gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/{quality} -dNOPAUSE -dQUIET -dBATCH -sOutputFile={outfn} {fn}'
  
    p1 = subprocess.call(command.split())        

@click.command()
@click.argument('source')
@click.argument('dest')
@click.option('--quality', "-q", default='ebook', type=click.Choice(['screen', 'ebook', 'prepress']))
@click.option('--processors', "-p", default=10, type=int)
def compress(source, dest, quality, processors):
        
    with suppress(FileExistsError):
        os.makedirs(dest)
    
    inputs = [(str(p), dest, quality) for p in pathlib.Path(source).glob("**/*") if not p.is_dir()]    
    
    with multiprocessing.Pool(processors) as pool:
        for _ in tqdm(pool.imap_unordered(worker, inputs ), total = len(inputs)):
            pass

if __name__ == '__main__':
    compress()