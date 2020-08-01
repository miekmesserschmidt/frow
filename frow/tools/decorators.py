import logging

logger = logging.getLogger(__name__)


def with_silence_errors_toggle(f):

    def wrapper(*args, silence_errors = False, **kwargs):
        try:
            f(*args, **kwargs)
        except Exception as e:
            logger.exception(f"{f.__name__} failed on {args} {kwargs}", stack_info=True)
            if not silence_errors:
                raise e
            if isinstance(e, KeyboardInterrupt):
                raise e

    return wrapper
