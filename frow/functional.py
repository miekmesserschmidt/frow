import functional.pipeline
import functools

@functional.pipeline.extend()
def zipmap(it, func):
    return zip(it, map(func, it))

@functional.pipeline.extend()
def map_with_args_kwargs(it, func, *args, **kwargs):
    g = lambda x : functools.partial(func, x, *args, **kwargs)()
    return map(g, it)


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
            

        
