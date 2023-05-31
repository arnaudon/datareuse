from pathlib import Path
import pandas as pd
from contextlib import contextmanager
import json


@contextmanager
def Reuse(filename, index=True, index_col=None, disable=False):
    """Context manager to reuse existing data file from previous run.

    At the moment, it is saved with pandas in .csv format only.

    index is passed to to_csv and index_col to read_csv

    Usage is as follow:

        with Reuse("data.csv") as reuse:
            df = reuse(computation, args, kwargs)
    """

    class reuse_data:
        def __init__(self, filename):
            self._filename = filename
            self._reader = None
            self._writer = None

        def dispatch_io(self, filename):
            if Path(filename).suffix == ".csv":

                def reader(name, args):
                    return pd.read_csv(name, index_col=index_col)

                def writer(data, name):
                    data.to_csv(name, index=index)

            elif Path(filename).suffix == ".json":

                def reader(name):
                    return json.read(open(name))

                def writer(data, name):
                    return json.write(data, open(name, "w"))

            else:
                raise ValueError("File format not understood.")

            self._reader = reader
            self._writer = writer

        def __call__(self, computation, *args, **kwargs):
            if not disable and Path(self._filename).exists():
                return pd.read_csv(self._filename, index_col=index_col)
            else:
                data = computation(*args, **kwargs)
                data.to_csv(self._filename, index=index)
                return data

    yield reuse_data(filename)
