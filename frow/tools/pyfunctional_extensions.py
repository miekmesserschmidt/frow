import multiprocessing
import functional
import functional.pipeline
import functools
import itertools
import more_itertools
import tqdm

@functional.pipeline.extend()
def zip_map(it, func):
    it0, it1 = itertools.tee(it, 2)
    return zip(it0, map(func, it1))


@functional.pipeline.extend()
def zip_starmap(it, func):
    it0, it1 = itertools.tee(it, 2)
    return zip(it0, itertools.starmap(func, it1))


@functional.pipeline.extend()
def star_for_each(it, func):
    it0, it1 = itertools.tee(it, 2)    
    for i in it1:        
        func(*i)
    return it0



@functional.pipeline.extend()
def distribute(it, n):
    return more_itertools.distribute(n, it)



@functional.pipeline.extend()
def map_with_args_kwargs(it, func, *args, **kwargs):
    g = lambda x: functools.partial(func, x, *args, **kwargs)()
    return map(g, it)


@functional.pipeline.extend()
def starmap_with_args_kwargs(it, func, *args, **kwargs):
    g = lambda *x: functools.partial(func, *x, *args, **kwargs)()
    return itertools.starmap(g, it)


@functional.pipeline.extend()
def silent_errors(it, logger=None):
    I = iter(it)

    while True:
        try:
            yield next(I)
        except StopIteration:
            return
        except KeyboardInterrupt:
            raise
        except Exception as e:
            if logger:
                logger.exception(f"Error {e}", stack_info=True)

            print(e)


@functional.pipeline.extend()
def with_progress(it, total=None):    
    for item in tqdm.tqdm(it, total=total):
        yield item
        
@functional.pipeline.extend()
def multiprocessing_map(it, func, pool_size=4, chunksize=128):
    
    with multiprocessing.Pool(pool_size) as p:
        yield from p.imap(func, it, chunksize=chunksize)
            
    