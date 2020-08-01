import os


class Files:
    def __init__(self, path):
        self.path = path
        self.rel = lambda p: os.path.relpath(p, self.path)

    def joined(self):
        yield from (os.path.join(base, fn) for base, fn in self)


class FilesRecursive(Files):
    def __iter__(self,):
        for root, _, files in os.walk(self.path):
            yield from ((self.path, self.rel(os.path.join(root, f))) for f in files)


class DirsRecursive(Files):
    def __iter__(self,):
        for root, dirs, _ in os.walk(self.path):
            yield from ((self.path, self.rel(os.path.join(root, d))) for d in dirs)


class FilesNonRecursive(Files):
    def __iter__(self,):
        yield from ((self.path, i.name) for i in os.scandir(self.path) if i.is_file())


class DirsNonRecursive(Files):
    def __iter__(self,):
        yield from ((self.path, i.name) for i in os.scandir(self.path) if i.is_dir())

