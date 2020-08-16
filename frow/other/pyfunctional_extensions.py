import multiprocessing
import functional
import functional.pipeline
import functools
import itertools
import more_itertools
import tqdm

@functional.pipeline.extend()
def zip_map(it, func):
    """Same as map, but the result is a zip: (a, func(a))

    Args:
        it ([type]): iterator to map on
        func ([type]): function to map

    Returns:
        [iterator]: equivalent to generator expression ```((a, func(a)) for a in a in it)```
    """
    it0, it1 = itertools.tee(it, 2)
    return zip(it0, map(func, it1))


@functional.pipeline.extend()
def zip_starmap(it, func):
    """Same as starmap, but the result is a zip: (a, func(\*a))

    Args:
        it ([type]): iterator to map on
        func ([type]): function to map

    Returns:
        [iterator]: equivalent to generator expression ```((a, func(*a)) for a in a in it)```
    """
    it0, it1 = itertools.tee(it, 2)
    return zip(it0, itertools.starmap(func, it1))


@functional.pipeline.extend()
def star_chained_for_each(it, func):
    """Same as for_each, but \*-unpacks inputs

    Args:
        it ([type]): iterator to map on
        func ([type]): function to map
        
    Returns:
        [iterator]: equivalent to generator expression ```(func(*a) for a in a in it)```
    """
    it0, it1 = itertools.tee(it, 2)    
    for i in it1:        
        func(*i)
    return it0

@functional.pipeline.extend()
def chained_for_each(it, func):
    """Same as for_each, but \*-unpacks inputs

    Args:
        it ([type]): iterator to map on
        func ([type]): function to map
        
    Returns:
        [iterator]: equivalent to generator expression ```(func(*a) for a in a in it)```
    """
    it0, it1 = itertools.tee(it, 2)    
    for i in it1:        
        func(i)
    return it0



@functional.pipeline.extend()
def distribute(it, n):
    """Distributes the iterator evenly into n iterators.

    Args:
        it ([type]): iterator to map on
        n ([int]): number of iterators to distribute into
        
    Returns:
        [iterator]: n-iterators that the iterator was distributed acoross
    """    
    return more_itertools.distribute(n, it)



@functional.pipeline.extend()
def map_with_args_kwargs(it, func, *args, **kwargs):
    """Same as map but passes args and kwargs down to the function
    
    Args:
        it ([type]): iterator to map on
        func ([type]): function to map
        ```*args``` : args to pass down to function
        ```**kargs``` : kwargs to pass down to function

    Returns:
        [iterator]: equivalent to generator ```(func(a, *args, **kwargs) for a in a in it)```
    """
    g = lambda x: functools.partial(func, x, *args, **kwargs)()
    return map(g, it)


@functional.pipeline.extend()
def starmap_with_args_kwargs(it, func, *args, **kwargs):
    """Same as starmap but passes args and kwargs down to the function
    
    Args:
        it ([type]): iterator to map on
        func ([type]): function to map
        ```*args``` : args to pass down to function
        ```**kargs``` : kwargs to pass down to function

    Returns:
        [iterator]: equivalent to generator ```(func(*a, *args, **kwargs) for a in a in it)```
    """    
    
    g = lambda *x: functools.partial(func, *x, *args, **kwargs)()
    return itertools.starmap(g, it)


@functional.pipeline.extend()
def silent_errors(it, logger=None):
    """Prevents errors during iteration from stopping execution. Errors are caught and logged instead.

    Args:
        it ([type]): iterator which may raise exceptions
        logger ([type], optional): Logger to log to. Defaults to None.

    Yields:
        [type]: yields from the iterator
    """
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
    """Allows for iteration with a tqdm progressbar

    Args:
        it ([type]): iterator
        total ([type], optional): Total number of items in the iterator. Defaults to None.

    Yields:
        [type]: it
    """
    for item in tqdm.tqdm(it, total=total):
        yield item
        
@functional.pipeline.extend()
def multiprocessing_map(it, func, pool_size=4, chunksize=128):
    """[summary]

    Args:
        it ([type]): iterator to map on
        func ([type]): function to map
        pool_size (int, optional): Number of workers. Defaults to 4.
        chunksize (int, optional): Chunck size passed to workers. Defaults to 128.

    Yields:
        [type]: equivalent to generator ```(func(a) for a in a in it)```
    """
    with multiprocessing.Pool(pool_size) as p:
        yield from p.imap(func, it, chunksize=chunksize)
            
    