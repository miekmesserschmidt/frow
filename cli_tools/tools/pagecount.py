#! env/bin/python3.8

import re
import click
from contextlib import suppress
import os
import fitz
from tqdm import tqdm
import sys 

print(os.getcwd())
conf_path = os.getcwd()
sys.path.append(conf_path)

from frow.tools import pdf, common
from frow.up import extract_first_st_num
import pathlib


import data


@click.command()
@click.argument('source')
def pagecount(source):
    print(source)
        
    fns = [str(p )for p in pathlib.Path(source).glob("**/*") if not p.is_dir()]
    fns = tqdm(fns)
    total_pages = sum(fitz.open(fn).pageCount for fn in fns)

    print(total_pages)        


if __name__ == '__main__':
    pagecount()
    
    