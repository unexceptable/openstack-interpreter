from contextlib import contextmanager
from datetime import datetime


@contextmanager
def timed(desc):
    """
    A useful context manager for timing how long something took

    Example use:
    In [1]: with timed("getting server list:"):
       ...:     oi.sdk.connection.compute.servers()
       ...:
    getting server list: took: 0:00:00.001366
    """
    start = datetime.utcnow()
    yield
    end = datetime.utcnow()
    print("%s took: %s" % (desc, end - start))
