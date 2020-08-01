import functional.pipeline
import functools
import itertools

@functional.pipeline.extend()
def zip_map(it, func):
    it0, it1 = itertools.tee(it, 2)
    return zip(it0, map(func, it1))

@functional.pipeline.extend()
def zip_starmap(it, func):
    it0, it1 = itertools.tee(it, 2)
    return zip(it0, itertools.starmap(func, it1))


@functional.pipeline.extend()
def map_with_args_kwargs(it, func, *args, **kwargs):
    g = lambda x : functools.partial(func, x, *args, **kwargs)()
    return map(g, it)

@functional.pipeline.extend()
def starmap_with_args_kwargs(it, func, *args, **kwargs):
    g = lambda *x : functools.partial(func, *x, *args, **kwargs)()
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
                logger.exception(f"Error {e}",stack_info=True)

            print(e)
            

        
