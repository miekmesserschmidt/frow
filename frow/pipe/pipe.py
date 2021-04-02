
import multiprocessing
import os 
import contextlib
import collections
from itertools import chain

def ensure_good_args_kwargs(args, kwargs):
    if args is  None:
        args = tuple()
        
    if kwargs is  None:
        kwargs = {}
        
    return args, kwargs


id = lambda x:x


class Pipe:
    
    def __init__(self, items):
        self.items = items
        
    
    def map(self, worker, args=None, kwargs = None):
        args, kwargs = ensure_good_args_kwargs(args, kwargs)
        
        out_items = [worker(item, *args, **kwargs) for item in self.items]
        return Pipe(out_items)


    def starmap(self, worker, args=None, kwargs = None):
        args, kwargs = ensure_good_args_kwargs(args, kwargs)
        
        out_items = [worker(*item, *args, **kwargs) for item in self.items]
        return Pipe(out_items)
            

    def multi_map(self, worker, args=None, kwargs = None, processes = 10):
        args, kwargs = ensure_good_args_kwargs(args, kwargs)

        with multiprocessing.Pool(processes) as pool:
            
            promises = [
                pool.apply_async(worker, args=tuple(chain([item], args)), kwds=kwargs) 
                for item in self.items
            ]
            results = [p.get() for p in promises]

        return Pipe(results)

    
    def multi_starmap(self, worker, args=None, kwargs = None, processes = 10):
        args, kwargs = ensure_good_args_kwargs(args, kwargs)

        with multiprocessing.Pool(processes) as pool:
            
            promises = [
                pool.apply_async(worker, args=tuple(chain(item, args)), kwds=kwargs) 
                for item in self.items
            ]
            results = [p.get() for p in promises]

        return Pipe(results)

    
    
    def group_by(self, key):    
        d = collections.defaultdict(list)
                
        keys = map(key, self.items)        
        for key, item in zip(keys, self.items):
            d[key].append(item)
            
        return Pipe(list(d.items()))
        
        
        
            
            
        
        
        