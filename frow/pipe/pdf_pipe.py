from .pipe import Pipe


import contextlib
import os

def default_namer(path):
    *_, fn = os.path.split(path)
    return fn

class PdfPipe(Pipe):
    
    
    def doc_map(self, worker, outpath, outnamer = default_namer):
        
        with contextlib.suppress(FileExistsError):
            os.makedirs(outpath)
        
        output = [
            (worker(item), os.path.join(outpath, outnamer(item)))
            for item in self.items
        ]
    
        return super([outpath for _, outpath in output])
    

    def doc_mmap(self, worker, outpath, outnamer = default_namer, processes):
        
        with contextlib.suppress(FileExistsError):
            os.makedirs(outpath)
        
        output = [
            (worker(item), os.path.join(outpath, outnamer(item)))
            for item in self.items
        ]
    
        return super([outpath for _, outpath in output])    