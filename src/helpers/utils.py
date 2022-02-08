from contextlib import contextmanager
from time import time


@contextmanager
def timer():
    start = time()
    yield
    end = time()
    print(end-start)
