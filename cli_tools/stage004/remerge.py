#! env/bin/python3.8
import os, sys

print(os.getcwd())
conf_path = os.getcwd()
sys.path.append(conf_path)

from contextlib import suppress
import multiprocessing
import pathlib

from tqdm import tqdm
import click

from frow.other import itools
from frow.tools import pdf, common, qr, bubbles
from frow.up import extract_first_st_num


def worker(inputs_):
    key, bucket, dest = inputs_

    fns = [pdf.open_ensuring_pdf(fn) for fn in sorted(bucket)]
    doc = pdf.merge_pdf(fns)
    doc.save(os.path.join(dest, f"{key}.pdf"))


@click.command()
@click.argument("source")
@click.argument("dest")
@click.option("--processors", "-p", default=10, type=int)
def remerge(source, dest, processors):

    with suppress(FileExistsError):
        os.makedirs(dest)

    fns = [str(p) for p in pathlib.Path(source).glob("**/*") if not p.is_dir()]

    buckets = itools.bucket(fns, bucket_key=extract_first_st_num)
    inputs = [(key, bucket, dest) for key, bucket in buckets.items()]

    with multiprocessing.Pool(processors) as pool:

        for _ in tqdm(
            pool.imap_unordered(worker, inputs, chunksize=10), total=len(inputs)
        ):
            pass


if __name__ == "__main__":
    remerge()
