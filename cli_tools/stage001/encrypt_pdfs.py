#! env/bin/python3.8

import sys, os
print(os.getcwd())
conf_path = os.getcwd()
sys.path.append(conf_path)


import pathlib
import itertools
import multiprocessing
from contextlib import suppress
import subprocess

import click
from tqdm import tqdm


from data.allocations import students
student_map = {
    student["stnum"] : student for student in students    
}


def worker(input_):
    fn, dest = input_
    *_, f = os.path.split(fn)
    sn, _ = os.path.splitext(f)    
    outfn = os.path.join(dest, f)
    passwd = student_map[sn]["passwd"]
    
    command = f"pdftk {fn} output {outfn} user_pw {passwd}"
    proc =  subprocess.Popen(command.split())    


@click.command()
@click.argument('source')
@click.argument('dest')
@click.option('--processors', "-p", default=10, type=int)
def encrypt(source, dest, processors):
        
    with suppress(FileExistsError):
        os.makedirs(dest)
    
    fns = [(str(p),dest) for p in pathlib.Path(source).glob("**/*.pdf") if not p.is_dir()]
    
    with multiprocessing.Pool(processors) as pool:
        for _ in tqdm(pool.imap_unordered(worker, fns ), total = len(fns)):
            pass

if __name__ == '__main__':
    encrypt()            
    