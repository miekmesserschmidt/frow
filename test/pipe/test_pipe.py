from frow.pipe import Pipe


def test_map():
    
    p = Pipe(["1234","2345", "3456"])
    
    q=p.map(lambda x:x[1])
    
    assert q.items == ["2", "3", "4"]
    

def test_map_args():
    
    p = Pipe(["1234","2345", "3456"])    
    q=p.map(lambda x, r:x[r], args=(2,))    
    assert q.items == ["3", "4", "5"]
    

def test_starmap_args():
    
    p = Pipe([
        ("12345", 0),
        ("23456", 1), 
        ("34567", 2),
    ])    
    q=p.starmap(lambda x, i, r:x[i*r], args=(2,))    
    assert q.items == ["1", "4", "7"]



def test_map_args_kwargs():
    def w(item, ind=1):
        return item[ind]
    
    p = Pipe(["1234","2345", "3456"])    
    q=p.map(w, kwargs={"ind" : 3})    
    assert q.items == ["4", "5", "6"]
    

def a(item):
    return item[1]

def test_multimap():
    
    p = Pipe(["1234","2345", "3456"])
    
    q=p.multi_map(a)
    
    assert q.items == ["2", "3", "4"]
    

def c(item, i, r):
    return item[i*r]

def test_multi_map_args():
    
    p = Pipe([
        ("12345", 0),
        ("23456", 1), 
        ("34567", 2),
    ])    
    q=p.multi_starmap(c, args=(2,))    
    assert q.items == ["1", "4", "7"]



def b(item, r):
    return item[r]

def test_multi_starmap_args():
    
    p = Pipe(["1234","2345", "3456"])    
    q=p.multi_map(b, args=(2,))    
    assert q.items == ["3", "4", "5"]

    

def globalw(item, ind=1):
    return item[ind]

def test_multi_map_args_kwargs():
    
    p = Pipe(["1234","2345", "3456"])    
    q=p.multi_map(globalw, kwargs={"ind" : 3})    
    assert q.items == ["4", "5", "6"]
    


def test_group_by():
    
    p = Pipe(["a1234","a2345", "b3456"])    
    q=p.group_by(key = lambda item: "a" in item)
    assert q.items == [
        (True, ["a1234","a2345"]),
        (False, ["b3456"])
    ]
    

import time
def sleeper(item):
    time.sleep(1)
    return item

def test_multimap_sleep():
    
    p = Pipe(range(10))
   
    q=p.multi_map(sleeper)
    
