import functional.pipeline
import functools

@functional.pipeline.extend()
def zipmap(it, func):
    return zip(it, map(func, it))

@functional.pipeline.extend()
def map_with_args_kwargs(it, func, *args, **kwargs):
    gunc = lambda x : functools.partial(func, x, *args, **kwargs)()
    return map(gunc, it)