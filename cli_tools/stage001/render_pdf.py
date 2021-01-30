#! env/bin/python3.8
import sys, os
run_path = os.getcwd()
sys.path.append(run_path)


import pathlib
import itertools
import multiprocessing
import subprocess
from contextlib import suppress

import click
from tqdm import tqdm



from data.allocations import students
student_map = {
    student["stnum"] : student for student in students    
}


def worker(input_):
    student, source, dest, verbose = input_
    st_num = student["stnum"]
    if verbose:
        print(st_num)
    proc = subprocess.Popen(f"pdflatex --jobname={st_num} --output-directory=../{dest}  {source}".split(), stdout=subprocess.PIPE)    
    proc.wait()

    if verbose:
        print(proc.communicate()[0].decode())

    
    


@click.command()
@click.argument('sourcefile')
@click.argument('dest')
@click.option('--processors', "-p", default=10, type=int)
@click.option('--number', "-n", default=0, type=int)
@click.option('--chunksize', "-c", default=5, type=int)
@click.option('--verbose', "-v", count=True)
def render_pdf(sourcefile, dest, processors, number, chunksize, verbose):
    
    
        
    sourcedir, source_fn = os.path.split(sourcefile)
    with suppress(FileExistsError):
        os.makedirs(dest)
                
    os.chdir(sourcedir)

    inputs = [(s, source_fn, dest, verbose) for s in students]
    if number:
        inputs = inputs[:number]
    with multiprocessing.Pool(processors) as pool:
        
        for _ in tqdm(pool.imap_unordered(worker, inputs, chunksize=chunksize), total=len(inputs)):
            pass
        
    os.chdir("..")


if __name__ == '__main__':
    render_pdf()            
        