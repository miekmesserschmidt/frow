#! env/bin/python3.8
import os, sys
print(os.getcwd())
conf_path = os.getcwd()
sys.path.append(conf_path)

import pathlib
import warnings
from contextlib import suppress

import click
from tqdm import tqdm

from frow.tools import pdf
from frow.other import itools



from data.allocations import students
d = {student["stnum"] : student for student in students}




@click.command()
@click.argument('source')
@click.argument('dest')
@click.argument('var_name')
def varmerge(source, dest, var_name):
    with suppress(FileExistsError):
        os.makedirs(dest)
        
    def variation_key(fn):
        _, stnum = os.path.split(fn)
        
        data = d.get(stnum, {})
        if var_name not in data:
            warnings.warn(f"{var_name} not a key in data")
        
        return data.get(var_name, "unknown")

    print(f"{source} -> {dest}")
    
    
    fns = [str(p) for p in pathlib.Path(source).glob("**/*")]
    buckets = itools.bucket(fns, bucket_key=variation_key)

    for key,bucket in tqdm(buckets.items()):
        docs = (pdf.open_ensuring_pdf(fn) for fn in sorted(bucket))
        doc = pdf.merge_pdf(docs)
        doc.save(os.path.join(dest,key))
    
      

if __name__ == '__main__':
    varmerge()