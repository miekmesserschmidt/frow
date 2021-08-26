import functools
import multiprocessing
import os
import contextlib
import collections
import itertools
from itertools import chain
from tqdm import tqdm
import more_itertools


def ensure_good_args_kwargs(args, kwargs):
    if args is None:
        args = tuple()

    if kwargs is None:
        kwargs = {}

    return args, kwargs


def wrap(iterator, wrap, yes):
    if yes:
        return wrap(iterator)
    else:
        return iterator


def with_suppressed_errors(worker):
    @functools.wraps(worker)
    def suppressed_worker(*args, **kwargs):
        try:
            return worker(*args, **kwargs)
        except Exception as e:
            print(e)

    return suppressed_worker


def error_reporting_worker(worker):
    @functools.wraps(worker)
    def error_reporting_worker(*args, **kwargs):
        try:
            return worker(*args, **kwargs)
        except Exception as e:
            raise Exception(worker, args, kwargs, e)

    return error_reporting_worker



class Pipe:
    def __init__(self, items):
        self.items = items

    @property
    def list_items(self):
        self.items = list(self.items)
        return self.items

    def _map(
        self,
        worker,
        args=None,
        kwargs=None,
        eager=True,
        show_progress=False,
        star=False,
        suppress_errors=False,
    ):
        worker = error_reporting_worker(worker)

        if suppress_errors:
            worker = with_suppressed_errors(worker)

        args, kwargs = ensure_good_args_kwargs(args, kwargs)
        iterator = wrap(self.items, tqdm, show_progress)

        if not star:
            out_items = (worker(item, *args, **kwargs) for item in iterator)
        elif star:
            out_items = (worker(*item, *args, **kwargs) for item in iterator)

        if eager:
            out_items = list(out_items)
        return Pipe(out_items)

    def map(
        self,
        worker,
        args=None,
        kwargs=None,
        eager=True,
        show_progress=False,
        suppress_errors=False,
    ):
        return self._map(
            worker,
            args=args,
            kwargs=kwargs,
            eager=eager,
            show_progress=show_progress,
            suppress_errors=suppress_errors,
            star=False,
        )

    def starmap(
        self,
        worker,
        args=None,
        kwargs=None,
        eager=True,
        show_progress=False,
        suppress_errors=False,
    ):
        return self._map(
            worker,
            args=args,
            kwargs=kwargs,
            eager=eager,
            show_progress=show_progress,
            suppress_errors=suppress_errors,
            star=True,
        )

    def _multi_map(
        self,
        worker,
        args=None,
        kwargs=None,
        processes=10,
        show_progress=False,
        star=False,
        suppress_errors=False,
    ):
        
        
        if suppress_errors:
            worker = with_suppressed_errors(worker)

        args, kwargs = ensure_good_args_kwargs(args, kwargs)

        with multiprocessing.Pool(processes) as pool:

            if not star:
                promises = [
                    pool.apply_async(
                        worker, args=tuple(chain([item], args)), kwds=kwargs
                    )
                    for item in self.items
                ]
            else:
                promises = [
                    pool.apply_async(worker, args=tuple(chain(item, args)), kwds=kwargs)
                    for item in self.items
                ]

            results = [p.get() for p in wrap(promises, tqdm, show_progress)]

        return Pipe(results)

    def multi_map(
        self,
        worker,
        args=None,
        kwargs=None,
        processes=10,
        show_progress=False,
        suppress_errors=False,
    ):
        return self._multi_map(
            worker,
            args=args,
            kwargs=kwargs,
            show_progress=show_progress,
            star=False,
            suppress_errors=False,
        )

    def multi_starmap(
        self,
        worker,
        args=None,
        kwargs=None,
        processes=10,
        show_progress=False,
        suppress_errors=False,
    ):
        return self._multi_map(
            worker,
            args=args,
            kwargs=kwargs,
            show_progress=show_progress,
            star=True,
            suppress_errors=False,
        )

    def group_by(self, key):
        d = collections.defaultdict(list)

        keys = map(key, self.items)
        for key, item in zip(keys, self.items):
            d[key].append(item)

        return Pipe(list(d.items()))

    def split(self, n=2):
        return Pipe(list(zip(itertools.count(), more_itertools.divide(n, self.items))))

    def chain(self):
        return Pipe(list(chain(*self.items)))
    
    def sort(self, key=None):
        return Pipe(sorted(self.items, key=key))
