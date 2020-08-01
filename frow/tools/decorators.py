import logging
import os 

logger = logging.getLogger(__name__)


def ensure_path(path):
    try:
        os.makedirs(path)
    except FileExistsError:
        pass


def with_silence_errors_toggle(f):
    def wrapper(*args, silence_errors=False, **kwargs):
        try:
            f(*args, **kwargs)
        except Exception as e:
            logger.exception(f"{f.__name__} failed on {args} {kwargs}", stack_info=True)
            if not silence_errors:
                raise e
            if isinstance(e, KeyboardInterrupt):
                raise e

    return wrapper

def with_overwrite_toggle(f):
    def wrapper(source_fn, dest_fn, *args, overwrite=True, **kwargs):
        if os.path.isfile(dest_fn) and not overwrite:
            return dest_fn
        else:
            return f(source_fn, dest_fn, *args, **kwargs)

    return wrapper

