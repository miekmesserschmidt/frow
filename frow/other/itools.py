import more_itertools

def bucket(container, bucket_key = lambda x: x, sort_key= None):
    b = more_itertools.bucket(container, bucket_key)
    return {k: sorted(list(b[k]), key=sort_key) for k in b}
