#! env/bin/python3.8

import os,sys
print(os.getcwd())
conf_path = os.getcwd()
sys.path.append(conf_path)


import re
import click
import pathlib
from contextlib import suppress
from tqdm import tqdm

from frow.tools import pdf, common
from frow.other import itools
from frow.up import extract_first_st_num


@click.command()
@click.argument('source')
@click.argument('dest')
def clean(source, dest):
    print(source, dest)
    with suppress(FileExistsError):
        os.makedirs(dest)
        
        
    fns = [str(p )for p in pathlib.Path(source).glob("**/*") if not re.match(r'.*.txt', str(p))]
    buckets = itools.bucket(fns, bucket_key=extract_first_st_num)
    
    for key, fns in tqdm(list(buckets.items())):
        try:
            doc = pdf.merge_pdf(pdf.open_ensuring_pdf(fn) for fn in fns)
            doc.save(os.path.join(dest, key))
        except RuntimeError:
           print(key, fns)
           raise
      
        
if __name__ == '__main__':
    clean()