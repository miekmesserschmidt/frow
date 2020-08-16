import fitz

class PickableFitzDoc:
    """A wrapper that behaves like a fitz doc, but is picklable so can be used with multiprocessing.
    
    Pass it as constructor to frow.tools.pdf.open_ensuring_pdf.
    """
    
    def __init__(self, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs
        self._doc = None
        
    @property
    def doc(self):
        if not self._doc:            
            self._doc = fitz.open(*self._args, **self._kwargs)
        return self._doc
        
    def __getattr__(self, name):
        return getattr(self.doc, name)
        
    def __getitem__(self, index):
        return PickableFitzPage( self._args, self._kwargs, index, doc=self.doc)
    
    def __getstate__(self):
        d = self.__dict__.copy()
        d["_doc"] = None
        return d

    def __setstate__(self,state):
        self.__dict__=state.copy()
        self._doc = None
    
    
    def pages(self):
        for i in range(self.doc.pageCount):
            yield PickableFitzPage( self._args, self._kwargs, i, doc=self.doc)
        
    

class PickableFitzPage:
    """A wrapper that behaves like a fits page, but is picklable so can be used with multiprocessing.
    """
    
    def __init__(self, doc_args, doc_kwargs, page_index, doc=None):
        self._doc_args = doc_args
        self._doc_kwargs = doc_kwargs
        self._page_index = page_index
        
        self._doc = doc
        self._page = None

    @property
    def doc(self):
        if not self._doc:            
            self._doc = PickableFitzDoc(*self._doc_args, **self._doc_kwargs)
        return self._doc

    @property
    def page(self):
        if self._page:            
            return self._page
        else:
            self._page = self.doc[self._page_index]        
            return self._page
        
        
    def __getattr__(self, name):        
        if name in ("_page_index", "_doc_args", "_doc_kwargs", "_doc"):
            raise ValueError(f"Not supposed to happen {name}")
        return getattr(self.page, name)
        
    
    def __getstate__(self):
        d = self.__dict__.copy()
        d["_doc"] = None
        d["_page"]= None
        return d
    
    def __setstate__(self,state):
        self.__dict__=state.copy()
        self._doc = None
        self._page = None
    