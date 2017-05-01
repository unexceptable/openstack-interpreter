
from contextlib import contextmanager
from datetime import datetime


@contextmanager
def timed(desc):
    start = datetime.utcnow()
    yield
    end = datetime.utcnow()
    print("%s took: %s" % (desc, end - start))
